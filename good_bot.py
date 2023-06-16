import telebot
import openai
from telebot import types
import requests
import base64

KEY = "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"
openai.api_key = KEY

bot = telebot.TeleBot("6224897670:AAFA-S-mBRS54P7qQVPBH8xwVGqjJn4HB6Q", parse_mode=None)

def get_action():

    with open("what_to_dop.txt", "r") as file:
        action = file.read()
    return action

@bot.message_handler(commands=['essay'])
def write_essay(message):

    bot.send_message(message.chat.id, "Гаразд! Введіть тему для есе, який потрібно написати")

    with open("what_to_dop.txt", "w") as file:
        file.write("essay")

@bot.message_handler(commands=['image'])
def image(message):

    bot.send_message(message.chat.id, "Круто! Введіть тему для малюнка, який хочете получити")

    with open("what_to_dop.txt", "w") as file:
        file.write("image")

def image(caption):
    # quastion = input("Введіть речення: ")
    try:
        response = openai.Image.create(
        prompt=caption,
        n=2,
        size="1024x1024",
        response_format="b64_json"
        )
        print(response)
        # Отримання результату генерації зображення
        image_data = response['data'][0]['b64_json']
        with open('image.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image_data))  
    except:
        print("Щось пішло не по плану!")

def quastion(quastion):
    # quastion = input("Введіть речення: ")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"You: {quastion}",
    temperature=0.5,
    max_tokens=2000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=["You:"]
    )
    print(response)
    for txt in response['choices']: 
        return(txt['text'])

def essey(theme):
    # quastion = input("Введіть речення: ")

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"write an essey:  {theme}",
    temperature=0.5,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    max_tokens=2000,
    )
    print(response)
    for txt in response['choices']: 
        return(txt['text'])

@bot.message_handler(content_types=['text'])
def get_quastion(message):

    action = get_action()

    if action == "essay":
        bot.send_message(message.chat.id, "Окей, скоро скину текст!")

        response = essey(message.text)
        bot.send_message(message.chat.id, response)

        with open('what_to_dop.txt', 'w') as file:
            file.write(" ")

    elif action == "image":
        image(message.text)

        with open('image.png', 'rb') as image_:

            bot.send_photo(message.chat.id, image_)
        
        with open('what_to_dop.txt', 'w') as file:
            file.write(" ")

    else:
        response = quastion(message.text)
        bot.send_message(message.chat.id, response)

bot.polling()