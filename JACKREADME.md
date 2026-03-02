# Tech Test: Python Backend Wired up to Existing Frontend

  

## Overview

  

This project implements the backend for the provided FastAPI + frontend tech test, exposing a small REST API backed by PostgreSQL so the existing frontend can create, list, and delete items without any changes to its expectations.

  

The service is written with scalability in mind so it can be containerised and deployed behind a load balancer in AWS or a similar environment.

  

---

  

## Stack

  

- Python 3.13
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pytest for tests
- Git (Version control on home machine) 

  

## Tech

- Task Completed on Windows 11
- Visual Code Studio for my IDE
- Postgres Running Locally
- Postman for API development and testing

  
  

---

  

## Setup

  

Create and activate a virtualenv, then install dependencies:

  

```bash

python  -m  venv  .venv

source  .venv/bin/activate  # Windows: .venv\Scripts\activate

pip  install  -r  requirements.txt

```

  

## Project Structure

 
tech-test-python/
├── backend/
│   ├── main.py          # FastAPI application and route handlers
│   ├── database.py      # SQLAlchemy engine, sessions, Base, DB dependency
│   ├── models.py        # SQLAlchemy ORM models (ItemModel)
│   └── schemas.py       # Pydantic models for request/response schemas
├── frontend/
│   └── index.html       # Provided SPA that consumes the API
├── tests/
│   └── test_api.py      # API test suite (pytest)
├── requirements.txt
├── .env # Local development settings
├── JACKREADME.md # Developer notes!
└── README.md # Original Spec


---

### PostgreSQL Setup

I used PGAdmin 4 to set up the databases locally.

**Production Database:**

1. Install PostgreSQL (version 12+)

2. Create a database for the application:

3. Set your database connection string in `.env`:

```

DATABASE_URL=postgresql://username:password@localhost:5432/tech_test_db

```

  

**Testing Database:**

The test suite uses a separate PostgreSQL database to avoid data pollution:

1. Create testing database

2. Update `.env`:

```

DATABASE_URL=postgresql://username:password@localhost:5432/tech_test_db_test

```

  

### Running Migrations

  

SQLAlchemy models are automatically synced on application startup. Within production, tools like Alembic can be used for version controlled migrations.

  

### Running Tests

  

Tests will automatically create and tear down tables in the test database:

```bash

pytest tests/test_api.py -v -s

```

  



## Running The Project

This has not changed since from the original task description:

#### 1. Backend

  

From the repository root:

  

```bash

python  -m  venv  .venv

source  .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip  install  -r  requirements.txt

  

uvicorn  backend.main:app  --reload

```

  

By default the backend will be available at `http://localhost:8000`.

  

You can verify it is running with:

  

```bash

curl  http://localhost:8000/health

```

  

#### 2. Frontend

  

From a separate terminal, in the `frontend` directory:

  

```bash

cd  frontend

python  -m  http.server  5173

```

  

Then open `http://localhost:5173` in your browser.

## Development Choices

Throughout this task I approached my code with an I-gaming/high request scenarios in mind. I have left comments within the code however in this section ill give an over of the choices made.

1. I used PostgreSQL with UUID primary keys (generated in the database) which should scale up nicely through multiple instances.
2. Connection pool settings, I have lifted some primary settings from past RGS deployments, these can be fine tuned in production against various factors, however I have exposed the connection settings to show awareness of their role in session management.
3. Container viability, I have tried to have this service depend on environment variables whilst retaining the standard ports, so it can be straightforward to dockerise and deploy.
4. Originally I was using an SQLite database for testing, however this would not have been representative of a production like environment, as there would have been some hard code changes to get the tests to pass. I decided to spin up a 2nd PG database for the test suite to replicate a production environment, and this would make it easier for CI pipelines within production.

---

## Candidate notes

1. I have to the best of my ability followed modern coding/python conventions. Splitting the core logic into their own files (database.py/models.py/...) for improved readability.
2. Whilst I have left comments in the code, I believe well written code should be mostly self explanatory. 