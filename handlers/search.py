from telegram import Update
from telegram.ext import ContextTypes

from services.product_service import ProductService
from keyboards.user import product_button


async def search_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🔎 نام محصول را ارسال کنید."
    )

    context.user_data["search"] = True


async def search_result(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("search"):
        return

    context.user_data["search"] = False

    name = update.message.text

    products = ProductService.search(name)

    if not products:

        await update.message.reply_text(
            "محصولی پیدا نشد."
        )

        return

    for product in products:

        product_id = product[0]
        name = product[1]
        description = product[2]
        price = product[3]
        stock = product[4]
        photo = product[5]

        if photo:

            await update.message.reply_photo(
                photo=photo,
                caption=
                f"📦 {name}\n\n"
                f"{description}\n\n"
                f"💰 {price:,} تومان\n"
                f"📦 موجودی: {stock}",
                reply_markup=product_button(product_id)
            )

        else:

            await update.message.reply_text(
                f"📦 {name}\n\n"
                f"{description}\n\n"
                f"💰 {price:,} تومان\n"
                f"📦 موجودی: {stock}",
                reply_markup=product_button(product_id)
            )