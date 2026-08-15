from telegram import Update
from telegram.ext import ContextTypes


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    print(context.error)

    if isinstance(update, Update):

        try:

            await update.effective_message.reply_text(
                "❌ خطایی رخ داد، دوباره امتحان کنید."
            )

        except Exception:
            pass