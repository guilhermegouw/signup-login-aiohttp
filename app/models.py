from sqlalchemy import Column, Integer, String

from app.config import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
