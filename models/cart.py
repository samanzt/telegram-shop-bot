from database.connection import get_connection


class Cart:

    def __init__(self, user_id):
        self.user_id = user_id


    def add_product(self, product_id, quantity=1):

        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT *
            FROM cart
            WHERE user_id = ?
            AND product_id = ?
            """,
            (
                self.user_id,
                product_id
            )
        )


        item = cursor.fetchone()


        if item:

            cursor.execute(
                """
                UPDATE cart
                SET quantity = quantity + ?
                WHERE user_id = ?
                AND product_id = ?
                """,
                (
                    quantity,
                    self.user_id,
                    product_id
                )
            )


        else:

            cursor.execute(
                """
                INSERT INTO cart
                (user_id, product_id, quantity)
                VALUES (?, ?, ?)
                """,
                (
                    self.user_id,
                    product_id,
                    quantity
                )
            )


        conn.commit()
        conn.close()



    def remove_product(self, product_id):

        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            DELETE FROM cart
            WHERE user_id = ?
            AND product_id = ?
            """,
            (
                self.user_id,
                product_id
            )
        )


        conn.commit()
        conn.close()



    def get_items(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            products.id,
            products.name,
            products.price,
            cart.quantity

            FROM cart

            JOIN products
            ON cart.product_id = products.id

            WHERE cart.user_id = ?
            """,
            (self.user_id,)
        )


        items = cursor.fetchall()

        conn.close()

        return items



    def get_total_price(self):

        items = self.get_items()

        total = 0


        for item in items:
            product_id = item[0]
            name = item[1]
            price = item[2]
            quantity = item[3]


            total += price * quantity


        return total

    def clear(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM cart
            WHERE user_id = ?
            """,
            (self.user_id,)
        )

        conn.commit()
        conn.close()

    def increase_quantity(self, product_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT stock
            FROM products
            WHERE id = ?
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        if not product:
            conn.close()
            return False

        stock = int(product[0])

        cursor.execute(
            """
            SELECT quantity
            FROM cart
            WHERE user_id = ?
            AND product_id = ?
            """,
            (
                self.user_id,
                product_id
            )
        )

        item = cursor.fetchone()

        if not item:
            conn.close()
            return False

        current_quantity = int(item[0])

        if current_quantity >= stock:
            conn.close()
            return False

        cursor.execute(
            """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id = ?
            AND product_id = ?
            """,
            (
                self.user_id,
                product_id
            )
        )

        conn.commit()
        conn.close()

        return True
    def decrease_quantity(self, product_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE cart
            SET quantity = quantity - 1
            WHERE user_id = ?
            AND product_id = ?
            AND quantity > 1
            """,
            (
                self.user_id,
                product_id
            )
        )

        affected = cursor.rowcount

        conn.commit()
        conn.close()

        return affected > 0