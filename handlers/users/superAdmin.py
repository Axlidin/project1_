from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from keyboards.default.main_menu import AdminMain_menu, mainMenu
from loader import dp, bot, db

class AddSuperadmin(StatesGroup):
    fio = State()
    tg_id = State()


@dp.message_handler(text="📊 Statistika")
async def Statistika_function(message: types.Message):
    tg_id = message.from_user.id
    user_count = await db.count_users()
    pul_ayirboshlash_count = await db.count_SuperAdmin_allowe_msg()
    message = (
        f"<b>📊 Statistika\n"
        f"👥 Foydalanuvchilar soni: {user_count} ta\n"
        f"💸 Pul ayirboshlash amallari: {pul_ayirboshlash_count} ta</b>"
    )
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 5419118871:
        await bot.send_message(tg_id, message, reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, message, reply_markup=AdminMain_menu)

@dp.message_handler(text="➕ Superadmin")
async def add_superadmin(message: types.Message):
    tg_id = message.from_user.id
    if tg_id == 5419118871:
        await message.answer("Assalomu alaykum Bot creator, Yangi superAdmin ismini kiriting")
        await AddSuperadmin.next()
    else:
        pass

@dp.message_handler(state=AddSuperadmin.fio)
async def superadmin_fullname(message: types.Message, state: FSMContext):
    fio = message.text
    await state.update_data(
        {"fio": fio}
    )
    data = await state.get_data()
    await message.answer(f"Super admin <b>telegram id</b> raqamini kiriting.")
    await AddSuperadmin.next()

@dp.message_handler(lambda message: message.text.isdigit(), state=AddSuperadmin.tg_id)
async def superadmin_tg_id(message: types.Message, state: FSMContext):
    tg_id = int(message.text)
    await state.update_data(
        {"tg_id": tg_id}
    )
    data = await state.get_data()
    fio = data.get('fio')
    tg_id = int(tg_id)
    try:
        await db.add_SuperAdmin(
            Superadmin_fio=fio,
            telegram_id=tg_id,
        )
    except Exception as e:
        pass
    await message.answer("Siz super adminni muvaffaqiyatli qo'shdingiz.",
                         reply_markup=AdminMain_menu)


@dp.message_handler(text="📞 Aloqa")
async def Statistika_function(message: types.Message):
    tg_id = message.from_user.id
    user_count = await db.count_users()
    pul_ayirboshlash_count = await db.count_SuperAdmin_allowe_msg()
    message = (
        f"<b>Ushbu botga aloqaga chiqing</b>\n"
        f"http://t.me/Foydauzbot"
    )
    tg_id = int(tg_id)
    checkid = await db.see_SuperAdmin(tg_id)
    if tg_id == 5419118871:
        await bot.send_message(tg_id, message, reply_markup=AdminMain_menu)
    elif tg_id == checkid:
        await bot.send_message(tg_id, message, reply_markup=AdminMain_menu)
    else:
        await bot.send_message(tg_id, message, reply_markup=mainMenu)