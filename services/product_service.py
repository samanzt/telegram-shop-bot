from models.product import Product
from database.connection import get_connection
from rapidfuzz import fuzz


class ProductService:

    @staticmethod
    def create_product(
        name,
        description,
        price,
        stock,
        photo=None
    ):

        product = Product(
            name,
            description,
            price,
            stock,
            photo
        )

        product.save()

    @staticmethod
    def get_products():

        return Product.get_all()

    @staticmethod
    def get_product(product_id):
        return Product.get_by_id(product_id)

    @staticmethod
    def update_product(
        product_id,
        name,
        description,
        price,
        stock,
        photo
    ):

        Product.update(
            product_id,
            name,
            description,
            price,
            stock,
            photo
        )

    @staticmethod
    def delete_product(product_id):

        Product.delete(product_id)

    @staticmethod
    def decrease_stock(
        product_id,
        quantity
    ):

        return Product.decrease_stock(
            product_id,
            quantity
        )

    @staticmethod
    def search(name):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM products
            """
        )

        products = cursor.fetchall()

        conn.close()

        result = []

        for product in products:

            score = fuzz.ratio(
                name.lower(),
                product[1].lower()
            )

            if (
                    score >= 60
                    or
                    name.lower() in product[1].lower()
            ):
                result.append(product)

        result.sort(
            key=lambda p: fuzz.ratio(
                name.lower(),
                p[1].lower()
            ),
            reverse=True
        )

        return result