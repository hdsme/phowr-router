import uvicorn
from fastapi import FastAPI
from phowr_router.core import DynamicRouter

app = FastAPI()

easy_router = DynamicRouter()

app.include_router(router=easy_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)