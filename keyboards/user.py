from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)



def main_menu(is_admin=False):

    keyboard = [

        [
            KeyboardButton("🛒 محصولات"),
            KeyboardButton("🛍 سبد خرید")
        ],

        [
            KeyboardButton("📦 سفارش‌های من"),
            KeyboardButton("🔎 جستجو")
        ]

    ]
    if is_admin:

        keyboard.append(["⚙️ پنل مدیریت"])


    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )





def checkout_button():

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ ثبت سفارش",
                callback_data="checkout"
            )
        ]

    ]

    return InlineKeyboardMarkup(keyboard)


def product_button(product_id):

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ افزودن به سبد",
                callback_data=f"add_{product_id}"
            )
        ]

    ]


    return InlineKeyboardMarkup(keyboard)




from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def cart_item_keyboard(product_id):

    keyboard = [

        [

            InlineKeyboardButton(
                "➕",
                callback_data=f"cart_plus_{product_id}"
            ),

            InlineKeyboardButton(
                "➖",
                callback_data=f"cart_minus_{product_id}"
            ),

            InlineKeyboardButton(
                "🗑",
                callback_data=f"cart_delete_{product_id}"
            )

        ]

    ]

    return InlineKeyboardMarkup(keyboard)


def cancel_order_button(order_id):

    keyboard = [
        [
            InlineKeyboardButton(
                "❌ لغو سفارش",
                callback_data=f"cancel_order_{order_id}"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def cart_keyboard(products):

    keyboard = []

    for product_id in products:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "➕",
                    callback_data=f"cart_plus_{product_id}"
                ),

                InlineKeyboardButton(
                    "➖",
                    callback_data=f"cart_minus_{product_id}"
                ),

                InlineKeyboardButton(
                    "🗑 حذف",
                    callback_data=f"cart_delete_{product_id}"
                )
            ]
        )


    keyboard.append(
        [
            InlineKeyboardButton(
                "✅ ثبت سفارش",
                callback_data="checkout"
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)