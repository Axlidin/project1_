from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Almashtirish")
        ],
        [
            KeyboardButton(text="🗂 Hamyonlar"),
            KeyboardButton(text="🗳 Amallar tarixi")
        ],
        [
            KeyboardButton(text="👥 Referallar"),
            KeyboardButton(text="📞 Aloqa"),
        ],

    ], resize_keyboard=True, one_time_keyboard=True
)

AdminMain_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔄 Almashtirish"),
            KeyboardButton(text="📊 Statistika")
        ],
        [
            KeyboardButton(text="🗂 Hamyonlar"),
            KeyboardButton(text="🗳 Amallar tarixi")
        ],
        [
            KeyboardButton(text="👥 Referallar"),
            KeyboardButton(text="📞 Aloqa"),
        ],
        [
            KeyboardButton(text="➕ Superadmin"),
            KeyboardButton(text="Sendpost"),
        ]

    ], resize_keyboard=True, one_time_keyboard=True
)
