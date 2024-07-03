import json
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from data.config import ADMINS, CHANNELS
from keyboards.default.main_menu import mainMenu, AdminMain_menu
from keyboards.inline.allow_post import pulyechish_keyboard, pulyechish_callbackData, pulyechish_kartadan_keyboard
from keyboards.inline.kirishqismi import choose_keyboard_get
from loader import dp, bot, db
from states.almashish_state import PulYechish
from datetime import datetime
now = datetime.now()
vaqt = now.strftime("%Y.%m.%d %H:%M:%S")
@dp.message_handler(text="👥 Referallar")
async def referallar_function(message: types.Message):
    tg_id = message.from_user.id
    referalim = await db.count_referal_id(tg_id)
    bot_info = await bot.get_me()
    if referalim:
        msg = (f"💵Sizning hisobingiz: {referalim * 500} UZS\n"
               "👥 Do'stlarni taklif qiling va referalingizning birinchi almashuvidan 💰500 UZS daromad oling)\n")
    else:
        msg = (f"💵Sizning hisobingiz: 0 UZS\n"
               "👥 Do'stlarni taklif qiling va referalingizning birinchi almashuvidan 💰500 UZS daromad oling)\n")
    msg += (f"\nhttps://t.me/{bot_info.username}?start={tg_id}\n\n"
            f"Eng kam pul yechish miqdori 5000 UZS so'm")

    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.row(
        InlineKeyboardButton(text="👥 Referallarim", callback_data="referallarim")
    )
    inline_keyboard.row(
        InlineKeyboardButton(text="💸 Pul Yechish", callback_data="pul_yechish"),
        InlineKeyboardButton(text="💸 Pul Yechish: Referaldan", callback_data="pulyechish_referal")
    )
    inline_keyboard.add(
        InlineKeyboardButton(text="⬅️ Chiqish", callback_data="ortga_qaytish")
    )
    await message.answer(msg, reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda c: c.data in ["referallarim", "pulyechish_referal", "ortga"])
async def process_inline_button(callback_query: types.CallbackQuery):
    tg_id = callback_query.from_user.id
    if callback_query.data == "referallarim":
        referalim = await db.count_referal_id(tg_id)
        await callback_query.answer(f"Sizning referallaringiz soni: {referalim}", show_alert=True)
    elif callback_query.data == "pulyechish_referal":
        referalim = await db.count_referal_id(tg_id)
        if referalim * 500 <= 5000:
            hamyonim = await db.see_hamyonlar_humouz(tg_id=tg_id)
            if hamyonim:

                await callback_query.answer("So'rovingiz adminga yuborildi", show_alert=True)
                msg = (f"<b>👤Foydalanuvchi: {callback_query.from_user.full_name}\n"
                       f"Hisobidan pul yechib olmoqchi:\n"
                       f"Hisobidagi pul miqdori: {referalim * 500}\n"
                       f"Karta nomi: {hamyonim['hamyon_nomi'].upper()}\n"
                       f"Karta nomeri:</b><code>{hamyonim['card_number']}</code>\n"
                       f"<b>💸 Pul Yechish: Referaldan\n"
                       f"📝 {vaqt}\n</b>")

                sendmsg = await bot.send_message(
                    chat_id=CHANNELS[1],
                    text=msg,
                    parse_mode='HTML'
                )
                await bot.edit_message_reply_markup(
                    chat_id=CHANNELS[1],
                    message_id=sendmsg.message_id,
                    reply_markup=await pulyechish_keyboard(chat_id=tg_id,
                                                            message_id=sendmsg.message_id)
                )
            else:
                await callback_query.answer("Pul yechish uchun Uzcard/Humo kartalarini qo'shishingiz kerak", show_alert=True)
        else:
            await callback_query.answer("Pul yechish uchun kamida 5000 so'm bo'lishi kerak", show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'ortga_qaytish')
async def ortga_to_main_menu(callback_query: types.CallbackQuery):
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


@dp.callback_query_handler(pulyechish_callbackData.filter(action='allow'))
async def let_to_check(call: CallbackQuery):
    tg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[2]
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    msg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[-1]
    await bot.send_message(tg_id, "Admin to'lovni tasdiqladi.")
    await call.answer("Siz to'lovni tasdiqladingiz.", show_alert=True)
    target_channel = CHANNELS[0]
    await call.message.edit_reply_markup()
    new_caption = call.message.text + (f"\n✅ Tasdiqlangan\n"
                                       f"✅ {vaqt}")
    await bot.send_message(
        chat_id=target_channel,
        text=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )
    await bot.edit_message_text(
        chat_id=CHANNELS[1],
        message_id=msg_id,
        text=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )

