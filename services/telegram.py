import os
import telebot

token_final = "7729314755:AAEbqoHhyDyku2AMTkRycDDwfdVk8VhMhJA"


def enviar_mensagem(mensagem, CHAT_ID = '5588207726',BOT_TOKEN = token_final):

    bot = telebot.TeleBot(BOT_TOKEN)

    # Enviando a mensagem
    bot.send_message(CHAT_ID, mensagem)

