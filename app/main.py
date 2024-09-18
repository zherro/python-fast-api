from fastapi import FastAPI
from app.api.endpoints import items

app = FastAPI(
    title="FastAPI Project",
    description="An organized FastAPI project following best practices.",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Include the items router
app.include_router(items.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
