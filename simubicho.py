import telebot
from telebot import types
import random
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
def obter_grupo_e_descricao_por_numero(numero):
    for intervalo, dados in grupos.items():
        if dados['grupo'] == numero:
            return dados['grupo'], dados['descricao']
    return None, None
def obter_grupo_e_descricao(valor):
    for intervalo, dados in grupos.items():
        if intervalo[0] <= valor <= intervalo[1]:  # <= em vez de <
            return dados['grupo'], dados['descricao']
    return None, None
def obter_grupo_e_descricao(valor):
    for intervalo, dados in grupos.items():
        if intervalo[0] <= valor < intervalo[1]:
            return dados['grupo'], dados['descricao']
    return None, None

def obter_animal(numero):
    grupo, descricao = obter_grupo_e_descricao(numero)
    return descricao if grupo is not None else None

def obter_aposta_sorteio_animais(numero, numero_gerado, digitos):
    aposta = numero 
    sorteio = numero_gerado 
    animal_aposta = obter_animal(aposta % 100)
    animal_sorteado = obter_animal(sorteio%100)
    return aposta, sorteio, animal_aposta, animal_sorteado
# Manipulador de consulta para lidar com o botão "Novo Jogo"
@bot.callback_query_handler(func=lambda call: call.data == 'novo_jogo')
def callback_novo_jogo(call):
    # Chamar a função send_welcome
    send_welcome(call.message)
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

        lucro = -valor_aposta  # Se não acertou, o lucro é negativo, representando a perda.
    message += f'\n*Número sorteado:* {sorteio}\n' 
    message += f'\n*Número sorteado considerando os últimos {digitos} dígitos: *"{str(sorteio % (10 ** digitos)).zfill(digitos)}"\n'
    message += f'\n*Animal sorteado:* {animal_sorteado}\n'
    message += f'{"➖" * 17}'
    message += f'\n🎯 *Aposta realizada:* {str(aposta).zfill(digitos)}\n'
    message += f'\n*Animal correspondente da aposta:* {animal_aposta}\n'
    message += f'\n💲*Lucro: R$*{lucro}\n'
    # Botão "Novo Jogo"
    markup = types.InlineKeyboardMarkup()
    novo_jogo_button = types.InlineKeyboardButton("Novo Jogo", callback_data='novo_jogo')
    markup.add(novo_jogo_button)

    # Mensagem com o botão
    bot.send_message(chat_id, message, reply_markup=markup, parse_mode="Markdown")
