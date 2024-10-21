from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.common.database import Base


class BorrowItem(Base):
    __tablename__ = "borrow_item"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String)
    product_id = Column(ForeignKey("product.id"), nullable=False)

    product = relationship("Product")