import speech_recognition as sr
import webbrowser as wb
import os
import winsound
import datetime
import pyautogui as pag

recognize = sr.Recognizer()
recognize.pause_threshold = 0.5

while True:
    try:
        with sr.Microphone() as source:
            audio = recognize.listen(source=source)
            result = recognize.recognize_google(audio_data=audio, language="ru-RU")
            print(result)
        if result.lower() == "музыка":
            os.system(f"start muz.mp3")
        elif result.lower() == "закрой окно":
            # pag.moveTo(1880, 10)
            pag.click(1880, 15, 1, 1, 'left')
            pag.moveTo(900, 500)
        elif result.lower() == "стоп":
            winsound.PlaySound("round-start.wav", winsound.SND_FILENAME)
            break
        elif result.lower() == "открой браузер":
            wb.open_new_tab("https://pypi.org/project/SpeechRecognition/")
    except sr.UnknownValueError as e:
        print(f'Ошибка - {e}. Вы молчите...')
    except sr.RequestError as e:
        print('Ошибка при запросе к Google API. Возможно неполадки с интернетом')
    except KeyboardInterrupt:
        print('Программа завершена')










