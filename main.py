# Для Google Colab установить библиотеку: !pip install pyTelegramBotAPI

from telebot import TeleBot, types
import json
import time

bot = TeleBot('7395468145:AAH_APOj3dMtZVMXcXHLmkiFsNLuy_OZk6U', parse_mode='HTML')  # вставь свой токен из телеграмм бота @BotFather


# /start 
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    # создаём клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_example = types.KeyboardButton('Пример')
    btn_help = types.KeyboardButton('Помощь')
    btn_clear = types.KeyboardButton('Очистить экран')
    markup.add(btn_example, btn_help, btn_clear)

    bot.send_message(
        message.chat.id,
        "Привет! 👋 Я PrettyJsonBot.\n"
        "Отправь мне JSON, и я сделаю его красивым.\n"
        "Или нажми «Пример», чтобы увидеть пример JSON.",
        reply_markup=markup
    )


# Обработка кнопок и сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message: types.Message):
    if message.text == 'Пример':
        example_json = '{"name":"PrettyJsonBot","version":1.0,"features":["validation","formatting","fun"],"author":"Mur Mur"}'
        bot.send_message(message.chat.id, example_json)
        return

    elif message.text == 'Помощь':
        bot.send_message(
            message.chat.id,
            "📘 Просто пришли мне JSON в виде текста, "
            "а я проверю его и верну красиво отформатированную версию!"
        )
        return

    elif message.text == 'Очистить экран':
        clear_screen(message)
        return

    # Обработка JSON 
    try:
        payload = json.loads(message.text)
    except json.JSONDecodeError as ex:
        bot.send_message(
            message.chat.id,
            f"⚠️ Ошибка в JSON:\n<code>{str(ex)}</code>"
        )
        return

    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)

    # Если JSON длинный нужно отправить его как файл
    if len(text) > 4000:
        with open('pretty_json.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        with open('pretty_json.txt', 'rb') as f:
            bot.send_document(message.chat.id, f, caption="📄 Вот твой отформатированный JSON")
    else:
        bot.send_message(message.chat.id, f"✨Красота! Вот твой JSON✅ :\n<code>{text}</code>")


# Очистка экрана
def clear_screen(message: types.Message):
    bot.send_message(message.chat.id, "🧹 Очищаю экран...")
    time.sleep(0.5)

    # Удаляем последние 20 сообщений
    for i in range(20):
        try:
            bot.delete_message(message.chat.id, message.message_id - i)
        except:
            pass

    bot.send_message(message.chat.id, "✅ Экран очищен!\nМожешь начать заново 😉")


# Запуск самого бота
if __name__ == '__main__':
    print("🤖 PrettyJsonBot запущен!")
    bot.infinity_polling()
