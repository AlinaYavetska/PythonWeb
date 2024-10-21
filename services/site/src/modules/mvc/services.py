from fastapi.responses import RedirectResponse

from src.common.templates import templates
from src.models.borrow_cards.models import BorrowCard
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
        orders = await BorrowCardRepository.get_all_by_user_id(db, user_id)

        return templates.TemplateResponse("home.html", {
            "request": request,
            "username": user_id,
            "orders": orders,
            "products": products
        })

    async def add_order(self, request, db, product_id, quantity):
        product = await ProductRepository.get_one(db, product_id)
        await BorrowCardRepository.create(db, BorrowCard(
            user_id=request.session.get("user_id"),
            product_id=product.id,
            qty=quantity
        ))
        return RedirectResponse(url="/home", status_code=303)

    async def remove_order(self, request, db, order_id):
        await BorrowCardRepository.delete(db, await BorrowCardRepository.get_order_by_id(db, order_id))
        return RedirectResponse(url="/home", status_code=303)


from src.models.borrow_item.models import BorrowItem
from src.models.borrow_item.repository import BorrowRepository


class CartService:

    async def create_cart_item(self, user_id, db, product_id):
        product = await ProductRepository.get_one(db, product_id)
        product.isAvailable = False
        await ProductRepository.update(db, product)
        return await BorrowRepository.create(db, BorrowItem(
            user_id=user_id,
            product_id=product.id
        ))

    async def delete_cart_item(self, db, cart_item_id):
        await BorrowRepository.delete(
            db, await BorrowRepository.get_one(db, cart_item_id))


class OrderService:

    async def create_order(self, db, user_id, product_id):
        product = await ProductRepository.get_one(db, product_id)
        return await BorrowCardRepository.create(db, BorrowCard(
            user_id=user_id,
            product_id=product.id
        ))


class homeViews:

    def __init__(self):
        self.order_service = OrderService()
        self.cart_service = CartService()


    async def display_home(self, request, db) -> templates.TemplateResponse:
        user_id = request.session.get("user_id")
        products = await ProductRepository.get_all(db)
        cart_items = await BorrowRepository.get_all_by_user_id(db, user_id)
        orders = await BorrowCardRepository.get_all_by_user_id(db, user_id)
        return templates.TemplateResponse("home.html", {
            "request": request,
            "username": user_id,
            "borrow_cards": orders,
            "products": products,
            "borrow_item_count": len(cart_items)
        })

    async def add_to_cart(self, request, db, product_id) -> RedirectResponse:
        product = await ProductRepository.get_one(db, product_id)
        cart_item = await self.cart_service.create_cart_item(
            request.session.get("user_id"), db, product_id
        )
        return RedirectResponse(url="/home", status_code=303)

    async def remove_from_cart(self, db, cart_item_id) -> RedirectResponse:
        await self.cart_service.delete_cart_item(db, cart_item_id)
        return RedirectResponse(url="/home", status_code=303)
