from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from text_to_speech import text_to_speech, speech_to_text
from environ import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

user_state = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    user_state[message.chat.id] = 'start'

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/speech"))

    bot.send_message(message.chat.id, "Welcome! Use the '/speech' command to have your text voiced "
                                      "or use voice message to turn into text.",
                     reply_markup=markup)


@bot.message_handler(commands=['speech'])
def speech(message: Message):
    user_state[message.chat.id] = 'waiting_for_text'
    bot.send_message(message.chat.id, "Send me your message, and I will voice it for you.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message: Message):
    text = message.text
    text_to_speech(text)
    with open('text_to_speech.mp3', 'rb') as audio_file:
        bot.send_audio(message.chat.id, audio_file)


@bot.message_handler(content_types=['voice'])
def voice(message):
    file = bot.get_file(message.voice.file_id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    bot.send_message(message.chat.id, text=text)


def my_commands():
    return [
        BotCommand("/start", "Start bot"),
        BotCommand("/speech", "Speech to text")
    ]


if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
