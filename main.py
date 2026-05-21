import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import collections
import datetime

TOKEN = "YOUR_BOT_TOKEN_HERE"

# bot = Bot(token=TOKEN)
dp = Dispatcher()

db = []

class Habit:
    _start_date: datetime.date
    _text: str
    _status: bool

    def __init__(self, description: str):
        self._start_date = datetime.date.today()
        self._text = description
        self._status = True

    def set_status(self, status):
        if (not(status) and self._status) or (status and not(self._status)): # если привыку бросили ИЛИ возобновили - отсчитываем время с сегодня
            self._start_date = datetime.date.today()
        self._status = status
    
    def get_status(self):
        return self._status

    def __str__(self):
        today = datetime.date.today()
        postfix = "дней"
        delta_days = (today - self._start_date).days
        if delta_days % 10 == 1:
            postfix = "день"
        elif delta_days % 10 in [2, 3, 4]:
            postfix = "дня"
        return self._text + f" - уже {delta_days} " + postfix

class UserHabits:
    __user_id: str
    _habits: list[Habit]

    def __init__(self, user_id: str):
        self.__user_id = user_id
        self._habits = []

    def get_user(self) -> str:
        return self.__user_id
    
    def set_user(self, user_id: str):
        self.__user_id = user_id
    
    def get_habits(self) -> list[Habit]:
        return self._habits
    
    def add_habit(self, habit: Habit):
        if habit not in self._habits:
            self._habits.append(habit)
    
    def remove_habit(self, habit: Habit):
        if habit in self._habits:
            self._habits.remove(habit)
    
    def get_habits_str(self) -> str:
        return "\n".join([f"{n:2}) {i}" for n, i in enumerate(self.get_habits(), start=1)])



@dp.message(CommandStart())
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Добавить привычку", callback_data="btn_add")
    
    builder.adjust(1)

    await message.answer(f"Здоров! Буду отслеживать твои новые привычки", reply_keyboard=builde.as_markup())


async def send_periodic_message(user_id: str):
    msg = ""
    for i in range(len(db)):
        if db[i].get_user() == user_id:
            msg += "\n".join([str(i) for i in db[i].get_habits()])
            break

    await bot.send_message(chat_id=CHAT_ID, text=msg)

@dp.message()
async def echo_handler(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice message!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

def example():
    h = Habit("testHabit")
    u = UserHabits('testUser')
    for i in range(10):
        u.add_habit(Habit("test" + str(i)))
    # Вывел все привычки пользователя
    print(u.get_user() + ":\n" + u.get_habits_str())

    print("==============")

    # Проверка на сброс счетчика дней привычки после прекращения
    h._start_date = datetime.date(2020, 1, 1)
    print(str(h))
    h.set_status(False)
    print(str(h))

if __name__ == "__main__":
    #asyncio.run(main())
    example()
