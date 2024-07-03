from aiogram.dispatcher.filters.state import State, StatesGroup

class HamyonState_buy(StatesGroup):
    choose_kirish = State()
    choose_chiqish = State()
    price = State()
    check_photo = State()

class PulYechish(StatesGroup):
    karta = State()
    mahsusKod = State()
    tasdiqlash = State()

from aiogram.dispatcher.filters.state import StatesGroup, State

class sendPost(StatesGroup):
    text = State()
    state = State()
    photo = State()
    video = State()
    document = State()
