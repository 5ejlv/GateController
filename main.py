from fastapi import FastAPI
import uvicorn
from api_v1.RequestRouter import request_router

app = app = FastAPI(
    title="Dashboard",
)

app.include_router(request_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)