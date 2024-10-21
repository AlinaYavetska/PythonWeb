from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.common.database import Base


class BorrowCard(Base):
    __tablename__ = "borrow_card"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String)
    borrowed_date = Column(Date) 
    due_date = Column(Date)

    products = relationship("Product", secondary="borrow_card_products")


class BorrowCardProducts(Base):
    __tablename__ = "borrow_card_products"
    borrow_card_id = Column(Integer, ForeignKey("borrow_card.id"), primary_key=True)
    product_id = Column(ForeignKey("product.id"), primary_key=True)