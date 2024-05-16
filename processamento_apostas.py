from grupos import grupos
import random
import telebot
import telebot.types as types
from telebot_instance import bot
from time import sleep
from telebot import types
def validar_valor_aposta(message, digitos):
    try:
        valor_aposta = float(message.text)
        if valor_aposta <= 0:
            raise ValueError("O valor da aposta deve ser maior que zero.")
        bot.reply_to(message, f"💵 *Você escolheu apostar R$ {valor_aposta}.\n \nAgora, por favor, informe o número que deseja apostar ({digitos} dígitos).*", parse_mode='Markdown')
        bot.register_next_step_handler(message,validar_numero_aposta, valor_aposta, digitos)
    except ValueError:
            bot.reply_to(message, " ❌ Valor de aposta inválido. Por favor, tente novamente.")
            bot.register_next_step_handler(message,validar_valor_aposta, digitos)

def validar_numero_aposta(message, valor_aposta, digitos):
    try:
        numero_aposta = int(message.text)
        if not (0 <= numero_aposta < 10 ** digitos):
            raise ValueError(f"O número da aposta deve ter exatamente {digitos} dígitos.")
        processar_aposta(message, valor_aposta, numero_aposta, digitos)
    except ValueError:
            bot.reply_to(message, f"Número de aposta inválido. Por favor, informe um número de {digitos} dígitos.")
            bot.register_next_step_handler(message,  validar_numero_aposta, valor_aposta, digitos)

def processar_aposta(message, valor_aposta, numero_aposta, digitos):
    numero_gerado = random.randint(0, 9999)
    possivel_ganho = valor_aposta * 100
    aposta, sorteio, animal_aposta, animal_sorteado =  obter_aposta_sorteio_animais(numero_aposta, numero_gerado, digitos)
    msg =  bot.send_message(message.chat.id, "🎲 Estamos sorteando o número... 🎲\n\n🍀 Boa Sorte! 🍀")
    sleep(5)
    bot.delete_message(message.chat.id, msg.message_id)
    exibir_resultado(message.chat.id, aposta, sorteio, valor_aposta, possivel_ganho, animal_aposta, animal_sorteado, 0, digitos)

def obter_grupo_e_descricao_por_numero(numero):
    for intervalo, dados in  grupos.items():
        if dados['grupo'] == numero:
            return dados['grupo'], dados['descricao']
    return None, None

def obter_grupo_e_descricao(valor):
    for intervalo, dados in  grupos.items():
        if intervalo[0] <= valor < intervalo[1]:
            return dados['grupo'], dados['descricao']
    return None, None

def obter_animal(numero):
    grupo, descricao =  obter_grupo_e_descricao(numero)
    return descricao if grupo is not None else None

def obter_aposta_sorteio_animais(numero, numero_gerado, digitos):
    aposta = numero 
    sorteio = numero_gerado 
    animal_aposta =  obter_animal(aposta % 100)
    animal_sorteado =  obter_animal(sorteio % 100)
    return aposta, sorteio, animal_aposta, animal_sorteado

def exibir_resultado(chat_id, aposta, sorteio, valor_aposta, possivel_ganho, animal_aposta, animal_sorteado, lucro, digitos):
    if aposta == sorteio:
        message = f'🥳 Parabéns, você acertou! 🥳\n'
        message += f'\n💸 Você investiu R${valor_aposta}, e ganhou R${possivel_ganho} 💸\n'
        message += f'{"➖" * 17}'

        lucro = possivel_ganho - valor_aposta
    else:
        message = f'😭 Lamentamos, você não acertou! 😭\n'
        message += f'\nInfelizmente você investiu R${valor_aposta}, e não obteve retorno. 😞\n'
        message += f'{"➖" * 17}'
    message += f'\n*Número sorteado:* {sorteio}\n'
    message += f'\n*Número sorteado considerando os últimos {digitos} dígitos: *"{str(sorteio % (10 ** digitos)).zfill(digitos)}"\n'
    message += f'\n*Animal sorteado:* {animal_sorteado}\n'
    message += f'{"➖" * 17}'
    message += f'\n🎯 *Aposta realizada:* {str(aposta).zfill(digitos)}\n'
    message += f'\n*Animal correspondente da aposta:* {animal_aposta}\n'
    markup = types.InlineKeyboardMarkup()
    novo_jogo_button = types.InlineKeyboardButton("Novo Jogo", callback_data='novo_jogo')
    markup.add(novo_jogo_button)
    bot.send_message(chat_id, message, reply_markup=markup, parse_mode="Markdown")

