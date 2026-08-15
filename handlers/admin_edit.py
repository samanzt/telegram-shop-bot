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
from config import ADMIN_ID


EDIT_NAME, EDIT_DESCRIPTION, EDIT_PRICE, EDIT_STOCK, EDIT_PHOTO = range(5)


# ==========================================
# شروع ویرایش محصول
# ==========================================

async def start_edit_product(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        return ConversationHandler.END

    await query.answer()

    try:
        product_id = int(
            query.data.split("_")[2]
        )

    except (ValueError, IndexError):
        await query.message.reply_text(
            "❌ شناسه محصول نامعتبر است."
        )

        return ConversationHandler.END

    product = ProductService.get_product(
        product_id
    )

    if not product:
        await query.message.reply_text(
            "❌ محصول پیدا نشد."
        )

        return ConversationHandler.END

    context.user_data.clear()

    context.user_data["edit_product_id"] = product_id

    await query.message.reply_text(
        "نام جدید محصول را وارد کنید\n\n"
        "برای لغو عملیات /cancel را ارسال کنید"
    )

    return EDIT_NAME


# ==========================================
# نام جدید
# ==========================================

async def edit_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["edit_name"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "توضیحات جدید محصول را وارد کنید:"
    )

    return EDIT_DESCRIPTION


# ==========================================
# توضیحات جدید
# ==========================================

async def edit_description(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["edit_description"] = (
        update.message.text.strip()
    )

    await update.message.reply_text(
        "قیمت جدید محصول را وارد کنید:"
    )

    return EDIT_PRICE


# ==========================================
# قیمت جدید
# ==========================================

async def edit_price(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        price = int(
            update.message.text
        )

        if price < 0:
            raise ValueError

    except ValueError:

        await update.message.reply_text(
            "❌ قیمت نامعتبر است.\n"
            "لطفاً فقط یک عدد وارد کنید."
        )

        return EDIT_PRICE

    context.user_data["edit_price"] = price

    await update.message.reply_text(
        "موجودی جدید محصول را وارد کنید:"
    )

    return EDIT_STOCK


# ==========================================
# موجودی جدید
# ==========================================

async def edit_stock(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        stock = int(
            update.message.text
        )

        if stock < 0:
            raise ValueError

    except ValueError:

        await update.message.reply_text(
            "❌ تعداد موجودی نامعتبر است.\n"
            "لطفاً فقط یک عدد وارد کنید."
        )

        return EDIT_STOCK

    context.user_data["edit_stock"] = stock

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⏭ بدون تغییر عکس",
                callback_data="no_photo_edit"
            )
        ]
    ])

    await update.message.reply_text(
        "عکس جدید محصول را ارسال کنید 📷\n\n"
        "اگر نمی‌خواهید عکس تغییر کند، "
        "دکمه «⏭ بدون تغییر عکس» را بزنید.",
        reply_markup=keyboard
    )

    return EDIT_PHOTO


# ==========================================
# عکس جدید
# ==========================================

async def edit_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    product_id = context.user_data.get(
        "edit_product_id"
    )

    if not product_id:
        await update.message.reply_text(
            "❌ اطلاعات ویرایش پیدا نشد."
        )

        context.user_data.clear()

        return ConversationHandler.END

    old_product = ProductService.get_product(
        product_id
    )

    if not old_product:

        if update.callback_query:
            await update.callback_query.message.reply_text(
                "❌ محصول پیدا نشد."
            )

        else:
            await update.message.reply_text(
                "❌ محصول پیدا نشد."
            )

        context.user_data.clear()

        return ConversationHandler.END

    # --------------------------------------
    # بدون تغییر عکس
    # --------------------------------------

    if update.callback_query:

        query = update.callback_query

        await query.answer()

        if query.data != "no_photo_edit":
            return EDIT_PHOTO

        photo = old_product["photo"]

        await query.edit_message_reply_markup(
            reply_markup=None
        )

        ProductService.update_product(
            product_id,
            context.user_data["edit_name"],
            context.user_data["edit_description"],
            context.user_data["edit_price"],
            context.user_data["edit_stock"],
            photo
        )

        await query.message.reply_text(
            "محصول با موفقیت ویرایش شد ✅"
        )

        context.user_data.clear()

        return ConversationHandler.END

    # --------------------------------------
    # عکس جدید
    # --------------------------------------

    if update.message and update.message.photo:

        photo = update.message.photo[-1].file_id

        ProductService.update_product(
            product_id,
            context.user_data["edit_name"],
            context.user_data["edit_description"],
            context.user_data["edit_price"],
            context.user_data["edit_stock"],
            photo
        )

        await update.message.reply_text(
            "محصول با موفقیت ویرایش شد ✅"
        )

        context.user_data.clear()

        return ConversationHandler.END

    # --------------------------------------
    # ورودی نامعتبر
    # --------------------------------------

    await update.message.reply_text(
        "لطفاً عکس محصول را ارسال کنید 📷\n"
        "یا دکمه «⏭ بدون تغییر عکس» را بزنید."
    )

    return EDIT_PHOTO


# ==========================================
# لغو ویرایش
# ==========================================

async def cancel_edit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.clear()

    await update.message.reply_text(
        "ویرایش لغو شد ❌"
    )

    return ConversationHandler.END