from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Показать клиентов")],
        [KeyboardButton(text="📤 Импорт файла")],
    ],
    resize_keyboard=True
)
