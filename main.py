import telebot
import random
from pydub import AudioSegment
import time
import requests
import speech_recognition as sr
from telebot import types 
# Замени 'TOKEN' на токен твоего бота
bot = telebot.TeleBot("")
interestingfacts = ["Глобальное потепление, является результатом увеличения средней температуры на поверхности Земли из-за парниковых газов, таких как углекислый газ и метан."
                    ," Выбросы парниковых газов, останутся в атмосфере в течение многих лет, делая невозможным устранение проблемы глобального потепления на протяжении нескольких десятилетий."
                    ,"Согласно докладу МГЭИК 2007 года, уровень моря из-за глобального потепления поднимется на 19-60 см к концу этого столетия.",
                    "С 1880 года средняя температура воздуха выросла на 0,7–0,8°С."
                    ,"В соответствии с исследованиями по изменению климата, последние два десятилетия 20-го века были самыми жаркими за последние 400 лет."
                    ,"За последние 50 лет температура на планете увеличивалась быстрее, чем за любой аналогичный период в прошедшие 2 000 лет."
                    ,"Самая быстро нагревающаяся территория на Земле — Арктика. В среднем Арктика теплеет в 3–4 раза быстрее, чем остальные регионы планеты. А в 2020 году в городе Верхоянск (Республика Саха/Якутия) был побит невероятный рекорд: впервые к северу от Полярного круга была зафиксирована температура воздуха 38 °C."
                    ,"Данные НАСА показывают, что за период с 1993 по 2019 год Гренландия теряла в среднем 279 миллиардов тонн льда в год. Такого объёма хватило бы, чтобы покрыть всю Москву слоем льда толщиной около 250 метров. Антарктида в то же время теряла около 148 миллиардов тонн льда в год."
                    ,"Концентрации основных парниковых газов (углекислого газа, метана и закиси азота) в атмосфере Земли сейчас выше, чем когда-либо за последние 800 000 лет."
                    ,"Первыми людьми, кто был эвакуирован из-за повышения уровня Мирового океана, вызванного глобальным потеплением, стали жители острова Тегуа в Тихом океане. Это произошло в 2006 году."
                    ,"По данным Всемирного фонда дикой природы, глобальное потепление может стать виновником вымирания белых медведей в течение следующих 20 лет."
                    ,"В условиях изменения климата наиболее уязвимыми районами станут: Сахара, дельты рек в Азии и небольшие острова."
                    ,"В результате роста средней температуры увеличивается площадь пустынь. В 2007 году Австралия потеряла 25% растениеводческой продукции из-за опустынивания."]
keyboard = types.ReplyKeyboardMarkup
key = types.KeyboardButton 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global markup
    
    bot.reply_to(message, "Привет! Я твой Telegram бот освещающий проблемы глобального потепления.")
    markup = keyboard(resize_keyboard = True)
    butt1 = ("Интересный факт")
    butt2 = ("Мини-игра викторина")
    butt5 = ("Голосовое в текст")
    butt6 = ("Полезные статьи")
    markup.add(butt1,butt2,butt5,butt6)
    send = bot.send_message(message.chat.id,"Выбирай что тебе интресено из блоков ниже:",reply_markup=markup)
    bot.register_next_step_handler(send,reply)
@bot.message_handler(content_types=["voice","text"])
def reply(message):
    global markup
    global interestingfacts
    yesornot = keyboard(resize_keyboard = True)
    butt3 = ("Да")
    butt4 = ("Нет")
    yesornot.add(butt3,butt4)
    facts = random.choice(interestingfacts)
    if message.text == "Интересный факт":
        bot.send_message(message.chat.id,f"{facts}")
    if message.text == "Мини-игра викторина":
        send = bot.send_message(message.chat.id,f"Ты действительно хочешь сыграть?",reply_markup=yesornot)
        bot.register_next_step_handler(send,yesornotgame)
    if message.text == "Голосовое в текст":
        send = bot.send_message(message.chat.id,f"Отправляй голосовое а я переведу его в текст! Круто,да?",reply_markup=markup)
        bot.register_next_step_handler(send,get_voice)
    if message.text == "Полезные статьи":
        global markup
        bot.send_message(message.chat.id,f"Статья на Wikipedia:https://ru.wikipedia.org/wiki/Глобальное_потепление\nСтатья ООН:https://www.un.org/ru/global-issues/climate-change\nСтатья от Яндекс:https://yandex.ru/pogoda/ru/blog/globalnoe-poteplenie\nСюжет от РБК:https://www.rbc.ru/story/66b4a5ce9a79473cb11c638d\nСоветы по борьбе с глобальныйм потеплением:https://ru.wikihow.com/бороться-с-глобальным-потеплением",reply_markup=markup)



