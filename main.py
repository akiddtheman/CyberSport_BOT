from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import buttons
from states import Tournament
import database

storage = MemoryStorage()

bot = Bot('TOKEN')
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def command_start(message):
    start_text = "Приветствуем Вас на регистрационной платформе по ближайшим киберспортивным событиям на территории нашей Родины! 🇺🇿\n\n" \
                 "❗ Турниры для лиц, достигших 16-летнего возраста ❗\n\n" \
                 "Просим вас нажать ниже на соответствующую кнопку, если вы готовы начать регистрацию на турниры 🔽"

    await message.answer(start_text, reply_markup=buttons.main_menu())

@dp.callback_query_handler()
async def login(callback_query: types.CallbackQuery):
    if callback_query.data == 'register':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Для начала напишите ваше настоящее имя\n\n'
                                                                         'Просим ввести свое настоящее имя правильно - без ошибок\n'
                                                                         'Имя должно соответствовать с тем, что в вашем паспорте 🪪', reply_markup=ReplyKeyboardRemove())

    await Tournament.player_name_state.set()

@dp.message_handler(state=Tournament.player_name_state)
async def player_name(message, state=Tournament.player_name_state):
    player_name = message.text

    await state.update_data(name=player_name)

    await message.answer('Супер!\n\n'
                         'Теперь введите пожалуйста ID вашего игрового аккаунта 🎮\n\n'
                         '❗ Предупреждение ❗\n\n'
                         'Введите пожалуйста ID именно того аккаунта, на котором будете принимать участие на турнире')

    await Tournament.player_id_state.set()

@dp.message_handler(state=Tournament.player_id_state)
async def player_id(message, state=Tournament.player_id_state):
    player_id = message.text

    if not player_id.isdigit():
        await message.answer('⚠ Пожалуйста, введите только ID игрового аккаунта')
        return

    await state.update_data(id=int(player_id))

    await message.answer('✅ Oтлично, вы зарегистрировали ID вашего игрового аккаунта\n\n'
                         '✅ Этот ID будет использован для внесения вас в базу данных участников\n\n'
                         'Выберите теперь дисциплину, по которой хотите принять участие на турнире ⬇', reply_markup=buttons.disc_kb())

    await Tournament.game_disc_state.set()

@dp.callback_query_handler(state=Tournament.game_disc_state)
async def discipline(callback_query: types.CallbackQuery, state=Tournament.game_disc_state):
    game_discipline = callback_query.data
    await state.update_data(game_discipline=game_discipline)

    if callback_query.data == 'CS:GO':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Регистрация прошла успешно!\nЗа подробной информации о турнире перейдите по ссылке нашего сайта:\n\n'
                                                                         'http://JAproject.pythonanywhere.com\n\n'
                                                                         'Скиньте пожалуйста ваш контакный номер, чтобы наши администраторы могли с вами связаться', reply_markup=buttons.phone_number_kb())
    elif callback_query.data == 'VALORANT':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Регистрация прошла успешно!\nЗа подробной информации о турнире перейдите по ссылке нашего сайта:\n\n'
                                                                         'http://JAproject.pythonanywhere.com\n\n'
                                                                         'Скиньте пожалуйста ваш контакный номер, чтобы наши администраторы могли с вами связаться', reply_markup=buttons.phone_number_kb())
    elif callback_query.data == 'FIFA':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Регистрация прошла успешно!\nЗа подробной информации о турнире перейдите по ссылке нашего сайта:\n\n'
                                                                         'http://JAproject.pythonanywhere.com\n\n'
                                                                         'Скиньте пожалуйста ваш контакный номер, чтобы наши администраторы могли с вами связаться',reply_markup=buttons.phone_number_kb())
    elif callback_query.data == 'DOTA 2':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Регистрация прошла успешно!\nЗа подробной информации о турнире перейдите по ссылке нашего сайта:\n\n'
                                                                         'http://JAproject.pythonanywhere.com\n\n'
                                                                         'Скиньте пожалуйста ваш контакный номер, чтобы наши администраторы могли с вами связаться', reply_markup=buttons.phone_number_kb())
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text='Пожалуйста, выберите лишь существующие дисциплины из списка ниже:\n\nCounter Strike\nVALORANT\nFIFA\nDOTA 2', reply_markup=buttons.disc_kb())

    await Tournament.player_phone_number_state.set()

@dp.message_handler(state=Tournament.player_phone_number_state, content_types=['contact'])
async def player_number(message, state=Tournament.player_phone_number_state):
    user_number = message.contact.phone_number

    await state.update_data(number=user_number)

    await message.answer('Отлично! Чтобы посмотреть полную информацию о вашем себе перейдите в свой аккаунт по соответствующей кнопке ниже ⬇', reply_markup=buttons.account_kb())

    all_info = await state.get_data()
    player_name = all_info.get('name')
    player_id = all_info.get('id')
    game_discipline = all_info.get('game_discipline')
    user_number = all_info.get('number')
    database.add_player(player_name, player_id, game_discipline, user_number)

    print(database.get_player(player_id))

    await Tournament.profile_player.set()

@dp.callback_query_handler(state=Tournament.profile_player)
async def account(callback_query: types.CallbackQuery, state=Tournament.profile_player):
    all_info = await state.get_data()
    player_name = all_info.get('name')
    player_id = all_info.get('id')
    game_discipline = all_info.get('game_discipline')
    user_number = all_info.get('number')

    # Получаем данные из базы данных
    database.get_player(player_name)
    database.get_player(player_id)
    database.get_player(game_discipline)
    database.get_player(user_number)

    if callback_query.data == "profile":
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Ваше имя: {player_name}\n'
                                                                         f'ID вашего игрового аккаунта: {player_id}\n'
                                                                         f'Турнир, в котором вы участвуете: {game_discipline}\n'
                                                                         f'Ваш контактный номер: {user_number}\n\n'
                                                                         'Сохраните пожалуйста эти данные. Администраторы турниров напомнят вам о дате и месте проведения турнира\n\n'
                                                                         'Желаем великих побед!!! 🏆')

    await state.finish()

executor.start_polling(dp)
