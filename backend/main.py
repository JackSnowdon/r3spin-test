from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Tech Test API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items():
    raise HTTPException(status_code=501, detail="Not implemented")


@app.post("/api/items")
def create_item():
    raise HTTPException(status_code=501, detail="Not implemented")


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    raise HTTPException(status_code=501, detail="Not implemented")

