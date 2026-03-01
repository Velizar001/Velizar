import requests
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "ТВОЙ_ТОКЕН"
WEATHER_API_KEY = "ТВОЙ_API_КЛЮЧ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Almaty&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            gradus = data['main']['temp']

            if gradus < -10:
                return f"В Алматы: {gradus}°C\nОчень холодно, наденьте шапку и шарф"
            elif -10 <= gradus < 0:
                return f"В Алматы: {gradus}°C\nХолодно, наденьте тёплую куртку"
            elif 0 <= gradus < 10:
                return f"В Алматы: {gradus}°C\nПрохладно, возьмите с собой жилетку"
            else:
                return f"В Алматы: {gradus}°C\nОчень тепло, наслаждайтесь погодой"

        return "Погода недоступна"
    except:
        return "Ошибка связи"


def main_kb():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="🌤 Погода", callback_data="wth"))
    return keyboard


@dp.message_handler(commands=["start"])
def start(message: types.Message):
    message.answer("Выберите действие:", reply_markup=main_kb())


@dp.callback_query_handler(lambda c: c.data == "wth")
def process_callback(call: types.CallbackQuery):
    txt = get_weather()
    call.message.answer(txt)
    call.answer()


if __name__ == "__main__":
    print("--- БОТ ЗАПУСКАЕТСЯ ---")
    executor.start_polling(dp, skip_updates=True)
