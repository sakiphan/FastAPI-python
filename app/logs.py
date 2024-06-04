from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from .database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)
    endpoint = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    username = Column(String, nullable=True)
    user_agent = Column(String)

def create_log(db: Session, ip_address: str, endpoint: str, method: str, status_code: int, username: str = None, user_agent: str = None):
    db_log = Log(ip_address=ip_address, endpoint=endpoint, method=method, status_code=status_code, username=username, user_agent=user_agent)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log