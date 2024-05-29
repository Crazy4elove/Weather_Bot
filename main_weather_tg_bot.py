import requests
import datetime
from config import tg_bot_token, open_weather_token
import telebot
from telebot import types

dp = telebot.TeleBot(token=tg_bot_token)
@dp.message_handler(commands=["start"])
def start_command(message: types.Message):
    dp.reply_to(message, "Привіт! Напиши мені назву міста і я пришлю прогноз погоди!")


@dp.message_handler()
def get_weather(message: types.Message):
    city = message.text

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:

        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = response.json()


        city_name = data["name"]
        current_temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        weather_emoji = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!")
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        daylight_hours = sunset_timestamp - sunrise_timestamp


        weather_message = (
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в місті: {city_name}\n"
            f"Температура: {current_temperature}C° {weather_emoji}\n"
            f"Вологість: {humidity}%\n"
            f"Вітер: {wind_speed} м/с\n"
            f"Всхід сонця: {sunrise_timestamp}\n"
            f"Захід сонця: {sunset_timestamp}\n"
            f"Тривалість дня: {daylight_hours}\n"
            f"Гарного дня!"
        )


        dp.reply_to(message, weather_message)
        dp.reply_to(message, "Напиши мені назву міста і я пришлю прогноз погоди!")

    except Exception as e:
        # Обработка ошибок
        print(f"Помилка при запросі погоди: {e}")
        dp.reply_to(message, "Перевірте назву міста!")

dp.polling()

#if __name__ == '__main__':
    #dp.start_polling(dp)