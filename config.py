import os
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(
    os.getenv("ADMIN_ID")
)
