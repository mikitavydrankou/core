from datetime import datetime

from sqlalchemy import DateTime, Float, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class DriverState(Base):
    __tablename__ = "driver_states"

    driver_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(32), server_default=text("'online'"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
