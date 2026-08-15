from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database.connection import get_connection
from keyboards.admin import (
    admin_menu,
    order_status_keyboard,
    orders_menu,
    product_manage_button,
)
from keyboards.user import main_menu
from models.order import Order
from services.order_service import OrderService
from services.product_service import ProductService


STATUS_MAP = {
    "pending": "در انتظار بررسی",
    "accepted": "تایید شده",
    "shipping": "در حال ارسال",
    "completed": "دریافت شده",
    "cancelled": "لغو شده",
}


def get_status_text(status):
    return STATUS_MAP.get(status, status)


def build_order_text(order):

    order_id = order[0]
    total = order[2]
    status = order[3]

    items = Order.get_order_items(order_id)

    text = (
        f"🆔 سفارش #{order_id}\n"
        f"💰 مبلغ: {total:,} تومان\n"
        f"📌 وضعیت: {get_status_text(status)}\n\n"
        f"📦 محصولات:\n"
    )

    for item in items:
        text += (
            f"• {item[0]}: "
            f"{item[1]} عدد\n"
        )

    return text


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "⚙️ پنل مدیریت",
        reply_markup=admin_menu(),
    )


async def show_orders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "📦 مدیریت سفارش‌ها\n\n"
        "بخش مورد نظر را انتخاب کنید:",
        reply_markup=orders_menu(),
    )


async def show_pending_orders(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer()
        return

    await query.answer()

    orders = OrderService.get_pending_orders()

    if not orders:
        await query.message.reply_text(
            "🆕 سفارش در انتظاری وجود ندارد"
        )
        return

    for order in orders:

        order_id = order[0]

        await query.message.reply_text(
            build_order_text(order),
            reply_markup=order_status_keyboard(
                order_id
            ),
        )


async def show_order_history(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer()
        return

    await query.answer()

    orders = OrderService.get_order_history()

    if not orders:
        await query.message.reply_text(
            "📋 تاریخچه سفارش‌ها خالی است."
        )
        return

    for order in orders:
        await query.message.reply_text(
            build_order_text(order)
        )


async def delete_product_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer()
        return

    await query.answer()

    product_id = int(
        query.data.split("_")[2]
    )

    ProductService.delete_product(
        product_id
    )

    await query.message.delete()

    await query.message.chat.send_message(
        "محصول با موفقیت حذف شد ✅"
    )


async def add_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "دسترسی ندارید ❌"
        )
        return

    args = context.args

    if len(args) < 4:
        await update.message.reply_text(
            """
فرمت اشتباه است.

مثال:

/add_product
نام
توضیح
قیمت
موجودی
"""
        )
        return

    name = args[0]
    description = args[1]

    try:
        price = int(args[2])
        stock = int(args[3])
    except ValueError:
        await update.message.reply_text(
            "❌ قیمت و موجودی باید عدد باشند."
        )
        return

    ProductService.create_product(
        name,
        description,
        price,
        stock,
    )

    await update.message.reply_text(
        "محصول اضافه شد ✅"
    )


async def list_products(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        return

    products = ProductService.get_products()

    if not products:
        await update.message.reply_text(
            "هیچ محصولی وجود ندارد."
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

        keyboard = product_manage_button(
            product["id"]
        )

        if product["photo"]:

            await update.message.reply_photo(
                photo=product["photo"],
                caption=text,
                reply_markup=keyboard,
            )

        else:

            await update.message.reply_text(
                text,
                reply_markup=keyboard,
            )


async def change_order_status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer()
        return

    await query.answer()

    data = query.data.split("_")

    if len(data) != 3:
        return

    status = data[1]

    try:
        order_id = int(data[2])
    except ValueError:
        return

    status_actions = {
        "accept": "accepted",
        "shipping": "shipping",
        "complete": "completed",
        "cancel": "cancelled",
    }

    new_status = status_actions.get(status)

    if not new_status:
        return

    OrderService.change_status(
        order_id,
        new_status,
    )

    # سفارش نهایی شده یا لغو شده
    if new_status in {
        "completed",
        "cancelled",
    }:

        await query.edit_message_text(
            f"🆔 سفارش #{order_id}\n"
            f"📌 وضعیت: "
            f"{get_status_text(new_status)}"
        )

        return

    # دریافت وضعیت جدید سفارش
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,),
    )

    order = cursor.fetchone()

    conn.close()

    if not order:
        return

    await query.edit_message_text(
        build_order_text(order),
        reply_markup=order_status_keyboard(
            order_id
        ),
    )


async def back_to_main(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "بازگشت به منوی اصلی",
        reply_markup=main_menu(
            is_admin=True
        ),
    )


async def show_stats(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.effective_user.id != ADMIN_ID:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )
    users = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )
    products = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )
    orders = cursor.fetchone()[0]

    cursor.execute(
        "SELECT SUM(total) FROM orders"
    )
    income = cursor.fetchone()[0] or 0

    conn.close()

    await update.message.reply_text(
        f"""
📊 آمار فروشگاه

👤 کاربران: {users}

📦 محصولات: {products}

🛒 سفارش‌ها: {orders}

💰 فروش کل: {income:,} تومان
"""
    )