grupos = {
    (1, 5): {'grupo': 1, 'descricao': "Avestruz - Grupo 1 🥚"},
    (5, 9): {'grupo': 2, 'descricao': "Águia - Grupo 2 🦅"},
    (9, 13): {'grupo': 3, 'descricao': "Burro - Grupo 3🫏"},
    (13, 17): {'grupo': 4, 'descricao': "Borboleta - Grupo 4 🦋"},
    (17, 21): {'grupo': 5, 'descricao': "Cachorro - Grupo 5 🐶"},
    (21, 25): {'grupo': 6, 'descricao': "Cabra - Grupo 6 🐐"},
    (25, 29): {'grupo': 7, 'descricao': "Carneiro - Grupo 7 🐏"},
    (29, 33): {'grupo': 8, 'descricao': "Camelo - Grupo 8 🐫"},
    (33, 37): {'grupo': 9, 'descricao': "Cobra - Grupo 9 🐍"},
    (37, 41): {'grupo': 10, 'descricao': "Coelho - Grupo 10 🐇"},
    (41, 45): {'grupo': 11, 'descricao': "Cavalo - Grupo 11 🐎"},
    (45, 49): {'grupo': 12, 'descricao': "Elefante - Grupo 12 🐘"},
    (49, 53): {'grupo': 13, 'descricao': "Galo - Grupo 13 🐔"},
    (53, 57): {'grupo': 14, 'descricao': "Gato - Grupo 14 🐱"},
    (57, 61): {'grupo': 15, 'descricao': "Jacaré - Grupo 15 🐊"},
    (61, 65): {'grupo': 16, 'descricao': "Leão - Grupo 16 🦁"},
    (65, 69): {'grupo': 17, 'descricao': "Macaco - Grupo 17 🐒"},
    (69, 73): {'grupo': 18, 'descricao': "Porco - Grupo 18 🐖"},
    (73, 77): {'grupo': 19, 'descricao': "Pavão - Grupo 19 🦚"},
    (77, 81): {'grupo': 20, 'descricao': "Peru - Grupo 20 🦃"},
    (81, 85): {'grupo': 21, 'descricao': "Touro - Grupo 21 🐂"},
    (85, 89): {'grupo': 22, 'descricao': "Tigre - Grupo 22 🐅"},
    (89, 93): {'grupo': 23, 'descricao': "Urso - Grupo 23 🐻"},
    (93, 97): {'grupo': 24, 'descricao': "Veado - Grupo 24 🦌"},
    (97, 100): {'grupo': 25, 'descricao': "Vaca - Grupo 25 🐄"},
    (0, 1): {'grupo': 25, 'descricao': "Vaca - Grupo 25 🐄"}
}
@bot.message_handler(func=lambda message: message.text.lower().startswith('/bicho'))
#Exibição dos grupos e intervalo
def listar_grupos(message):
    mensagem = "_Aqui estão os grupos e seus respectivos números:_\n\n"

    for intervalo, dados in grupos.items():
        #aqui ele verifica se tem um range de (0,1) e só exibe 0, isso ocorre pela compelxidade do grupo vaca.
        if intervalo == (0, 1):
            mensagem += f"\n*0: {dados['descricao']}*\n"
        else:
            #aqui exibe normal,  diminuindo em 1 undiade a exibição, pq ele ta extraindo  o range, so q o range em python n conta o ultimo segundo exibido
            mensagem += f"\n*{intervalo[0]}-{intervalo[1] - 1}: {dados['descricao']}*\n"

    bot.reply_to(message, mensagem,parse_mode='Markdown')

# Mensagem de boas-vindas
@bot.message_handler(func=lambda message: message.text.lower().startswith('/sobre'))
def send_sobre(message):
    sobre_message = "🐊🎩 *SimuBicho* é um jogo de simulação inspirado no tradicional jogo do bicho, mas é importante ressaltar que *NÃO* tem nenhum envolvimento com loterias reais. O objetivo é proporcionar uma experiência divertida e interativa.\n"
    sobre_message+= """\n*Simubicho V0.1*💚
    Este bot está passando por sua primeira atualização/implantação inicial. 
    Em breve, receberá melhorias para aprimorar a realidade da experiência simulada. Agradecemos pela sua paciência!\n"""
    sobre_message += """\n*❗Aviso Importante:*
    Este simulador é baseado na lógica criada pelo programador e não utiliza as mesmas normas ou resultados do jogo do bicho real.
    A randomização dos números é feita de forma programática, proporcionando uma experiência virtual única.\n"""
    sobre_message +="""\n❗Lembramos que *NÃO* há prêmios em dinheiro real envolvidos. Este jogo é puramente recreativo. Divirta-se e boa sorte! 🍀\n"""
    sobre_message += "\n/Dezena - _Jogar na modalidade de Dezena_\n"
    sobre_message += "/Centena - _Jogar na modalidade de Centena_\n"
    sobre_message += "/Milhar - _Jogar na modalidade de Milhar_\n"
    sobre_message += "/Grupo - _Jogar na modalidade de Grupo_\n"
    sobre_message += "/Bicho - _Visualizar tabela_\n"
    sobre_message +="\n ☕ Bot desenvolvido por @doiscafe"

    bot.reply_to(message, sobre_message, parse_mode="Markdown")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton("/Dezena")
    item2 = types.KeyboardButton("/Centena")
    item3 = types.KeyboardButton("/Milhar")
    item4 = types.KeyboardButton("/Grupo")
    item5 = types.KeyboardButton("/Sobre")
    item6 = types.KeyboardButton("/Bicho")


    markup.add(item1, item2, item3, item4,item5,item6)

    bot.reply_to(message, f"🐊 Bem-vindo ao SimuBicho, seu simulador de jogo do bicho online.\n● Digite /Sobre para obter mais  informações.\n● Digite /Bicho para obter a tabela.\nEscolha uma modalidade para jogar:", reply_markup=markup)

