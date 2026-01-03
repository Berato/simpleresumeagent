# Simple Resume Agent

A basic FastAPI application with standard project structure using Poetry.

## Setup

1. Install Poetry (if not already installed).
2. Install dependencies:
   ```bash
   make install
   ```

## Running the application

```bash
make run
```

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Database (MongoDB)

The project uses MongoDB via Docker Compose.

- MongoDB Port: `27018` (local) mapped to `27017` (container)
- Mongo Express GUI: [http://localhost:8082](http://localhost:8082)
- Credentials (Admin): `admin` / `password`

To start the database:
```bash
make db-up
```
# simpleresumeagent
