from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from models.user import User
from keyboards.user import main_menu



async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    telegram_id = update.effective_user.id
    name = update.effective_user.first_name

    is_admin = telegram_id == ADMIN_ID


    user = User.get_by_telegram_id(
        telegram_id
    )


    if not user:

        new_user = User(
            telegram_id,
            name
        )

        new_user.save()


        message = "ثبت نام شما انجام شد ✅"


    else:

        message = "درود دوباره👋"



    await update.message.reply_text(
        message + "\n\nبه فروشگاه خوش آمدید 🛒",
        reply_markup=main_menu(is_admin)
    )