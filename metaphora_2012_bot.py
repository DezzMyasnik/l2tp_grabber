from time import sleep

import telebot
bot = telebot.TeleBot('2059874864:AAFsVUVv9v2RVEhFOZvsstdmOXl7h2O8T6Q')
chat_id = 1972421843
user_id = 1972421843
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #chat_id = bot.get_chat("Metaphora_2012_bot")

    print(message.from_id.id)
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def send_sate(message):

    bot.send_message(1972421843,message)

if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
       bot.polling(none_stop=True) # запуск бота
    except Exception as e:
       print(e) # или import traceback; traceback.print_exc() для печати полной инфы
       sleep(15)