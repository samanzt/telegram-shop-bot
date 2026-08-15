from database.connection import get_connection


class Product:

    def __init__(self, name, description, price, stock, photo=None):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.photo = photo

    def save(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products
            (name, description, price, stock, photo)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.name,
                self.description,
                self.price,
                self.stock,
                self.photo
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_all():

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM products
            ORDER BY id DESC
            """
        )

        products = cursor.fetchall()

        conn.close()

        return products

    @staticmethod
    def get_by_id(product_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM products
            WHERE id = ?
            """,
            (product_id,)
        )

        product = cursor.fetchone()

        conn.close()

        return product

    @staticmethod
    def delete(product_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM products
            WHERE id = ?
            """,
            (product_id,)
        )

        conn.commit()
        conn.close()

    @staticmethod
    def update(product_id, name, description, price, stock, photo):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE products
            SET
                name = ?,
                description = ?,
                price = ?,
                stock = ?,
                photo = ?
            WHERE id = ?
            """,
            (
                name,
                description,
                price,
                stock,
                photo,
                product_id
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def decrease_stock(product_id, quantity):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE products
            SET stock = stock - ?
            WHERE id = ?
            AND stock >= ?
            """,
            (
                quantity,
                product_id,
                quantity
            )
        )

        conn.commit()

        success = cursor.rowcount > 0

        conn.close()

        return success