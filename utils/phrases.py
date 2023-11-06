import random

greeting_phrases_name = [
    'Здорово, рад тебя видеть, {user_name}! Ну чё, давай о деле поговорим?',
    'Эх, гробы подорожают!',
    'Ты бы еще консервных банок насобирал…',
    'О, а этот живой! Счастливчик. Хотя, кто знает, что для тебя лучше…',
    'Приветствую {user_name}! Как успехи?',
]

greeting_phrases = [
    'Сталкер, если что-то интересное найдешь в зоне, приноси сюда. Неплохо на этом можно заработать.',
    'Сколько раз я говорил: не лазь в аномалии, иначе ты останешься без артефактов и без жизни.',
    'Привет, пришелец. Ты случайно не новичок? Если что, я всегда тут, готов помочь советом или продажей.',
    'Ну что, здоровченко, как нашелся в Зоне? Хочешь торговать или секретные задания выполнять?',
]


def random_greeting_phrase(user_name):
    if len(user_name) > 1:
        greeting = random.choice(greeting_phrases_name).format(user_name=user_name)
    else:
        greeting = random.choice(greeting_phrases)
    return greeting