from aiogram.dispatcher.filters.state import State, StatesGroup

# Процессс для регистрации
class Tournament(StatesGroup):
    player_name_state = State()
    player_id_state = State()
    game_disc_state = State()
    player_phone_number_state = State()
    profile_player = State()

