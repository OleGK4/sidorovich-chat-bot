import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from utils.markups import (
    mainMenu,
    startDialog,
    btnStartDialog,
    btnNext
)
from models import createtables
from db import Database
from utils import auth
from utils.phrases import random_greeting_phrase

logging.basicConfig(level=logging.NOTSET)

createtables()
db = Database('sidor.db')

TOKEN = auth.token
bot = Bot(token=TOKEN)
form_router = Router()


class Form(StatesGroup):
    start_dialog = State()
    next = State()
    start_guide_level = State()
    signup = State()
    setname = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if db.user_exists(message.from_user.id) and db.get_signup(message.from_user.id) == 'registered':
        await bot.send_message(message.from_user.id, random_greeting_phrase(db.get_name(message.from_user.id)), reply_markup=mainMenu)
    else:
        await state.set_state(Form.start_dialog)
        await bot.send_message(message.from_user.id, random_greeting_phrase(''), reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [btnStartDialog]
            ]
        ))


@form_router.message(Form.start_dialog, F.text == 'СТАРТОВЫЙ ДИАЛОГ')
async def start_dialog(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.next)
    await bot.send_message(
        message.from_user.id,
        "Короче, Меченый. Я тебя спас и в благородство играть не буду."
        " Выполнишь для меня пару заданий и мы в расчете. Заодно посмотрим,"
        " как быстро у тебя башка после амнезии прояснится, а по твоей теме"
        " постараюсь разузнать. Хрен его знает на кой ляд тебе этот Стрелок "
        "сдался, ну а я в чужие дела не лезу. Хочешь убить, значит, есть за что.",
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [btnNext]
            ],
        ),
    )


@form_router.message(Form.next, F.text == 'Ну, выкладывай уже')
async def process_start_guide_level(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start_guide_level)
    await bot.send_message(
        message.from_user.id,
        "Выбирай, как мы с тобой поступим: либо я тебе сейчас мозги буду полоскать, как я обычно новичкам это "
        "делаю, либо я буду с тобой как с опытным сталкером: получай задание, и вперёд!",
        reply_markup=startDialog
    )


@form_router.message(Form.start_guide_level, F.text == "Давай как с новичком.")
async def start_guide(message: Message, state: FSMContext):
    await state.set_state(Form.signup)
    await bot.send_photo(
        message.from_user.id,
        photo="https://static.wikia.nocookie.net/stalker/images/8/81/PDA_2.png/revision/latest?cb=20180420174356&path-prefix=pl",
        caption="Это твой личный ПДА. Полезная хреновина, которая помогает не сдохнуть в Зоне, а если и сдохнешь, то хоть другие будут знать, как и где, хе-хе-хе...",
        reply_markup=ReplyKeyboardRemove(
            keyboard=[
                [
                    KeyboardButton(text="Ладно, шутник, давай записывай меня к себе!"),
                ]
            ],
            resize_keyboard=True,
        )
    )


@form_router.message(Form.start_guide_level, F.text == ("Давай как с опытным."))
async def start_guide(message: Message, state: FSMContext):
    await state.set_state(Form.signup)

    await message.answer(
        'Посмотрим насколько ты бывалый, опытный говоришь? А по тебе особо и не скажешь.',
        reply_markup=ReplyKeyboardRemove(
            keyboard=[
                [
                    KeyboardButton(text="Хватит болтовни, записывай в блокнотик свой!"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.signup,
                     F.text.in_({"Ладно, шутник, давай записывай меня к себе!",
                                 "Хватит болтовни, записывай в блокнотик свой!"}))
async def signup(message: Message, state: FSMContext) -> None:
    if db.user_exists(message.from_user.id) and db.get_signup(message.from_user.id) != 'setname':
        await bot.send_message(message.from_user.id,
                               "Чего ты мне лапшу на уши вешаешь? Ты уже есть у меня в списках! Я еще не настолько старый что-бы забыть такого как ты!")
    elif db.user_exists(message.from_user.id) and db.get_signup(message.from_user.id) == 'setname':
        await state.set_state(Form.setname)
        await bot.send_message(message.from_user.id, "Хорошо, в этот раз назовись, что-ли?",
                               reply_markup=ReplyKeyboardRemove())
    else:
        db.add_user(message.from_user.id)
        await state.set_state(Form.setname)
        await bot.send_message(message.from_user.id, "Ну, хорошо, как звать тебя?", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.setname, F.text)
async def set_name(message: Message) -> None:
    if db.get_signup(message.from_user.id) == 'setname':
        if len(message.text) > 30:
            await bot.send_message(message.from_user.id,
                                   'Братан, больно за края ты вылезаешь, слишком большое имя у тебя. Сократи что-ли!')
        elif '@' in message.text or '/' in message.text or '!' in message.text:
            await bot.send_message(message.from_user.id, 'Всякую бурду пишешь, давай без закорючек всяких!')
        else:
            data = 'registered'
            db.set_name(message.from_user.id, message.text, data)
            await bot.send_message(message.from_user.id, 'Отлично... так и запишем.', reply_markup=mainMenu)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
