import requests
import datetime
from config import tg_bot, open_weather
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types



bot = Bot(token=tg_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Йоу!🙃 Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1"


    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in smile:
            wd = smile[weather_description]
        else:
            wd = "Посмотри в окно, я не понимаю какая погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Погода в городе: {city}\n🌡Температура: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"🌅Восход солнца: {sunrise_timestamp}\n🌇Закат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"❤ всего хорошего)!❤"
                            )

    except:
        await message.reply("❗Пожалуйста проверь название города❗")


if __name__ == '__main__':
    executor.start_polling(dp)