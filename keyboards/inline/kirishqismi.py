from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
choose_buttons = CallbackData('choose', 'action')


async def choose_give_keyboards():
    choose_keyboard_give = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(text='⏫ Uzcard/Humo', callback_data=choose_buttons.new(action='humouzcard_give')),
        ],
        [
            InlineKeyboardButton(text='⬅️ Chiqish',callback_data=choose_buttons.new(action='exit_give')),
        ],
            ])
    return choose_keyboard_give

async def choose_get_keyboards():
    choose_keyboard_get = InlineKeyboardMarkup(
        inline_keyboard=[
        [
            InlineKeyboardButton(text='⏬ Melbet', callback_data=choose_buttons.new(action='melbet_get')),
            InlineKeyboardButton(text='⏬ Betmoon', callback_data=choose_buttons.new(action='betmoon_get')),
        ],
        [
            InlineKeyboardButton(text='⏬ Linebet', callback_data=choose_buttons.new(action='linebet_get')),
            InlineKeyboardButton(text='⏬ 1xbet', callback_data=choose_buttons.new(action='1xbet_get')),
        ],
        [
            InlineKeyboardButton(text='⬅️ Chiqish',callback_data=choose_buttons.new(action='exit_give')),
        ],
            ])
    return choose_keyboard_get


choose_keyboard_get = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💳 Melbet', callback_data='melbet_pulyech'),
            InlineKeyboardButton(text='💳 Betmoon', callback_data='betmoon_pulyech'),
        ],
        [
            InlineKeyboardButton(text='💳 Linebet', callback_data='linebet_pulyech'),
            InlineKeyboardButton(text='💳 1xbet', callback_data='1xbet_pulyech'),
        ],
        [
            InlineKeyboardButton(text='⬅️ Chiqish', callback_data='exit_pulyech'),
        ],
    ]
)