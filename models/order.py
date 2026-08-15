from database.connection import get_connection


class Order:

    def __init__(
        self,
        user_id,
        total,
        status="pending"
    ):

        self.user_id = user_id
        self.total = total
        self.status = status


    # ==========================================
    # ساخت سفارش
    # ==========================================

    def create(self, items):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO orders
            (user_id, total, status)
            VALUES (?, ?, ?)
            """,
            (
                self.user_id,
                self.total,
                self.status
            )
        )

        order_id = cursor.lastrowid

        for item in items:

            product_id = item[0]
            product_name = item[1]
            price = item[2]
            quantity = item[3]

            cursor.execute(
                """
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    product_name,
                    quantity,
                    price
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    product_id,
                    product_name,
                    quantity,
                    price
                )
            )

        conn.commit()
        conn.close()

        return order_id


    # ==========================================
    # سفارش‌های کاربر
    # ==========================================

    @staticmethod
    def get_user_orders(user_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        orders = cursor.fetchall()

        conn.close()

        return orders


    # ==========================================
    # تغییر وضعیت سفارش
    # ==========================================

    @staticmethod
    def update_status(
        order_id,
        status
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            """,
            (
                status,
                order_id
            )
        )

        conn.commit()
        conn.close()


    # ==========================================
    # همه سفارش‌ها
    # ==========================================

    @staticmethod
    def get_all_orders():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            ORDER BY id DESC
            """
        )

        orders = cursor.fetchall()

        conn.close()

        return orders


    # ==========================================
    # سفارش‌های در انتظار
    #
    # pending    → در انتظار بررسی
    # accepted   → تایید شده
    # shipping   → در حال ارسال
    # ==========================================

    @staticmethod
    def get_pending_orders():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE status IN (
                'pending',
                'accepted',
                'shipping'
            )
            ORDER BY id DESC
            """
        )

        orders = cursor.fetchall()

        conn.close()

        return orders


    # ==========================================
    # تاریخچه سفارش‌ها
    #
    # completed → دریافت شده
    # cancelled → لغو شده
    # ==========================================

    @staticmethod
    def get_order_history():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE status IN (
                'completed',
                'cancelled'
            )
            ORDER BY id DESC
            """
        )

        orders = cursor.fetchall()

        conn.close()

        return orders


    # ==========================================
    # لغو سفارش توسط کاربر
    # فقط سفارش pending قابل لغو است
    # ==========================================

    @staticmethod
    def cancel_order(order_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE orders
            SET status = ?
            WHERE id = ?
            AND status = ?
            """,
            (
                "cancelled",
                order_id,
                "pending"
            )
        )

        affected = cursor.rowcount

        conn.commit()
        conn.close()

        return affected > 0


    # ==========================================
    # محصولات سفارش
    # ==========================================

    @staticmethod
    def get_order_items(order_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                order_items.product_name,
                order_items.quantity
            FROM order_items
            WHERE order_items.order_id = ?
            """,
            (order_id,)
        )

        items = cursor.fetchall()

        conn.close()

        return items