def get_voice(message):
    global markup
    file_info = bot.get_file(message.voice.file_id)  
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format("8516966915:AAF3jkANtolI4_pzGDPJPjeuR8r5D7mroSc", file_info.file_path))  
    with open('input.ogg','wb') as f:  
        f.write(file.content)
    audio = AudioSegment.from_ogg("input.ogg")
    audio.export("voice.wav", format="wav", parameters=["-ar", "16000", "-ac", "1"])
    recognizer = sr.Recognizer()
    with sr.AudioFile("voice.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        bot.send_message(message.chat.id,f"Текст голосового:\n{text}")  

    except sr.UnknownValueError:             
        bot.send_message(message.chat.id,f"Не удалось распознать речь.")
    except sr.RequestError as e:             
        bot.send_message(message.chat.id,f"Ошибка сервиса: {e}")



#Код мини-игры(не оптимизированно,много строчек лишних)   
def yesornotgame(message):
    global gamebutt
    global markup
    gamebutt = keyboard(resize_keyboard = True)
    buttq1 = "A"
    buttq2 = "B"
    buttq3 = "C"
    buttq4 = "Выйти в меню"
    gamebutt.add(buttq1,buttq2,buttq3,buttq4)

    if message.text == "Да":
        bot.reply_to(message,"Значит начинаем!\nПервый вопрос. Что является основным источником углекислого газа, производимого человеком?")
        time.sleep(1)
        send = bot.send_message(message.chat.id,f"Варианты ответа:\nA:Сжигание ископаемого топлива\nB:Использование мобильных телефонов\nC:Строительство здания",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game)
    elif message.text == "Нет":
        send = bot.send_message(message.chat.id,f"Твое дело...",reply_markup=markup)
        bot.register_next_step_handler(send,reply)
    
def game(message):
    global score
    score = 0
    if message.text == "A":
        score += 10
        send = bot.send_message(message.chat.id,f"Абсолютнро верно! Ваш счет:{score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Второй вопрос. Как деревья помогают снизить уровень углекислого газа в атмосфере?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счет уменьшения эрозии почвы\nB:Выделяя кислород\nС:Поглощая углекислый газ в процессе фотосинтеза.",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game2)
    if message.text == "B":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:Сжигание ископаемого топлива. Ваш счет:{score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Второй вопрос. Как деревья помогают снизить уровень углекислого газа в атмосфере?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счет уменьшения эрозии почвы\nB:Выделяя кислород\nС:Поглощая углекислый газ в процессе фотосинтеза.",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game2)
    if message.text == "C":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:Сжигание ископаемого топлива",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Второй вопрос. Как деревья помогают снизить уровень углекислого газа в атмосфере?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счет уменьшения эрозии почвы\nB:Выделяя кислород\nС:Поглощая углекислый газ в процессе фотосинтеза.",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game2)
    if message.text == "Выйти в меню":
        send = bot.send_message(message.chat.id,f"Главное меню",reply_markup=markup)
        bot.register_next_step_handler(send,reply)

def game2(message):
    global score
    if message.text == "A":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:С:Поглощая углекислый газ в процессе фотосинтеза. Ваш счет:{score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Третий вопрос. Как океаны поглощают углекислый газ?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счёт растворения углекислого газа в воде\nB:Создавая океанские течения\nС:Путем испарения воды",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game3)
    if message.text == "B":
        time.sleep(0.6)
        bot.reply_to(message,"Третий вопрос. Как океаны поглощают углекислый газ?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счёт растворения углекислого газа в воде\nB:Создавая океанские течения\nС:Путем испарения воды",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game3)
    if message.text == "C":
        score += 10
        send = bot.send_message(message.chat.id,f"Абсолютно верно! Ваш счет:{score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Третий вопрос. Как океаны поглощают углекислый газ?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:За счёт растворения углекислого газа в воде\nB:Создавая океанские течения\nС:Путем испарения воды",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game3)
    if message.text == "Выйти в меню":
        send = bot.send_message(message.chat.id,f"Главное меню",reply_markup=markup)
        bot.register_next_step_handler(send,reply)


def game3(message):
    global score
    if message.text == "A":
        score += 10
        send = bot.send_message(message.chat.id,f"Абсолютнро верно! Ваш счет:{score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Четвертый вопрос. Как деятельность человека повлияла на баланс парниковых газов и поглотителей?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:Они увеличили пропускную способность естественных поглотителей\nB:Они произвели парниковых газов в количестве, превышающем поглощающую способность природных поглотителей\nC:Они увеличили пропускную способность естественных поглотителей",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game4)
    if message.text == "B":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:За счёт растворения углекислого газа в воде",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Четвертый вопрос. Как деятельность человека повлияла на баланс парниковых газов и поглотителей?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:Они увеличили пропускную способность естественных поглотителей\nB:Они произвели парниковых газов в количестве, превышающем поглощающую способность природных поглотителей\nC:Они увеличили пропускную способность естественных поглотителей",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game4)
    if message.text == "C":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:За счёт растворения углекислого газа в воде",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Четвертый вопрос. Как деятельность человека повлияла на баланс парниковых газов и поглотителей?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:Они увеличили пропускную способность естественных поглотителей\nB:Они произвели парниковых газов в количестве, превышающем поглощающую способность природных поглотителей\nC:Они увеличили пропускную способность естественных поглотителей",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game4)
    if message.text == "Выйти в меню":
        send = bot.send_message(message.chat.id,f"Главное меню",reply_markup=markup)
        bot.register_next_step_handler(send,reply)

