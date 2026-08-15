from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from services.product_service import ProductService


NAME, DESCRIPTION, PRICE, STOCK, PHOTO = range(5)


# ==========================================
# شروع افزودن محصول
# ==========================================

async def start_add_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "نام محصول را وارد کنید\n\n"
        "برای لغو عملیات /cancel را ارسال کنید"
    )

    return NAME


# ==========================================
# دریافت نام
# ==========================================

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["name"] = update.message.text.strip()

    await update.message.reply_text(
        "توضیحات محصول را وارد کنید:"
    )

    return DESCRIPTION


# ==========================================
# دریافت توضیحات
# ==========================================

async def get_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["description"] = update.message.text.strip()

    await update.message.reply_text(
        "قیمت محصول را وارد کنید:"
    )

    return PRICE


# ==========================================
# دریافت قیمت
# ==========================================

async def get_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        price = int(update.message.text)

        if price < 0:
            raise ValueError

    except ValueError:

        await update.message.reply_text(
            "❌ قیمت نامعتبر است.\n"
            "لطفاً فقط عدد وارد کنید."
        )

        return PRICE

    context.user_data["price"] = price

    await update.message.reply_text(
        "تعداد موجودی را وارد کنید:"
    )

    return STOCK


# ==========================================
# دریافت موجودی
# ==========================================

async def get_stock(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        stock = int(update.message.text)

        if stock < 0:
            raise ValueError

    except ValueError:

        await update.message.reply_text(
            "❌ تعداد موجودی نامعتبر است.\n"
            "لطفاً فقط یک عدد وارد کنید."
        )

        return STOCK

    context.user_data["stock"] = stock

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⏭ بدون عکس",
                callback_data="no_photo_add"
            )
        ]
    ])

    await update.message.reply_text(
        "عکس محصول را ارسال کنید 📷",
        reply_markup=keyboard
    )

    return PHOTO


# ==========================================
# دریافت عکس
# ==========================================

async def get_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # --------------------------------------
    # بدون عکس
    # --------------------------------------

    if update.callback_query:

        query = update.callback_query

        await query.answer()

        if query.data != "no_photo_add":
            return PHOTO

        photo = None

        await query.edit_message_reply_markup(
            reply_markup=None
        )

        ProductService.create_product(
            context.user_data["name"],
            context.user_data["description"],
            context.user_data["price"],
            context.user_data["stock"],
            photo
        )

        await query.message.reply_text(
            "محصول اضافه شد ✅"
        )

        context.user_data.clear()

        return ConversationHandler.END

    # --------------------------------------
    # دریافت عکس
    # --------------------------------------

    if update.message and update.message.photo:

        photo = update.message.photo[-1].file_id

        ProductService.create_product(
            context.user_data["name"],
            context.user_data["description"],
            context.user_data["price"],
            context.user_data["stock"],
            photo
        )

        await update.message.reply_text(
            "محصول اضافه شد ✅"
        )

        context.user_data.clear()

        return ConversationHandler.END

    # --------------------------------------
    # ورودی نامعتبر
    # --------------------------------------

    await update.message.reply_text(
        "لطفاً عکس محصول را ارسال کنید 📷\n"
        "یا دکمه «⏭ بدون عکس» را بزنید."
    )

    return PHOTO


# ==========================================
# لغو عملیات
# ==========================================

async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "لغو شد ❌"
    )

    return ConversationHandler.END