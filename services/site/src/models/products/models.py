from sqlalchemy import Column, String, Integer, Boolean

from src.common.database import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    isAvailable = Column(Boolean, nullable=False)
