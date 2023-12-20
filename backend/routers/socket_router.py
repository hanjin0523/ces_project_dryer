from fastapi import APIRouter

router = APIRouter(prefix="/socket", tags=["socket"])

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/{name}")
async def ro(name: str):
    return {f'message: {name}'}