def game4(message):
    global score
    if message.text == "A":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:B:Они произвели парниковых газов в количестве, превышающем поглощающую способность природных поглотителей",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Пятый ворос. Когда начались систематические измерения климата?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:Варианты ответа:\nA:1970-е годы\nB:Середина XIX века\nC:1600-е годы",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game5)
    if message.text == "B":
        score += 10 
        send = bot.send_message(message.chat.id,f"Абсолютно верно! Ваш балл: {score}",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Пятый ворос. Когда начались систематические измерения климата?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:1970-е годы\nB:Середина XIX века\nC:1600-е годы",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game5)
    if message.text == "C":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:За счёт растворения углекислого газа в воде",reply_markup=gamebutt)
        time.sleep(0.6)
        bot.reply_to(message,"Пятый ворос. Когда начались систематические измерения климата?")
        time.sleep(0.6)
        bot.send_message(message.chat.id,f"Варианты ответа:\nA:1970-е годы\nB:Середина XIX века\nC:1600-е годы",reply_markup=gamebutt)
        bot.register_next_step_handler(send,game5)
    if message.text == "Выйти в меню":
        send = bot.send_message(message.chat.id,f"Главное меню",reply_markup=markup)
        bot.register_next_step_handler(send,reply)

def game5(message):
    global score
    endg = keyboard(resize_keyboard=True)
    endq =  "Продолжить"
    endg.add(endq)
    if message.text == "A":
        send = bot.send_message(message.chat.id,f"Неверно",reply_markup=endg)
        time.sleep(0.6)
        bot.register_next_step_handler(send,gameend)
        
    if message.text == "B":
        score += 10
        send = bot.send_message(message.chat.id,f"Абсолютно верно!",reply_markup=endg)
        time.sleep(0.6)
        bot.register_next_step_handler(send,gameend)
       
    if message.text == "C":
        send = bot.send_message(message.chat.id,f"Неверно. Правильный вариант ответа:A:За счёт растворения углекислого газа в воде",reply_markup=endg)
        time.sleep(0.6)
        bot.register_next_step_handler(send,gameend)
       
    if message.text == "Выйти в меню":
        send = bot.send_message(message.chat.id,f"Главное меню",reply_markup=markup)
        bot.register_next_step_handler(send,reply)
def gameend(message):
    global score
    if message.text == "Продолжить":
        send = bot.send_message(message.chat.id,f"Игра окончена! Ваш счет:{score}",reply_markup=markup)
        if score == 50:
            bot.send_message(message.chat.id,f"Вы ответили на все вопросы правильно! Отличный резултат!!")
        if score <= 40:
            bot.send_message(message.chat.id,f"Вы ошиблись пару раз. Не стоит расстраиваться,ошибка повод чему то научится!")
        bot.register_next_step_handler(send,reply)
bot.polling()
