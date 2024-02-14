from aiogram import Bot, Dispatcher, executor, types
from gtts import gTTS
from pydub import AudioSegment
import tempfile
from pydub import AudioSegment
from pathlib import Path
import os
import speech_recognition as sr


token = "6829169088:AAGZa--U_s88qZm7gnxXjLo0d_RKFRMjfHc"

bot = Bot(token=token)   # сам бот
dp = Dispatcher(bot)
r = sr.Recognizer()


def ogg_to_vaw():
    print(os.listdir("voices"))     # получаем содержимое папки с голосовыми
    last_voice = os.listdir("voices")[-1]     # берем последнее из списка
    print(last_voice)     # выводим его название, что бы убедится в этом
    file = os.path.abspath(f"voices/{last_voice}")     # формируем путь до последнего голосового сообщения
    print(file)
    Path(f"output").mkdir(parents=True, exist_ok=True)     # создаем папку
    mp = AudioSegment.from_file(file).export("output/file", format="mp3")     # делаем копию в новую папку формата mp3
    sound = AudioSegment.from_mp3(mp)   # из mp3 конвертируем в wav
    sound.export(f"output/res.wav", format="wav")

    message = sr.AudioFile("output/res.wav")    #
    with message as source:    # считываем из аудио текст
        audio = r.record(source)
    result = r.recognize_google(audio,
                                language="ru_RU")  #   используя возможности библиотеки распознаем текст, так же тут можно изменять язык распознавания
    print(result)
    return result    # отправляем полученный текст из голосового


@dp.message_handler(content_types=["voice"])     # Декоратор для определения команды. То есть фраза начинается с /
async def start(message: types.Message):
        voice = await message.voice.get_file()  # получаем голосовое
        path = "voices"  # название папки в которую будем скачивать голосовое
        Path(f"{path}").mkdir(parents=True, exist_ok=True)  # создается папка если ее нет
        await bot.download_file(file_path=voice.file_path, destination=f"{path}/voice_{len(os.listdir(path))}.ogg")  #
        answer = ogg_to_vaw()
        print(answer)
        await message.answer(text=answer)


@dp.message_handler(content_types=["text"])
async def start(message: types.Message):
        await message.answer(text=message.text)

executor.start_polling(dp, skip_updates=True)

