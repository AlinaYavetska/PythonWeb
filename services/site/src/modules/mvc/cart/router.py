from fastapi import APIRouter, Request, Depends, Form

from src.modules.mvc.cart.services import CartViews, BorrowCardService

from src.common.database import get_postgres

router = APIRouter(prefix="/cart")

cart_view = CartViews()


@router.get("")
async def get_cart(request: Request, db=Depends(get_postgres)):
    return await cart_view.display_cart(request, db)


@router.post("/remove")
async def remove_from_cart(
        item_id: int = Form(...),
        db=Depends(get_postgres)):
    return await cart_view.remove_from_cart(db, item_id)


@router.post("/checkout")
async def checkout(request: Request, db=Depends(get_postgres)):
    return await cart_view.checkout(request, db)