@dp.callback_query_handler(pulyechish_callbackData.filter(action='cancel'))
async def cancel_to_check(call: CallbackQuery):
    await call.answer("Siz to'lovni tasdiqlamadingiz", show_alert=True)
    tg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[2]
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    msg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[-1]
    await bot.send_message(tg_id, "Admin to'lovni rad etdi.")
    new_caption = call.message.text + (f"\nHolat: ❌ Bekor qilingan"
                                       f"\n✅ {vaqt}")
    await bot.edit_message_text(
        chat_id=CHANNELS[1],
        message_id=msg_id,
        text=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )

@dp.callback_query_handler(lambda c: c.data == 'pul_yechish')
async def pulyechish_start(callback_query: types.CallbackQuery):
    msg = f"Kerakli karta nomini tanlang."
    await callback_query.message.edit_text(msg, reply_markup=choose_keyboard_get)
    await PulYechish.karta.set()

@dp.callback_query_handler(lambda c: c.data in ["melbet_pulyech", "betmoon_pulyech", "linebet_pulyech", "1xbet_pulyech", "exit_pulyech"], state=PulYechish)
async def pulyechiKeyboardds(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id
    karta = callback_query.data.split('_')[0]
    tg_id = int(tg_id)
    if karta == 'exit':
        await callback_query.message.edit_reply_markup()
        tg_id = int(tg_id)
        checkid = await db.see_SuperAdmin(tg_id)
        if tg_id == int(ADMINS[0]):
            await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
        elif tg_id == checkid:
            await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
        else:
            await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)
        await state.finish()
    else:
        hamyon_nomi = await db.see_my_hamyonlar(tg_id, karta)
        if not hamyon_nomi:
            await callback_query.answer(f"Hamyonlar bo'limiga {karta} karta raqamini qo'shing", show_alert=True)
            return
        await callback_query.message.answer("☑️ Qabul qilish kodini kiriting:")
        await callback_query.message.edit_reply_markup()
        if karta != 'exit':
            await state.update_data(
                {
                    "karta": karta,
                },
            )
            await PulYechish.mahsusKod.set()



@dp.message_handler(state=PulYechish.mahsusKod)
async def mahsusKod(message: types.Message, state: FSMContext):
    kod = message.text
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="🔐 Adminga yuborish", callback_data="send_kod"))
    inline_keyboard.add(
        InlineKeyboardButton(text="⬅️ Chiqish", callback_data="exit_give"))
    await message.answer(f"Maxfiy kodingiz to'g'ri ekanligiga ishonchingiz komilmi?\n"
                         f"Agar kod to'g'ri bo'lsa: <code>{kod}</code>\n"
                         f"Adminga yuborish tugmasini bosing!", reply_markup=inline_keyboard)
    await state.update_data(
        {
            "kod": kod,
        },
    )
    await PulYechish.tasdiqlash.set()

@dp.callback_query_handler(lambda c: c.data == 'exit_give', state=PulYechish.tasdiqlash)
async def exit_give_kod(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("So'rovingiz adminga yuborilmadi", show_alert=True)
    await callback_query.message.edit_reply_markup()
    tg_id = callback_query.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == int(ADMINS[0]):
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'send_kod', state=PulYechish.tasdiqlash)
async def send_kod(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    karta = data.get("karta")
    kod = data.get("kod")
    tg_id = callback_query.from_user.id
    hamyon_nomi = await db.see_my_hamyonlar(tg_id, karta)
    hamyonim = await db.see_hamyonlar_humouz(tg_id=tg_id)

    if not hamyonim:
        await callback_query.answer(f"Hamyonlar bo'limiga {hamyonim['hamyon_nomi']} karta raqamini qo'shing",
                                    show_alert=True)
    else:
        if hamyon_nomi:
            await callback_query.answer("So'rovingiz adminga yuborildi", show_alert=True)
            msg = (
                f"<b>👤Foydalanuvchi: {callback_query.from_user.full_name}</b>\n"
                f"<b>{karta.upper()}dan pul yechib olmoqchi:</b>\n"
                f"<b>Karta nomi:</b> {hamyon_nomi['hamyon_nomi'].upper()}\n"
                f"<b>Karta nomeri:</b> <code>{hamyon_nomi['card_number']}</code>\n"
                f"<b>Humouzcard nomeri:</b> <code>{hamyonim['card_number']}</code>\n"
                f"<b>Mahsus kod:</b> <code>{kod}</code>\n"
                f"<b>💸 Pul Yechish</b>\n"
                f"📝 {vaqt}"
            )

            sendmsg = await bot.send_message(
                chat_id=CHANNELS[1],
                text=msg,
                parse_mode='HTML'
            )
            await bot.edit_message_reply_markup(
                chat_id=CHANNELS[1],
                message_id=sendmsg.message_id,
                reply_markup=await pulyechish_kartadan_keyboard(chat_id=tg_id, message_id=sendmsg.message_id)
            )

        await callback_query.message.edit_reply_markup()

        checkid = await db.see_SuperAdmin(tg_id)
        if tg_id == int(ADMINS[0]) or tg_id == checkid:
            await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
        else:
            await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)
        await state.finish()
