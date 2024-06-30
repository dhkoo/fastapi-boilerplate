from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from app.databases.rdb import get_db
from app.schemas.base import ResponseBase
from app.api import user

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "ok"}


@app.get(
    "/health",
    response_model=ResponseBase,
    description="Health Check API",
)
async def health_check():
    return ResponseBase(
        code=200,
        message="Server Alive",
        data={"status": "alive"},
    )


@app.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return ResponseBase(
            code=200,
            message="Database connection successful",
            data={"status": "ok"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}")
