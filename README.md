## Tech Test: Python Backend + Simple Frontend

### What is already provided

- **Backend framework**: A minimal [FastAPI](https://fastapi.tiangolo.com/) application in `backend/main.py` with:
  - a working `GET /health` endpoint
  - placeholder endpoints for:
    - `GET /api/items`
    - `POST /api/items`
    - `DELETE /api/items/{item_id}`
- **Frontend**: A single page in `frontend/index.html` that:
  - calls `GET /api/items` to load items
  - calls `POST /api/items` with `{ "name": string }` to create a new item
  - calls `DELETE /api/items/{id}` to remove an item

The frontend assumes the backend is running at `http://localhost:8000`.

### Candidate task

- **Goal**: Expose a small REST API backed by a real database so that the existing frontend behaves as expected.

- **You should implement (server side)**:
  - A database connection (any reasonable approach is fine: SQLAlchemy, an ODM, raw driver, etc.).
  - A remote mongo database can be enabled on request, but using a local database is absolutely fine.
  - A persistent `Item` concept with at least:
    - `id`: unique identifier (number or string)
    - `name`: string
  - The three API endpoints:
    - `GET /api/items`  
      - Returns a JSON array of items, for example:
        - `[{ "id": 1, "name": "Write tech test" }]`
    - `POST /api/items`  
      - Accepts a JSON body: `{ "name": "Some item name" }`
      - Creates and persists a new item.
      - Returns the created item as JSON.
    - `DELETE /api/items/{item_id}`  
      - Deletes the item with the given `id`.
      - Returns an appropriate success response.

- **You may**:
  - Create additional Python modules and packages under `backend/`.
  - Use the existing `.env` values to connect to our remote database or introduce new environment variables if you prefer.
    (To connect to our remote mongo database you will need to be whitelisted.)
  - Add extra endpoints, tests, or validations if it helps show how you structure code.

- **You should not change**:
  - The basic behaviour of the frontend or the shape of the API it expects (URL paths and basic JSON structures).

### Running the project

#### 1. Backend

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn backend.main:app --reload
```

By default the backend will be available at `http://localhost:8000`.

You can verify it is running with:

```bash
curl http://localhost:8000/health
```

#### 2. Frontend

From a separate terminal, in the `frontend` directory:

```bash
cd frontend
python -m http.server 5173
```

Then open `http://localhost:5173` in your browser.
