from telegram import Update
from telegram.ext import ContextTypes

from models.product import Product
from models.cart import Cart

from keyboards.user import product_button



async def show_products(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    products = Product.get_all()


    if not products:

        await update.message.reply_text(
            "فعلا محصولی وجود ندارد."
        )

        return


    for product in products:

        text = (
            f"📦 نام محصول: {product['name']}\n\n"
            f"📝 توضیحات: {product['description']}\n\n"
            f"💰 قیمت: {product['price']:,} تومان\n"
            f"📦 موجودی: {product['stock']}\n"
            f"🆔 شناسه: {product['id']}"
        )


        if product["photo"]:

            await update.message.reply_photo(
                photo=product["photo"],
                caption=text,
                reply_markup=product_button(product["id"])
            )

        else:

            await update.message.reply_text(
                text,
                reply_markup=product_button(product["id"])
            )






async def add_to_cart(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    data = query.data


    product_id = int(
        data.split("_")[1]
    )


    telegram_id = query.from_user.id


    user = Product.get_by_id(product_id)


    if not user:

        await query.edit_message_text(
            "محصول پیدا نشد ❌"
        )

        return


    cart = Cart(telegram_id)


    cart.add_product(
        product_id
    )

    await query.message.reply_text(
        "✅ محصول به سبد خرید اضافه شد."
    )