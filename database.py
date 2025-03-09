from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()
engine = create_engine("postgresql://quest_user:secure_password@localhost:5432/questbot")
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    character = Column(String)
    balance = Column(Integer, default=100)
    completed_quests = Column(Integer, default=0)
    has_access_to_casino = Column(Boolean, default=False)

class QuestHistory(Base):
    __tablename__ = "quest_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quest_name = Column(String)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
