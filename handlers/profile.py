from telegram import Update
from telegram.ext import ContextTypes

from models.user import User


async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    user = User.get_by_id(user_id)


    if not user:
        await update.message.reply_text(
            "اطلاعات شما پیدا نشد ❌"
        )
        return

    text = (
        f"👤 حساب کاربری\n\n"
        f"نام کاربری: {user[2]}\n"
        f"آیدی تلگرام: {user[1]}"
    )


    await update.message.reply_text(text)