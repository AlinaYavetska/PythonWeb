from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from src.common.templates import templates
from src.models.borrow_cards.models import BorrowCard, BorrowCardProducts
from src.models.borrow_cards.repository import BorrowCardRepository
from src.models.products.repository import ProductRepository


class SiteViews:

    async def get_home_page(self, request):
        return templates.TemplateResponse(request=request, name="index.html")

    async def get_login_page(self, request):
        return templates.TemplateResponse(request=request, name="login.html")

    async def login(self, request, username, password):
        request.session['user_id'] = username
        return RedirectResponse(url="/home", status_code=303)

    async def logout(self, request):
        request.session.pop("user_id", None)
        return RedirectResponse(url="/login", status_code=303)

    async def get_home(self, request, db):
        user_id = request.session.get("user_id")
        products = await ProductRepository.get_all(db)
        borrow_cards = await BorrowCardRepository.get_all_by_user_id(db, user_id)

        return templates.TemplateResponse("home.html", {
            "request": request,
            "username": user_id,
            "borrow_cards": borrow_cards,
            "products": products
        })

    async def add_borrow_card(self, request, db, product_id):
        product = await ProductRepository.get_one(db, product_id)
        await BorrowCardRepository.create(db, BorrowCard(
            user_id=request.session.get("user_id"),
            product_id=product.id,
        ))
        return RedirectResponse(url="/home", status_code=303)

    async def remove_order(self, request, db, order_id):
        await BorrowCardRepository.delete(db, await BorrowCardRepository.get_order_by_id(db, order_id))
        return RedirectResponse(url="/home", status_code=303)


from src.models.borrow_item.models import BorrowItem
from src.models.borrow_item.repository import BorrowRepository


class BorrowService:

    async def create_borrow_item(self, user_id, db, product_id):
        product = await ProductRepository.get_one(db, product_id)
        return await BorrowRepository.create(db, BorrowItem(
            user_id=user_id,
            product_id=product.id,
        ))

    async def delete_cart_item(self, db, cart_item_id):
        borrowItem = await BorrowRepository.get_one(db, cart_item_id)
        product = await ProductRepository.get_one(db, borrowItem.product_id)
        product.isAvailable = True
        await ProductRepository.update(db, product)
        await BorrowRepository.delete(
            db, borrowItem)


class BorrowCardService:

    async def create_borrow_card(self, db, user_id):
        borrow_items = await BorrowRepository.get_all_by_user_id(db, user_id)
        order = await BorrowCardRepository.flush(
            db,
            BorrowCard(
                user_id=user_id,
                borrowed_date=datetime.now(),
                due_date=datetime.now() + timedelta(weeks=2)
            )
        )
        db.add_all([
            BorrowCardProducts(
                borrow_card_id=order.id,
                product_id=borrow_item.product_id,
            )
            for borrow_item in borrow_items
        ])

        await BorrowRepository.delete_by_user_id(db, user_id)


class homeViews:

    def __init__(self):
        self.order_service = BorrowCardService()
        self.cart_service = BorrowService()

    async def display_home(self, request, db) -> templates.TemplateResponse:
        user_id = request.session.get("user_id")
        products = await ProductRepository.get_all(db)
        borrow_items = await BorrowRepository.get_all_by_user_id(db, user_id)
        return templates.TemplateResponse("home.html", {
            "request": request,
            "username": user_id,
            "borrow_items": borrow_items,
            "products": products,
            "borrow_item_count": len(borrow_items)
        })

    async def add_to_cart(self, request, db, product_id) -> RedirectResponse:
        product = await ProductRepository.get_one(db, product_id)
        cart_item = await self.cart_service.create_borrow_item(
            request.session.get("user_id"), db, product_id)
        return RedirectResponse(url="/home", status_code=303)

    async def remove_from_cart(self, db, cart_item_id) -> RedirectResponse:
        await self.cart_service.delete_cart_item(db, cart_item_id)
        return RedirectResponse(url="/home", status_code=303)


class CartViews:

    def __init__(self):
        self.order_service = BorrowCardService()
        self.cart_service = BorrowService()

    async def display_cart(self, request, db):
        user_id = request.session.get("user_id")
        cart_items = await BorrowRepository.get_all_by_user_id(db, user_id)
        return templates.TemplateResponse("picks.html", {
            "request": request,
            "username": user_id,
            "borrow_items": cart_items
        })

    async def remove_from_cart(self, db, cart_item_id):
        await self.cart_service.delete_cart_item(db, cart_item_id)
        return RedirectResponse(url="/cart", status_code=303)

    async def checkout(self, request, db):
        user_id = request.session.get("user_id")
        await self.order_service.create_borrow_card(db, user_id)
        return RedirectResponse(url="/cart", status_code=303)
