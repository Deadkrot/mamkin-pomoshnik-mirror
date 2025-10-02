from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, BigInteger, DateTime, Text

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    dob: Mapped[str | None] = mapped_column(String(10))   # YYYY-MM-DD (опционально)
    age_months: Mapped[int | None] = mapped_column(Integer)
    formula_name: Mapped[str] = mapped_column(String(64), default="Nan Opti Pro 1")
    feeds_per_day: Mapped[int] = mapped_column(Integer, default=6)
    wake_time: Mapped[str] = mapped_column(String(5), default="07:00")
    night_start: Mapped[str] = mapped_column(String(5), default="20:30")
    night_end:   Mapped[str] = mapped_column(String(5), default="06:30")
    tz: Mapped[str] = mapped_column(String(64), default="Europe/Amsterdam")
    onboarding_done: Mapped[int] = mapped_column(Integer, default=0)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    kind: Mapped[str] = mapped_column(String(16))  # 'feed' | 'sleep_start' | 'sleep_end'
    at: Mapped[DateTime] = mapped_column(DateTime)
    note: Mapped[str | None] = mapped_column(Text)

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    key: Mapped[str] = mapped_column(String(64), index=True)   # уникальный ключ напоминания
    when: Mapped[DateTime] = mapped_column(DateTime)
    payload: Mapped[str | None] = mapped_column(Text)