# Manipulador de mensagens para a modalidade de Dezena
@bot.message_handler(func=lambda message: message.text.lower().startswith('/dezena'))
def handle_dezena(message):
    # Solicitar o valor da aposta
    bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*",parse_mode='Markdown')

    # Aguardar a resposta do usuário para o valor da aposta
    bot.register_next_step_handler(message, validar_valor_aposta_dezena)
    
def validar_valor_aposta_dezena(message):
    try:
        valor_aposta = float(message.text)
        if valor_aposta <= 0:
            raise ValueError(" *O valor da aposta deve ser positivo. Tente novamente.*")

        # Solicitar o número da dezena
        bot.reply_to(message, "*Agora, informe o número da dezena (entre 00 e 99)\n \nNúmeros com menos de 2 dígitos serão preenchidos com 0 à esquerda.*",parse_mode='Markdown')        
        bot.register_next_step_handler(message, processar_aposta_dezena, valor_aposta)
    except ValueError:
        bot.reply_to(message, f"❌ *Erro: Forneça um valor válido para investir*", parse_mode='Markdown')
        # Se ocorreu um erro, pedir novamente o valor da aposta
        bot.register_next_step_handler(message, validar_valor_aposta_dezena)

def processar_aposta_dezena(message, valor_aposta):
    try:
        numero = int(message.text)
        if not (0 <= numero < 100):
            raise ValueError
    except ValueError:
        bot.reply_to(message, "*Por favor, forneça um número de dezena válido (entre 00 e 99).*",parse_mode='Markdown')
        # Pedir novamente o número da dezena
        bot.register_next_step_handler(message, processar_aposta_dezena, valor_aposta)
        return
    # Mensagem indicando que a aposta está sendo processada
    msg = bot.reply_to(message, "⏰ *Processando a aposta, por favor aguarde...*",parse_mode='Markdown')
    # Aguarde 5 segundos
    sleep(5)
    numero_gerado = random.randint(0, 9999)
    possivel_ganho = valor_aposta * 6
    lucro = possivel_ganho - valor_aposta
    aposta, sorteio, animal_aposta, animal_sorteado = obter_aposta_sorteio_animais(numero, numero_gerado, 2)
    # Exibir resultado
    exibir_resultado(message.chat.id, aposta, sorteio, valor_aposta, possivel_ganho, animal_aposta, animal_sorteado, lucro, 2)
    # Remover a mensagem indicando processamento
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

#Centena
    
@bot.message_handler(func=lambda message: message.text.lower().startswith('/centena'))
def handle_centena(message):
    # Solicitar o valor da aposta
    bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*",parse_mode='Markdown')
    # Aguardar a resposta do usuário para o valor da aposta
    bot.register_next_step_handler(message, validar_valor_aposta_centena)
    
def validar_valor_aposta_centena(message):
    try:
        valor_aposta = float(message.text)
        if valor_aposta < 0:
            raise ValueError(" O valor da aposta deve ser positivo. Tente novamente")

        # Solicitar o número da centena
        bot.reply_to(message, "*Agora, informe o número da centena (entre 000 e 999)\n \nNúmeros com menos de 3 dígitos serão preenchidos com 0 à esquerda.*",parse_mode='Markdown')
        bot.register_next_step_handler(message, processar_aposta_centena, valor_aposta)
    except ValueError:
        bot.reply_to(message, f"❌ *Erro: Forneça um valor válido para investir*", parse_mode='Markdown')
        # Se ocorreu um erro, pedir novamente o valor da aposta
        bot.register_next_step_handler(message, validar_valor_aposta_centena)

