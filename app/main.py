from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware

from app.schemas.base import ResponseBase


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "ok"}


@app.get(
    "/health",
    response_model=ResponseBase,
    description="Health Check API",
)
async def health_check() -> ResponseBase:
    return ResponseBase(
        code=status.HTTP_200_OK,
        message="Server Alive",
        data={"status": "alive"},
    )
