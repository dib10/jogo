import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
#esse arquivo é responsável por instanciar o bot do telegram e carregar o token de acesso