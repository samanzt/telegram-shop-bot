
from telegram import Update
from telegram.ext import ContextTypes
from models.cart import Cart
from keyboards.user import cancel_order_button
from models.order import Order
from services.order_service import OrderService


def translate_status(status):

    statuses = {
        "pending": "در انتظار بررسی",
        "accepted": "تایید شده",
        "shipping": "در حال ارسال",
        "completed": "دریافت شده",
        "cancelled": "لغو شده"
    }

    return statuses.get(status, status)

    return statuses.get(status, status)


async def my_orders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id


    orders = OrderService.get_user_orders(user_id)

    if not orders:
        await update.message.reply_text(
            "شما هنوز سفارش فعالی ندارید ❌"
        )
        return

    for order in orders:

        order_id = order[0]
        total = order[2]
        status = translate_status(order[3])

        items = Order.get_order_items(order_id)

        text = (
            f"🆔 کد پیگیری: #{order_id}\n"
            f"💰 مبلغ: {total:,} تومان\n"
            f"📌 وضعیت: {status}\n\n"
            f"📦 محصولات:\n"
        )

        for item in items:
            text += f"• {item[0]}: {item[1]} عدد\n"

        keyboard = None

        if order[3] == "pending":
            keyboard = cancel_order_button(order_id)
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )


async def cancel_order(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    order_id = int(
        query.data.split("_")[2]
    )

    result = OrderService.cancel_order(order_id)

    if result:

        await query.edit_message_text(
            "❌ سفارش لغو شد"
        )

    else:

        await query.edit_message_text(
            "امکان لغو این سفارش وجود ندارد."
        )


