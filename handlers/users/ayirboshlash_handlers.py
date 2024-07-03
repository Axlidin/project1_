from datetime import datetime

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.dispatcher import FSMContext
from data.config import ADMINS, CHANNELS
from keyboards.default.main_menu import mainMenu, AdminMain_menu
from keyboards.inline.allow_post import create_post_keyboard, post_callbackData
from keyboards.inline.kirishqismi import choose_give_keyboards, choose_get_keyboards
from loader import dp, bot, db
from states.almashish_state import HamyonState_buy
now = datetime.now()
vaqt = now.strftime("%Y.%m.%d %H:%M:%S")

@dp.callback_query_handler(lambda c: c.data == 'choose:exit_give', state=HamyonState_buy)
async def exit_card_changeState(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.finish()
    tg_id = callback_query.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 2139896417:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)


@dp.message_handler(text="🛑 Chiqish", state=HamyonState_buy)
async def cancel_price(message: types.Message, state=FSMContext):
    await state.finish()
    tg_id = message.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 2139896417:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)

@dp.message_handler(text="🔄 Almashtirish")
async def ayirboshlash_function(message: types.Message):
    msg = "<b>⏫Berish valyutalarini tanlang</b>"
    await message.answer(msg, reply_markup=await choose_give_keyboards())
    await HamyonState_buy.next()

@dp.callback_query_handler(state=HamyonState_buy.choose_kirish)
async def process_card_change_kirish(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id
    action = callback_query.data.split('_')[1]
    card_type = callback_query.data.split('_')[0]
    card_type = card_type.split(':')[1]
    checkhamyon = await db.see_my_hamyonlar(tg_id, card_type)
    if not checkhamyon:
        await callback_query.answer("Sizda bunday hamyon qo'shilmagan", show_alert=True)
        return
    if action == 'give':
        await state.update_data(
            {
                "card_type": card_type,
                "action": action
            },
        )
        await callback_query.message.edit_text("<b>⏬Olish valyutalarini tanlang</b>")
        await callback_query.message.edit_reply_markup(reply_markup=await choose_get_keyboards())
        await HamyonState_buy.next()

@dp.callback_query_handler(state=HamyonState_buy.choose_chiqish)
async def process_card_change_chiqish(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id
    action = callback_query.data.split('_')[1]
    if action == 'get':
        card_type = callback_query.data.split('_')[0]
        card_type = card_type.split(':')[1]
        secon_card = card_type
        checkhamyon = await db.see_my_hamyonlar(tg_id, card_type)
        if not checkhamyon:
            await callback_query.answer("Sizda bunday hamyon qo'shilmagan", show_alert=True)
            return
        data = await state.get_data()
        first_card = data.get("card_type")
        if first_card == secon_card:
            await callback_query.answer("Bunday amalni bajarib bo'lmaydi", show_alert=True)
            return
        await state.update_data(
            {
                "first_card": first_card,
                "secon_card": secon_card
            },
        )
        result1 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=first_card)
        result2 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=secon_card)
        msg = (f"<b>Almashuv:</b>\n🔀{result1['hamyon_nomi'].upper()}➡️{result2['hamyon_nomi'].upper()}\n"
               f"Berish: {result1['hamyon_nomi'].upper()}\nOlish: ️{result2['hamyon_nomi'].upper()}\n"
               f"{result1['hamyon_nomi'].upper()}: {result1['card_number']}\n"
               f"{result2['hamyon_nomi'].upper()}: ️{result2['card_number']}\n")
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        inline_keyboard.add(
        InlineKeyboardButton(text="🇺🇿 Pul miqdorini UZS'da kiriting", callback_data="price"))
        inline_keyboard.add(
            InlineKeyboardButton(text="⬅️ Chiqish", callback_data="exit_give"))
        message_id = await callback_query.message.edit_text(msg, reply_markup=inline_keyboard)
        await HamyonState_buy.price.set()

@dp.callback_query_handler(lambda c: c.data == 'price', state=HamyonState_buy)
async def price_card_change(callback_query: types.CallbackQuery, state=FSMContext):
    msg = (f"Berish miqdorini UZS' da kiriting\n"
           f"<b>Minimal: 5000.00 UZS\n"
           f"Maximal: 2000000.00 UZS</b>\n\n"
            )
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 Chiqish")
    await callback_query.message.edit_reply_markup()
    await callback_query.message.edit_text(msg)
    await callback_query.message.answer("Bekor qilish uchun pastdagi tugmani bosing", reply_markup=Mk)

