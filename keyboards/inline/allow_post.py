from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

post_callbackData = CallbackData('create_post', 'action', 'chat_id', 'message_id')
async def create_post_keyboard(chat_id, message_id):
    post_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🆗 tasdiqlash', callback_data=post_callbackData.new(action='allow', chat_id=chat_id, message_id=message_id)),
                InlineKeyboardButton(text='❌ rad etish', callback_data=post_callbackData.new(action='cancel', chat_id=chat_id, message_id=message_id))
            ]
        ]
    )
    return post_keyboard


pulyechish_callbackData = CallbackData('pulyechish', 'action', 'chat_id', 'message_id')

async def pulyechish_keyboard(chat_id, message_id):
    post_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🆗 Tasdiqlash', callback_data=pulyechish_callbackData.new(action='allow', chat_id=chat_id, message_id=message_id)),
                InlineKeyboardButton(text='❌ Rad etish', callback_data=pulyechish_callbackData.new(action='cancel', chat_id=chat_id, message_id=message_id))
            ]
        ]
    )
    return post_keyboard

pulyechish_kartadan_callbackData = CallbackData('pulyechish', 'action', 'chat_id', 'message_id')

async def pulyechish_kartadan_keyboard(chat_id, message_id):
    post_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🆗 Tasdiqlash', callback_data=pulyechish_callbackData.new(action='allow', chat_id=chat_id, message_id=message_id)),
                InlineKeyboardButton(text='❌ Rad etish', callback_data=pulyechish_callbackData.new(action='cancel', chat_id=chat_id, message_id=message_id))
            ]
        ]
    )
    return post_keyboard
