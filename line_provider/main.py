import os

from app.routers import router
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("APP_HOST"),
        port=int(os.getenv("APP_HOST_PORT")),
        reload=True
    )
