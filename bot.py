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
import vars.token as api_token
TOKEN = api_token.token

form_router = Router()


class Form(StatesGroup):
    next = State()
    start_guide_level = State()
    durak = State()
    like_bots = State()
    language = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.next)
    await message.answer(
        "Короче, Меченый. Я тебя спас и в благородство играть не буду."
        " Выполнишь для меня пару заданий и мы в расчете. Заодно посмотрим,"
        " как быстро у тебя башка после амнезии прояснится, а по твоей теме постараюсь разузнать. "
        "Хрен его знает на кой ляд тебе этот Стрелок сдался, ну а я в чужие дела не лезу."
        " Хочешь убить, значит, есть за что.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Ну, выкладывай."),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.next, F.text.casefold() == ("Ну, выкладывай.").lower())
async def process_start_guide(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.start_guide_level)
    await message.answer(
        "Выбирай, как мы с тобой поступим: либо я тебе сейчас мозги буду полоскать,"
        " как я обычно новичкам это делаю, "
        "либо я буду с тобой как с опытным сталкером: получай задание, и вперёд!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Давай как с новичком."),
                    KeyboardButton(text="Давай как с опытным."),
                ]
            ],
            resize_keyboard=True,
        ),
    )
    # await show_summary(message=message, next=next, positive=False)


@form_router.message(Form.start_guide_level, F.text.casefold() == ("Давай как с новичком.").lower())
async def process_start_guide(message: Message, state: FSMContext):
    await state.set_state(Form.next)

    await message.answer_photo(
        photo="https://static.wikia.nocookie.net/stalker/images/8/81/PDA_2.png/revision/latest?cb=20180420174356&path-prefix=pl",
        caption="Это твой личный ПДА. Полезная хреновина, которая помогает не сдохнуть в Зоне, а если и сдохнешь, то хоть другие будут знать, как и где, хе-хе-хе...",
        reply_markup=ReplyKeyboardRemove(
            keyboard=[
                [
                    KeyboardButton(text="Ладно, шутник, давай к делу уже!"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@form_router.message(Form.next, F.text.casefold() == ("Ладно, шутник, давай к делу уже!").lower())
async def process_start_guide(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.durak)
    await message.answer(
        "Ну, сам напросился!",
        reply_markup=ReplyKeyboardRemove(
            keyboard=[
                [
                    KeyboardButton(text="Чёрт!"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
