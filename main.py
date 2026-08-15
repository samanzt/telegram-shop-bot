from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TOKEN
from database.tables import create_tables

from handlers.admin import (
    add_product,
    admin_panel,
    back_to_main,
    change_order_status,
    delete_product_callback,
    list_products,
    show_order_history,
    show_orders,
    show_pending_orders,
    show_stats,
)
from handlers.admin_conversation import (
    DESCRIPTION,
    NAME,
    PHOTO,
    PRICE,
    STOCK,
    cancel,
    get_description,
    get_name,
    get_photo,
    get_price,
    get_stock,
    start_add_product,
)
from handlers.admin_edit import (
    EDIT_DESCRIPTION,
    EDIT_NAME,
    EDIT_PHOTO,
    EDIT_PRICE,
    EDIT_STOCK,
    cancel_edit,
    edit_description,
    edit_name,
    edit_photo,
    edit_price,
    edit_stock,
    start_edit_product,
)
from handlers.cart import (
    cart_delete,
    cart_minus,
    cart_plus,
    checkout,
    create_order,
    show_cart,
)
from handlers.error import error_handler
from handlers.orders import cancel_order, my_orders
from handlers.profile import profile
from handlers.search import search_product, search_result
from handlers.shop import add_to_cart, show_products
from handlers.start import start


def main():

    # Create database tables
    create_tables()

    # Create bot application
    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # ==================================================
    # Commands
    # ==================================================

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("add_product", add_product)
    )

    app.add_handler(
        CommandHandler("products", show_products)
    )

    app.add_handler(
        CommandHandler("cart", show_cart)
    )

    app.add_handler(
        CommandHandler("order", create_order)
    )

    # ==================================================
    # Add product to cart
    # ==================================================

    app.add_handler(
        CallbackQueryHandler(
            add_to_cart,
            pattern=r"^add_"
        )
    )

    # ==================================================
    # Add product conversation
    # ==================================================

    add_product_conversation = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.TEXT & filters.Regex(
                    r"^➕ افزودن محصول$"
                ),
                start_add_product,
            )
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.COMMAND & filters.Regex(
                        r"^/cancel$"
                    ),
                    cancel,
                ),
                MessageHandler(
                    filters.TEXT,
                    get_name,
                ),
            ],

            DESCRIPTION: [
                MessageHandler(
                    filters.COMMAND & filters.Regex(
                        r"^/cancel$"
                    ),
                    cancel,
                ),
                MessageHandler(
                    filters.TEXT,
                    get_description,
                ),
            ],

            PRICE: [
                MessageHandler(
                    filters.COMMAND & filters.Regex(
                        r"^/cancel$"
                    ),
                    cancel,
                ),
                MessageHandler(
                    filters.TEXT,
                    get_price,
                ),
            ],

            STOCK: [
                MessageHandler(
                    filters.COMMAND & filters.Regex(
                        r"^/cancel$"
                    ),
                    cancel,
                ),
                MessageHandler(
                    filters.TEXT,
                    get_stock,
                ),
            ],

            PHOTO: [
                MessageHandler(
                    filters.COMMAND & filters.Regex(
                        r"^/cancel$"
                    ),
                    cancel,
                ),
                MessageHandler(
                    filters.PHOTO,
                    get_photo,
                ),
                CallbackQueryHandler(
                    get_photo,
                    pattern=r"^no_photo_add$"
                ),
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel,
            ),
            MessageHandler(
                filters.Regex(r"^❌ لغو$"),
                cancel,
            ),
        ],
    )

    app.add_handler(
        add_product_conversation
    )

    # ==================================================
    # Edit product conversation
    # ==================================================

    edit_product_conversation = ConversationHandler(

        entry_points=[
            CallbackQueryHandler(
                start_edit_product,
                pattern=r"^edit_product_"
            )
        ],

        states={

            EDIT_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_name,
                )
            ],

            EDIT_DESCRIPTION: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_description,
                )
            ],

            EDIT_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_price,
                )
            ],

            EDIT_STOCK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_stock,
                )
            ],

            EDIT_PHOTO: [
                MessageHandler(
                    filters.PHOTO,
                    edit_photo,
                ),
                CallbackQueryHandler(
                    edit_photo,
                    pattern=r"^no_photo_edit$"
                ),
            ],
        },

        fallbacks=[
            CommandHandler(
                "cancel",
                cancel_edit,
            ),
            MessageHandler(
                filters.Regex(r"^❌ لغو$"),
                cancel_edit,
            ),
        ],
    )

    app.add_handler(
        edit_product_conversation
    )

    # ==================================================
    # Shop
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^🛒 محصولات$"
            ),
            show_products,
        )
    )

    # ==================================================
    # Cart
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^🛍 سبد خرید$"
            ),
            show_cart,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            checkout,
            pattern=r"^checkout$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cart_plus,
            pattern=r"^cart_plus_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cart_minus,
            pattern=r"^cart_minus_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cart_delete,
            pattern=r"^cart_delete_"
        )
    )

    # ==================================================
    # Admin panel
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^⚙️ پنل مدیریت$"
            ),
            admin_panel,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^📋 لیست محصولات$"
            ),
            list_products,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^📊 آمار$"
            ),
            show_stats,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            delete_product_callback,
            pattern=r"^delete_product_"
        )
    )

    # ==================================================
    # Admin orders
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^📦 سفارش‌ها$"
            ),
            show_orders,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            show_pending_orders,
            pattern=r"^admin_pending_orders$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            show_order_history,
            pattern=r"^admin_order_history$"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            change_order_status,
            pattern=r"^status_"
        )
    )

    # ==================================================
    # User orders
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^📦 سفارش‌های من$"
            ),
            my_orders,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cancel_order,
            pattern=r"^cancel_order_"
        )
    )

    # ==================================================
    # Profile
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^👤 حساب من$"
            ),
            profile,
        )
    )

    # ==================================================
    # Back to main menu
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^🔙 بازگشت$"
            ),
            back_to_main,
        )
    )

    # ==================================================
    # Search
    # ==================================================

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(
                r"^🔎 جستجو$"
            ),
            search_product,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search_result,
        )
    )

    # ==================================================
    # Error handler
    # ==================================================

    app.add_error_handler(
        error_handler
    )

    # Start bot
    app.run_polling()


if __name__ == "__main__":
    main()

