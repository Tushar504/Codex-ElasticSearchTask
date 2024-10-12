# FastAPI Application with PostgreSQL and Elasticsearch

This project is a FastAPI application that connects to PostgreSQL and Elasticsearch. It provides RESTful APIs for managing tasks, including creating, searching, and updating data.

## Services

### 1. Elasticsearch

- **Image**: `docker.elastic.co/elasticsearch/elasticsearch:8.1.0`
- **Container Name**: `es`
- **Environment Variables**:
  - `discovery.type`: Set to `single-node` for single-node setups.
  - `xpack.security.enabled`: Set to `false` to disable security features.
- **Ports**: 
  - `9200:9200` - Exposes Elasticsearch on port 9200.
- **Volumes**:
  - `esdata`: Persistent storage for Elasticsearch data.

### 2. PostgreSQL

- **Image**: `postgres:latest`
- **Environment Variables**:
  - `POSTGRES_USER`: The user for the PostgreSQL database (set via environment).
  - `POSTGRES_PASSWORD`: The password for the PostgreSQL user (set via environment).
  - `POSTGRES_DB`: The name of the database to create (set via environment).
- **Ports**: 
  - `5432:5432` - Exposes PostgreSQL on port 5432.
- **Volumes**:
  - `pgdata`: Persistent storage for PostgreSQL data.

### 3. FastAPI Application

- **Build**: Builds the FastAPI app from the Dockerfile in the current directory.
- **Container Name**: `fastapi_app`
- **Environment Variables**:
  - `DATABASE_URL`: Connection string for PostgreSQL, formatted as:
    ```
    postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
    ```
- **Ports**: 
  - `8000:8000` - Exposes the FastAPI app on port 8000.
- **Dependencies**: The FastAPI app depends on both the PostgreSQL and Elasticsearch services.

## Getting Started

### Prerequisites

- Ensure you have Docker and Docker Compose installed on your machine.

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tushar504/Codex-ElasticSearchTask.git
   cd your-repo
2. **Set environment variables: Create a .env file in the root directory and add your PostgreSQL credentials**:
   - `POSTGRES_USER`=yourusername
   - `POSTGRES_PASSWORD`=yourpassword
   - `POSTGRES_DB`=yourdatabase
3. **Build and run the services**:
   ```bash
   docker-compose up --build
