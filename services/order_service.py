from models.order import Order
from models.cart import Cart
from services.product_service import ProductService


class OrderService:

    # ==========================================
    # ساخت سفارش
    # ==========================================

    @staticmethod
    def create_order(user_id):

        cart = Cart(user_id)

        items = cart.get_items()

        if not items:
            return None

        for item in items:

            product_id = item[0]
            quantity = item[3]

            result = ProductService.decrease_stock(
                product_id,
                quantity
            )

            if not result:
                return None

        total = cart.get_total_price()

        order = Order(
            user_id,
            total
        )

        order_id = order.create(
            items
        )

        cart.clear()

        return order_id

    # ==========================================
    # تغییر وضعیت
    # ==========================================

    @staticmethod
    def change_status(
        order_id,
        status
    ):

        Order.update_status(
            order_id,
            status
        )

    # ==========================================
    # سفارش‌های کاربر
    # ==========================================

    @staticmethod
    def get_user_orders(
        user_id
    ):

        return Order.get_user_orders(
            user_id
        )

    # ==========================================
    # همه سفارش‌ها
    # ==========================================

    @staticmethod
    def get_orders():

        return Order.get_all_orders()

    # ==========================================
    # سفارش‌های در انتظار
    # ==========================================

    @staticmethod
    def get_pending_orders():

        return Order.get_pending_orders()

    # ==========================================
    # تاریخچه
    # ==========================================

    @staticmethod
    def get_order_history():

        return Order.get_order_history()

    # ==========================================
    # لغو سفارش
    # ==========================================

    @staticmethod
    def cancel_order(
        order_id
    ):

        return Order.cancel_order(
            order_id
        )