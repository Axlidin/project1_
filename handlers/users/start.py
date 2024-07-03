from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main_menu import AdminMain_menu, mainMenu
from loader import dp, bot, db

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    tg_id = message.from_user.id
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 2139896417 or tg_id == checkid:
        await message.answer(f"Assalomu alaykum admin: {message.from_user.full_name}",
                             reply_markup=AdminMain_menu)
    else:
        db_user = await db.see_users(tg_id=tg_id)
        if db_user:
            await message.answer(f"Salom, {message.from_user.full_name}!",
                                 reply_markup=mainMenu)
        else:
            start_command = message.text
            referal_id = str(start_command[7:])
            if str(referal_id) != "":
                if str(referal_id) != str(tg_id):
                    await db.add_referal_id(telegram_id=int(tg_id), referal_id=int(referal_id))
                    try:
                        await bot.send_message(int(referal_id), "sizning havolangiz orqali yangi foydalanuvchi ro'yxatdan o'tdi")
                    except:
                        pass
                else:
                    await bot.send_message(tg_id, "Iltimos, o'zingizning havolangiz orqali ro'yxatdan o'ting.")
            else:
                await db.add_referal_id(telegram_id=int(tg_id))
