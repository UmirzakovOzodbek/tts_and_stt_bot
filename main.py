from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from text_to_speech import text_to_speech, speech_to_text
from environ import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")

bot = TeleBot(BOT_TOKEN)


# @bot.message_handler(commands=['start'])
# def start(message):
#     user = message.from_user
#     fullname = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
#     answer = f"<b>Hi!</b>, <u>{fullname}</u>"
#     bot.send_message(message.chat.id, text=answer, parse_mode='html')

user_state = {}


@bot.message_handler(commands=['start'])
def start(message: Message):
    # Set the user's state to 'start'
    user_state[message.chat.id] = 'start'

    # Create a custom keyboard with a 'Speech' button
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/speech"))
    markup.add(KeyboardButton("/voice"))

    # Send a welcome message and instruct the user to press the '/speech' command
    bot.send_message(message.chat.id, "Welcome! Use the '/speech' command to have your text voiced "
                                      "or use the /voice command to turn voice into text.",
                     reply_markup=markup)


# Handle the '/speech' command
@bot.message_handler(commands=['speech'])
def speech(message: Message):
    # Set the user's state to 'waiting_for_text'
    user_state[message.chat.id] = 'waiting_for_text'

    # Send a message instructing the user to send their text
    bot.send_message(message.chat.id, "Send me your message, and I will voice it for you.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message: Message):
    # Extract the text message
    text = message.text

    # Call the text-to-speech function to generate an audio file
    text_to_speech(text)

    # Open the generated audio file
    with open('text_to_speech.mp3', 'rb') as audio_file:
        # Send the audio file to the user
        bot.send_audio(message.chat.id, audio_file)


# @bot.message_handler(commands=['speech'])
# def speech(message):
#     text = ' '.join(message.text.split(' ')[1:])
#     text_to_speech(text)
#     with open('text_to_speech.mp3', 'rb') as f:
#         bot.send_audio(message.chat.id, f)


@bot.message_handler(commands=['voice'])
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
        BotCommand("/speech", "Speech to text"),
        BotCommand("/voice", "Text to speech")
    ]


if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()



# chat_id = message.chat.id
    # answer = f'Send me your message and I will voice it for you'
    # bot.send_message(chat_id, f"{answer}")
    # text = ' '.join(message.text.split(' ')[1:])
    # text_to_speech(text)