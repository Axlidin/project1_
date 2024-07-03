from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

from keyboards.default.main_menu import AdminMain_menu, mainMenu
from loader import dp, bot, db
Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Mk.add("🛑 Chiqish")
message_ids = []

async def format_transaction_message(record):
    amaliyot_type = record['amaliyot_type']
    username = record['username']
    karta1 = record['karta1']
    karta1_num = record['karta1_num']
    karta2 = record['karta2']
    karta2_num = record['karta2_num']
    send_time = record['send_time']
    allowed_time = record['allowed_time']
    amoun_money = record['amoun_money']
    status = record['status']
    message = (
        f"<b>👤: {username}\n"
        f"🔀:{karta1}➡️:{karta2}\n"
        f"🔎 Status: {status}\n"
        f"{send_time}\n"
        f"✅: {allowed_time}\n"
        f"📥: {amoun_money} UZS\n"
        f"{amaliyot_type}</b>"
    )
    return message


@dp.message_handler(text="🗳 Amallar tarixi")
async def Statistika_function(message: types.Message):
    tg_id = message.from_user.id
    records = await db.see_SuperAdmin_allowe_msg(tg_id=tg_id)
    await message.answer("<b>Pul ayirboshlash tarixingiz:</b>", reply_markup=Mk)
    for record in records:
        xabar = await format_transaction_message(record)
        msg = await message.answer(xabar)
        message_ids.append(msg.message_id)

@dp.message_handler(text="🛑 Chiqish")
async def cancel_savat(message: types.Message):
    for msg_id in message_ids:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

        except Exception as e:
            pass
    message_ids.clear()
    tg_id = message.from_user.id
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 5419118871:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz Admin.", reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, "Bosh menyuga qaytingiz.", reply_markup=mainMenu)