from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


# ==========================================
# منوی اصلی ادمین
# ==========================================

def admin_menu():

    keyboard = [

        [
            KeyboardButton("➕ افزودن محصول"),
            KeyboardButton("📋 لیست محصولات")
        ],

        [
            KeyboardButton("📦 سفارش‌ها"),
            KeyboardButton("📊 آمار")
        ],

        [
            KeyboardButton("🔙 بازگشت")
        ]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# ==========================================
# مدیریت محصول
# ==========================================

def product_manage_button(product_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "✏️ ویرایش محصول",
                callback_data=f"edit_product_{product_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "🗑 حذف محصول",
                callback_data=f"delete_product_{product_id}"
            )
        ]

    ]

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================
# منوی سفارش‌ها
# ==========================================

def orders_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🆕 سفارش‌های در انتظار",
                callback_data="admin_pending_orders"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 تاریخچه سفارش‌ها",
                callback_data="admin_order_history"
            )
        ]

    ]

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================
# دکمه‌های وضعیت سفارش
# ==========================================

def order_status_keyboard(order_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ تایید سفارش",
                callback_data=f"status_accept_{order_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "🚚 ارسال شد",
                callback_data=f"status_shipping_{order_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "📦 دریافت شد",
                callback_data=f"status_complete_{order_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ لغو سفارش",
                callback_data=f"status_cancel_{order_id}"
            )
        ]

    ]

    return InlineKeyboardMarkup(
        keyboard
    )


# ==========================================
# دکمه لغو
# ==========================================

def cancel_button():

    keyboard = [
        [
            KeyboardButton("❌ لغو")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )