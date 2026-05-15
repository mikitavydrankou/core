from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db

router = APIRouter()


@router.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Taxi dispatch prototypeee",
        "simulator": "/sim",
        "dispatcher": "/dispatch",
        "logs": "/monitor",
    }


@router.get("/api/health/db")
async def db_health(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    result = await db.execute(text("SELECT 1"))
    return {"status": "ok", "db": str(result.scalar_one())}