def processar_aposta_centena(message, valor_aposta):
    try:
        numero = int(message.text)
        if not (0 <= numero < 1000):
            raise ValueError
    except ValueError:
        bot.reply_to(message, "*Por favor, forneça um número de centena válido (entre 000 e 999).*",parse_mode='Markdown')
        # Pedir novamente o número da centena
        bot.register_next_step_handler(message, processar_aposta_centena, valor_aposta)
        return
    # Enviar uma mensagem indicando que a aposta está sendo processada
    msg = bot.reply_to(message, "⏰ *Processando a aposta, por favor aguarde...*",parse_mode='Markdown')
    # Aguarde 5 segundos
    sleep(5)
    numero_gerado = random.randint(0, 9999)
    possivel_ganho = valor_aposta * 6
    lucro = possivel_ganho - valor_aposta
    aposta, sorteio, animal_aposta, animal_sorteado = obter_aposta_sorteio_animais(numero, numero_gerado, 3)
    # Exibir resultado
    exibir_resultado(message.chat.id, aposta, sorteio, valor_aposta, possivel_ganho, animal_aposta, animal_sorteado, lucro, 3)
    # Remover a mensagem indicando processamento
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

#Milhar

@bot.message_handler(func=lambda message: message.text.lower().startswith('/milhar'))
def handle_milhar(message):
    # Solicitar o valor da aposta
    bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*",parse_mode='Markdown')
    # Aguardar a resposta do usuário para o valor da aposta
    bot.register_next_step_handler(message, validar_valor_aposta_milhar)
    
def validar_valor_aposta_milhar(message):
    try:
        valor_aposta = float(message.text)
        if valor_aposta <= 0:
            raise ValueError(" O valor da aposta deve ser positivo. Tente novamente")

        # Solicitar o número da milhar
        bot.reply_to(message, "*Agora, informe o número da milhar (entre 0000 e 9999)\n \nNúmeros com menos de 4 dígitos serão preenchidos com 0 à esquerda.*",parse_mode='Markdown')
        bot.register_next_step_handler(message, processar_aposta_milhar, valor_aposta)
    except ValueError:
        bot.reply_to(message, f"❌ *Erro: Forneça um valor válido para investir*", parse_mode='Markdown')
        # Se ocorreu um erro, pedir novamente o valor da aposta
        bot.register_next_step_handler(message, validar_valor_aposta_milhar)

def processar_aposta_milhar(message, valor_aposta):
    try:
        numero = int(message.text)
        if not (0 <= numero < 10000):
            raise ValueError
    except ValueError:
        bot.reply_to(message, "*Por favor, forneça um número de milhar válido (entre 0000 e 999).*",parse_mode='Markdown')
        # Pedir novamente o número da milhar
        bot.register_next_step_handler(message, processar_aposta_milhar, valor_aposta)
        return
    # Enviar uma mensagem indicando que a aposta está sendo processada
    msg = bot.reply_to(message, "⏰ *Processando a aposta, por favor aguarde...*",parse_mode='Markdown')
    # Aguarde 5 segundos
    sleep(5)
    numero_gerado = random.randint(0, 9999)
    possivel_ganho = valor_aposta * 6
    lucro = possivel_ganho - valor_aposta
    aposta, sorteio, animal_aposta, animal_sorteado = obter_aposta_sorteio_animais(numero, numero_gerado, 4)
    # Exibir resultado
    exibir_resultado(message.chat.id, aposta, sorteio, valor_aposta, possivel_ganho, animal_aposta, animal_sorteado, lucro, 4)
    # Remover a mensagem indicando processamento
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

#Grupo
@bot.message_handler(func=lambda message: message.text.lower().startswith('/grupo'))
def handle_grupo(message):
    # Solicitar o valor da aposta
    bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*",parse_mode='Markdown')
    # Aguardar a resposta do usuário para o valor da aposta
    bot.register_next_step_handler(message, validar_valor_aposta_grupo)
    
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
    msg = bot.reply_to(message, "⏰ *Processando a aposta, por favor aguarde...*",parse_mode='Markdown')
    # Aguarde 5 segundos
    sleep(5)
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

            f"💲*Lucro: R$* {lucro}\n"
        )
    # botão "Novo Jogo"
    markup = types.InlineKeyboardMarkup()
    novo_jogo_button = types.InlineKeyboardButton("Novo Jogo", callback_data='novo_jogo')
    markup.add(novo_jogo_button)
    bot.send_message(msg.chat.id, message, reply_markup=markup, parse_mode="Markdown")
    # Remover a mensagem indicando processamento
    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
bot.polling()