import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
# Using a simple predicate instead of aiogram's Text filter for compatibility
from dotenv import load_dotenv

# Load environment variables before importing modules that use them
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

from handlers import start_handler, show_clients, callback_handler, text_message_router, import_command, document_handler, import_button_handler, login_command, logout_command

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start_handler, lambda message: (getattr(message, "text", None) or "").strip().startswith("/start"))
dp.message.register(show_clients, lambda message: (getattr(message, "text", None) or "") == "📋 Показать клиентов")
dp.message.register(import_button_handler, lambda message: (getattr(message, "text", None) or "") == "📤 Импорт файла")
dp.message.register(import_command, lambda message: (getattr(message, "text", None) or "").strip().startswith("/import"))
dp.message.register(document_handler, lambda message: getattr(message, 'document', None) is not None)
dp.message.register(login_command, lambda message: (getattr(message, "text", None) or "").strip().startswith("/login"))
dp.message.register(logout_command, lambda message: (getattr(message, "text", None) or "").strip().startswith("/logout"))
dp.callback_query.register(callback_handler)
dp.message.register(text_message_router)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)