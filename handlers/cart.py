from telegram import Update
from telegram.ext import ContextTypes
from keyboards.user import checkout_button
from models.cart import Cart
from services.order_service import OrderService
from keyboards.user import cart_keyboard


async def show_cart(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id

    cart = Cart(telegram_id)

    items = cart.get_items()


    if not items:

        await update.message.reply_text(
            "سبد خرید شما خالی است 🛒"
        )

        return


    text = "🛒 سبد خرید شما:\n\n"

    products = []


    for item in items:

        product_id = item[0]
        name = item[1]
        price = item[2]
        quantity = item[3]

        products.append(product_id)

        text += (
            f"📦 {name}\n"
            f"💰 قیمت: {price:,} تومان\n"
            f"🔢 تعداد: {quantity}\n\n"
        )


    text += (
        f"💰 مجموع سبد خرید: "
        f"{cart.get_total_price():,} تومان"
    )


    await update.message.reply_text(
        text,
        reply_markup=cart_keyboard(products)
    )


async def create_order(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id


    order_id = OrderService.create_order(
        telegram_id
    )


    if not order_id:

        await update.message.reply_text(
            "سبد خرید شما خالی است ❌"
        )

        return


    await update.message.reply_text(
        f"سفارش شما ثبت شد ✅\n"
        f"شماره سفارش: {order_id}"
    )

async def checkout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    user_id = query.from_user.id


    order_id = OrderService.create_order(
        user_id
    )


    if not order_id:

        await query.edit_message_text(
            "سبد خرید خالی است ❌"
        )

        return


    await query.edit_message_text(
        f"سفارش ثبت شد ✅\n"
        f"شماره سفارش: {order_id}"
    )


async def update_cart_message(query, cart):

    items = cart.get_items()


    if not items:

        await query.edit_message_text(
            "سبد خرید شما خالی است 🛒"
        )

        return


    text = "🛒 سبد خرید شما:\n\n"

    products = []


    for item in items:

        product_id = item[0]
        name = item[1]
        price = item[2]
        quantity = item[3]

        products.append(product_id)

        text += (
            f"📦 {name}\n"
            f"💰 قیمت: {price:,} تومان\n"
            f"🔢 تعداد: {quantity}\n\n"
        )


    text += (
        f"💰 مجموع سبد خرید: "
        f"{cart.get_total_price():,} تومان"
    )


    await query.edit_message_text(
        text,
        reply_markup=cart_keyboard(products)
    )


async def cart_plus(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()


    product_id = int(
        query.data.split("_")[2]
    )


    cart = Cart(
        query.from_user.id
    )


    result = cart.increase_quantity(
        product_id
    )


    if result:

        await update_cart_message(
            query,
            cart
        )

    else:

        await query.answer(
            "❌ موجودی کافی نیست",
            show_alert=True
        )



async def cart_minus(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()


    product_id = int(
        query.data.split("_")[2]
    )


    cart = Cart(
        query.from_user.id
    )


    result = cart.decrease_quantity(
        product_id
    )


    if result:

        await update_cart_message(
            query,
            cart
        )

    else:

        await query.answer(
            "❌ تعداد کمتر از ۱ نمی‌شود",
            show_alert=True
        )



async def cart_delete(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()


    product_id = int(
        query.data.split("_")[2]
    )


    cart = Cart(
        query.from_user.id
    )


    cart.remove_product(
        product_id
    )


    await update_cart_message(
        query,
        cart
    )