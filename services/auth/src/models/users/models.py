from uuid import uuid4

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects import postgresql

from src.common.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    uuid = Column(postgresql.UUID(as_uuid=True), default=uuid4, unique=True, index=True)

    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)

    password = Column(String)

    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    is_enabled = Column(Boolean, default=True)