# Processamento referente a modalidade grupo

def validar_valor_aposta_grupo(message):
    try:
        valor_aposta = float(message.text)
        if valor_aposta <= 0:
            raise ValueError(" *O valor da aposta deve ser positivo. Tente novamente*")

        # Solicitar o número do grupo
        bot.reply_to(message, "*Agora, informe o número do grupo (entre 1 e 25)*",parse_mode='Markdown')
        bot.register_next_step_handler(message, processar_aposta_grupo, valor_aposta)
    except ValueError:
        bot.reply_to(message, f"❌ *Erro: Forneça um valor válido para investir*", parse_mode='Markdown')
        # Se ocorreu um erro, pedir novamente o valor da aposta
        bot.register_next_step_handler(message, validar_valor_aposta_grupo)

def processar_aposta_grupo(message, valor_aposta):
    try:
        numero = int(message.text)
        if not (1 <= numero < 26):
            raise ValueError
    except ValueError:
        bot.reply_to(message, "*Por favor, forneça um número de grupo válido (entre 1 e 25)*.",parse_mode='Markdown')
        # Pedir novamente o número do grupo
        bot.register_next_step_handler(message, processar_aposta_grupo, valor_aposta)
        return
    # Enviar uma mensagem indicando que a aposta está sendo processada
    msg =  bot.send_message(message.chat.id, "🎲 Estamos sorteando o número... 🎲\n\n🍀 Boa Sorte! 🍀")
    # Aguarde 5 segundos
    sleep(5)
    bot.delete_message(message.chat.id, msg.message_id)
    aposta_grupo = numero
    numero_gerado = random.randint(0, 9999)
    ultimos_dois_digitos = numero_gerado % 100
    possivel_ganho = valor_aposta * 2
    lucro = possivel_ganho - valor_aposta

    grupo_apostado, descricao_apostada = obter_grupo_e_descricao_por_numero(aposta_grupo)
    grupo_gerado, descricao_gerada = obter_grupo_e_descricao(ultimos_dois_digitos)
    # Exibir resultado
    if grupo_apostado == grupo_gerado:
        message = (
            f"🎉 Parabéns, você acertou o grupo! 🎉\n\n"
            f'{"➖" * 17}'
            f"\n🎯 Grupo Apostado: {descricao_apostada}\n"
            f"\nNúmero gerado: {numero_gerado}\n"
            f"\nGrupo Equivalente: {grupo_gerado}, {descricao_gerada}\n"
            f'{"➖" * 17}'

            f"\n💸 Você investiu R${valor_aposta}, e ganhou R${possivel_ganho} 💸\n"
            f"\n💲 Lucro: R${lucro}\n"
        )
    else:
        lucro = -valor_aposta
        message = (
            f"😔 Lamentamos, você não acertou o grupo.\n"
            f"\n🎯 *Grupo Apostado:* {descricao_apostada}\n"
            f'{"➖" * 17}'

            f"\n*Número gerado:* {numero_gerado}\n"

            f"\n*Grupo Equivalente:* {grupo_gerado}, {descricao_gerada}\n"
            f'{"➖" * 17}'

            f"\nInfelizmente você investiu R${valor_aposta}, e não obteve retorno. 😞\n"
            f'{"➖" * 17}\n'
            

            
        )
    markup = types.InlineKeyboardMarkup()
    novo_jogo_button = types.InlineKeyboardButton("Novo Jogo", callback_data='novo_jogo')
    markup.add(novo_jogo_button)
    bot.send_message(msg.chat.id, message, reply_markup=markup, parse_mode="Markdown")