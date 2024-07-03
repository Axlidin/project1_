from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import ADMINS
from keyboards.default.main_menu import mainMenu, AdminMain_menu
from loader import dp, bot, db


class HamyonState(StatesGroup):
    waiting_for_card_number = State()


@dp.message_handler(text="🗂 Hamyonlar")
async def Hamyonlar_function(message: types.Message):
    tg_id = message.from_user.id
    hamyonim = await db.see_hamyonlar(tg_id)

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ UZCARD/HUMO", callback_data=f"humouzcard"),
        InlineKeyboardButton(text="➕ Betmoon", callback_data=f"betmoon"))
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ Linebet", callback_data=f"linebet"),
        InlineKeyboardButton(text="➕ 1xbet", callback_data=f"1xbet"))
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ Melbet", callback_data=f"melbet"),
        InlineKeyboardButton(text="⬅️ Chiqish", callback_data=f"back"))

    msg = (f"🔖UZCARD/HUMO\n<code>{hamyonim.get('humouzcard', 'Kiritilmagan')}</code>\n"
           f"🔖Betmoon\n<code>{hamyonim.get('betmoon', 'Kiritilmagan')}</code>\n"
           f"🔖Linebet\n<code>{hamyonim.get('linebet', 'Kiritilmagan')}</code>\n"
           f"🔖1xbet\n<code>{hamyonim.get('1xbet', 'Kiritilmagan')}</code>\n"
           f"🔖Melbet\n<code>{hamyonim.get('melbet', 'Kiritilmagan')}</code>\n"
           )

    await message.answer(msg, reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'back')
async def back_to_main_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.delete()
    tg_id = callback_query.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == int(ADMINS[0]):
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)


@dp.callback_query_handler(lambda c: c.data in ["humouzcard", "betmoon", "linebet", "1xbet", "melbet"])
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.update_data(card_type=callback_query.data)
    if callback_query.data == "humouzcard":
        await callback_query.message.edit_text("Iltimos, karta raqamini kiriting (16 ta raqam):")
    else:
        await callback_query.message.edit_text("Iltimos, qayta kiriting (9 tadan ko'p belgi):")
    await HamyonState.waiting_for_card_number.set()


@dp.message_handler(state=HamyonState.waiting_for_card_number)
async def process_card_number(message: types.Message, state: FSMContext):
    card_number = message.text.strip()
    data = await state.get_data()
    card_type = data.get('card_type')

    if card_type == "humouzcard":
        if not (card_number.isdigit() and len(card_number) == 16):
            await message.answer("UZCARD/HUMO karta raqami noto'g'ri. Iltimos, 16 ta raqam kiriting:")
            return
    else:
        if not (card_number.isdigit() and len(card_number) >= 9):
            await message.answer("Karta raqami noto'g'ri. Iltimos, qayta kiriting (9 tadan ko'p belgi):")
            return

    tg_id = message.from_user.id
    await db.add_hamyon(tg_id, card_type, int(card_number))
    await message.answer("Karta muvaffaqiyatli qo'shildi.")

    hamyonim = await db.see_hamyonlar(tg_id)
    msg = (f"🔖UZCARD/HUMO\n<code>{hamyonim.get('humouzcard', 'Kiritilmagan')}</code>\n"
           f"🔖Betmoon\n<code>{hamyonim.get('betmoon', 'Kiritilmagan')}</code>\n"
           f"🔖Linebet\n<code>{hamyonim.get('linebet', 'Kiritilmagan')}</code>\n"
           f"🔖1xbet\n<code>{hamyonim.get('1xbet', 'Kiritilmagan')}</code>\n"
           f"🔖Melbet\n<code>{hamyonim.get('melbet', 'Kiritilmagan')}</code>\n"
           )
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ UZCARD/HUMO", callback_data=f"humouzcard"),
        InlineKeyboardButton(text="➕ Betmoon", callback_data=f"betmoon"))
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ Linebet", callback_data=f"linebet"),
        InlineKeyboardButton(text="➕ 1xbet", callback_data=f"1xbet"))
    inline_keyboard.add(
        InlineKeyboardButton(text="➕ Melbet", callback_data=f"melbet"),
        InlineKeyboardButton(text="⬅️ Chiqish", callback_data=f"back"))

    await message.answer(msg, reply_markup=inline_keyboard)
    await state.finish()
