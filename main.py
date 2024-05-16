from telebot_instance import bot
from message_handlers import send_welcome, listar_grupos, send_sobre, handle_dezena, handle_centena, handle_milhar, handle_grupo, callback_novo_jogo
import random
import time
from telebot import types
from grupos import grupos
bot.message_handler(commands=['start'])(send_welcome)
bot.message_handler(func=lambda message: message.text.lower().startswith('/bicho'))(listar_grupos)
bot.message_handler(func=lambda message: message.text.lower().startswith('/sobre'))(send_sobre)
bot.message_handler(func=lambda message: message.text.lower().startswith('/dezena'))(handle_dezena)
bot.message_handler(func=lambda message: message.text.lower().startswith('/centena'))(handle_centena)
bot.message_handler(func=lambda message: message.text.lower().startswith('/milhar'))(handle_milhar)
bot.message_handler(func=lambda message: message.text.lower().startswith('/grupo'))(handle_grupo)
bot.callback_query_handler(func=lambda call: call.data == 'novo_jogo')(callback_novo_jogo)


def run( ):
        bot.infinity_polling()
if __name__ == "__main__":
    run()



