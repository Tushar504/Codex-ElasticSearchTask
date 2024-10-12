from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from db import get_db
from es import es

from models.task import Tasks
from schemas.task import Task, TaskCreate, TaskSearchResponse

router = APIRouter(prefix='/tasks')

@router.post('/', response_model=Task)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = Tasks(title=task_data.title, description=task_data.description)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        es.index(index="tasks", id=new_task.id, body={
            "title": new_task.title,
            "description": new_task.description
        })

        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/search", response_model=TaskSearchResponse)
async def search_documents(q: str, response: Response):
    try:
        search_query = {
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["title^2", "description"]
                }
            }
        }
        es_response = es.search(index="tasks", body=search_query)

        results = []
        for hit in es_response['hits']['hits']:
            field = "title" if q in hit["_source"]["title"] else "description"
            results.append({
                "id": hit["_id"],
                "fieldName": field,
                "fieldContent": hit["_source"][field]
            })
        response.status_code = 200
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.patch("/{task_id}", response_model=Task)
async def update_document(task_id: int, task_to_update: TaskCreate, db: Session = Depends(get_db)):
    try:
    
        task = db.query(Tasks).filter(Tasks.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Document not found")

        task.title = task_to_update.title
        task.description = task_to_update.description
        db.commit()
        db.refresh(task)

        es.update(index="tasks", id=task_id, body={
            "doc": {
                "title": task.title,
                "description": task.description
            }
        })

        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))