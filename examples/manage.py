import os, uvicorn, re
from fastapi import APIRouter, FastAPI
import importlib

app = FastAPI()

easy_router = DirectoryRouter()

app.include_router(prefix='/api', router=easy_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)