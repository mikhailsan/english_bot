from sqlalchemy import Column, Integer, Date
from .database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    user_id = Column(Integer, primary_key=True, index=True)
    last_index = Column(Integer, default=0)
    last_sent = Column(Date)
    daily_index = Column(Integer, default=0)  # ✅ новая колонка
