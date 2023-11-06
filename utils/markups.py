from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnProfile = KeyboardButton(text='ИНВЕНТАРЬ')
btnQuests = KeyboardButton(text='ЗАДАНИЯ')
btnTrade = KeyboardButton(text='ТОРГОВЛЯ')

mainMenu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [btnProfile, btnQuests, btnTrade],
    ]
)

btnStartDialog = KeyboardButton(text='СТАРТОВЫЙ ДИАЛОГ')
btnNext = KeyboardButton(text='Ну, выкладывай уже')
btnNew = KeyboardButton(text="Давай как с новичком.")
btnExperienced = KeyboardButton(text="Давай как с опытным.")

startDialog = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [btnNew, btnExperienced],
    ]
)