@dp.message_handler(state=HamyonState_buy.price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        pul = float(message.text)
    except ValueError:
        await message.answer("Raqam kiritishingiz kerak. Qaytadan urinib ko'ring.")
        return
    if pul < 5000 or pul > 2000000:
        await message.answer("Kiritilgan miqdor belgilangan cheklovdan kam yoki ko'p. Qaytadan urinib ko'ring.")
        return
    tg_id = message.from_user.id
    pul = float(message.text)
    await state.update_data(
        {
            "pul": pul,
        },
    )
    data = await state.get_data()
    first_card = data.get("first_card")
    secon_card = data.get("secon_card")
    result1 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=first_card)
    result2 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=secon_card)
    melbet_1xbet = "9860340103483830"
    betmoon_linbet = "5614683517974804"

    msg = (f"<b>⚠ Ogohlantiramiz! Begona kartadan to'lov qilmang, karta faqat o'zingizga tegishli bo'lishi "
           f"kerak.\nBEGONA SHAXSLAR KARTASIDAN TO'LOV QILSANGIZ 100% TO'LOVINGIZ YO'QOTILADI.\n"
           f"Operator sizdan to'lov chekini so'rashi mumkin.\n\n"
           f"♻️ Sizning almashuv buyurtmangiz:\n\n"
           f"🔀{result1['hamyon_nomi'].upper()}➡️{result2['hamyon_nomi'].upper()}\n"
           f"Berish: {pul}\n"
           f"{result1['hamyon_nomi'].upper()}: {result1['card_number']}\n"
           f"{result2['hamyon_nomi'].upper()}: ️{result2['card_number']}\n</b>"
           )
    xabar = ""
    if secon_card in ["betmoon", "linebet"]:
        xabar = f"<code>{betmoon_linbet}</code>\n"
    elif secon_card in ["1xbet", "melbet"]:
        xabar = f"<code>{melbet_1xbet}</code>\n "
    xabar += (f"👆 Ko'chirib oling!\n\n"
              f"Mobil qurulmangizda bor to'lov tizimi orqali to'lov miqdorini to'lang")
    await message.answer(xabar)
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="🧾 Checkni yuborish", callback_data="send_check"))
    inline_keyboard.add(
        InlineKeyboardButton(text="⬅️ Chiqish", callback_data="exit_give"))
    await message.answer(msg, reply_markup=inline_keyboard)
    await HamyonState_buy.check_photo.set()

@dp.callback_query_handler(lambda c: c.data == 'exit_give', state=HamyonState_buy)
async def exit_send_check(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.finish()
    tg_id = callback_query.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 2139896417:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)


@dp.callback_query_handler(text='send_check', state=HamyonState_buy.check_photo)
async def send_check(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer("To'lov qilgan checkingizni yuboring.")

@dp.message_handler(content_types=types.ContentType.PHOTO, state=HamyonState_buy.check_photo)
async def process_price_photo(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 2139896417:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)
    mention = message.from_user.get_mention()
    photo = message.photo[-1].file_id
    data = await state.get_data()
    first_card = data.get("first_card")
    secon_card = data.get("secon_card")
    pul = data.get("pul")
    result1 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=first_card)
    result2 = await db.see_my_hamyonlar(tg_id=tg_id, hamyon_nomi=secon_card)
    text = (f"<b>👤Foydalanuvchi: {message.from_user.full_name}\n"
            f"🔀{result1['hamyon_nomi'].upper()}: ➡️{result2['hamyon_nomi'].upper()}\n"
            f"Berish: {pul}\n"
            f"{result1['hamyon_nomi'].upper()}: {result1['card_number']}\n"
            f"{result2['hamyon_nomi'].upper()}: ️{result2['card_number']}\n"
            f"♻️ Pul ayirboshlash\n"
            f"📝 {vaqt}\n</b>"
           )
    message_to_channel_photo = await bot.send_photo(
        chat_id=CHANNELS[1],
        photo=photo,
        caption=text,
        parse_mode='HTML'
    )
    await bot.edit_message_reply_markup(
        chat_id=CHANNELS[1],
        message_id=message_to_channel_photo.message_id,
        reply_markup= await create_post_keyboard(chat_id=tg_id, message_id=message_to_channel_photo.message_id)
    )

    await state.finish()


@dp.callback_query_handler(post_callbackData.filter(action='allow'))
async def let_to_print(call: CallbackQuery):
    tg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[2]
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    msg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[-1]
    await bot.send_message(tg_id, "Admin to'lovni tasdiqladi.")
    await call.answer("Siz to'lovni tasdiqladingiz.", show_alert=True)
    target_channel = CHANNELS[0]
    await call.message.edit_reply_markup()
    new_caption = call.message.caption + (f"\n<b>✅ Tasdiqlangan"
                                          f"\n📝 {vaqt}</b>")
    await bot.send_photo(
        chat_id=target_channel,
        photo=call.message.photo[-1].file_id,
        caption=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )
    await bot.edit_message_caption(
        chat_id=CHANNELS[1],
        message_id=msg_id,
        caption=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )
    new_caption = call.message['caption'].split('\n')
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y.%m.%d %H:%M:%S")
    allowed_time = str(current_time_str)
    status = "✅ Tasdiqlangan"
    if new_caption:
        try:
            await db.add_SuperAdmin_allowe_msg(
                username=new_caption[0].split(': ')[1],
                telegram_id=tg_id,
                karta1=new_caption[3].split(':')[0],
                karta1_num=new_caption[3].split(': ')[1],
                karta2=new_caption[4].split(':')[0],
                karta2_num=new_caption[4].split(': ')[1],
                send_time=new_caption[6],
                allowed_time=allowed_time,
                amoun_money=new_caption[2].split(': ')[1],
                amaliyot_type=new_caption[5],
                status=status
            )
        except Exception as e:
            pass


@dp.callback_query_handler(post_callbackData.filter(action='cancel'))
async def cancel_to_print(call: CallbackQuery):
    await call.answer("Siz to'lovni tasdiqlamadingiz", show_alert=True)
    tg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[2]
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    msg_id = call.message.reply_markup.inline_keyboard[0][0]['callback_data'].split(':')[-1]
    await bot.send_message(tg_id, "Admin to'lovni rad etdi.")
    new_caption = call.message.caption + (f"\n<b>❌ Bekor qilingan"
                                          f"\n📝 {vaqt}</b>")
    await bot.edit_message_caption(
        chat_id=CHANNELS[1],
        message_id=msg_id,
        caption=f"<b>{new_caption}</b>",
        parse_mode='HTML'
    )