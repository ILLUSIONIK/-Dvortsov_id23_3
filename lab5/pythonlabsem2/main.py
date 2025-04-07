import asyncio
from fastapi import FastAPI, HTTPException
from app.api import auth
from app import schemas
from app import bruteforce
import uuid

app = FastAPI()

app.include_router(auth.router)

@app.post("/brut_hash", response_model=schemas.TaskIdResponse)
async def brut_hash(request: schemas.BrutHashRequest):
    task_id = str(uuid.uuid4())
    bruteforce.tasks[task_id] = {"status": "pending", "progress": 0, "result": None}
    asyncio.create_task(asyncio.to_thread(bruteforce.bruteforce_task, task_id, request.hash, request.charset, request.max_length))
    return schemas.TaskIdResponse(task_id=task_id)

@app.get("/get_status", response_model=schemas.TaskStatusResponse)
async def get_status(task_id: str):
    if task_id not in bruteforce.tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = bruteforce.tasks[task_id]
    return schemas.TaskStatusResponse(status=task["status"], progress=task["progress"], result=task["result"])

@app.get("/")
async def root():
    return {"message": "Hello World"}