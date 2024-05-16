from telebot_instance import bot, TOKEN
from telebot import types
from grupos import grupos
from processamento_apostas import validar_valor_aposta, validar_numero_aposta, obter_aposta_sorteio_animais, obter_animal, validar_valor_aposta_grupo, processar_aposta_grupo

def listar_grupos(message):
    mensagem = "_Aqui estão os grupos e seus respectivos números:_\n\n"
    for intervalo, dados in  grupos.items():
        if intervalo == (0, 1):
            mensagem += f"\n*0: {dados['descricao']}*\n"
        else:
            mensagem += f"\n*{intervalo[0]}-{intervalo[1] - 1}: {dados['descricao']}*\n"
    bot.reply_to(message, mensagem, parse_mode='Markdown')

def send_sobre(message):
    sobre_message = "🐊🎩 *SimuBicho* é um jogo de simulação inspirado no tradicional jogo do bicho, mas é importante ressaltar que *NÃO* tem nenhum envolvimento com loterias reais. O objetivo é proporcionar uma experiência divertida e interativa.\n"
    sobre_message += """\n*Simubicho V0.1*💚
    Este bot está passando por sua primeira atualização/implantação inicial. 
    Em breve, receberá melhorias para aprimorar a realidade da experiência simulada. Agradecemos pela sua paciência!\n"""
    sobre_message += """\n*❗Aviso Importante:*
    Este simulador é baseado na lógica criada pelo programador e não utiliza as mesmas normas ou resultados do jogo do bicho real.
    A randomização dos números é feita de forma programática, proporcionando uma experiência virtual única.\n"""
    sobre_message += """\n❗Lembramos que *NÃO* há prêmios em dinheiro real envolvidos. Este jogo é puramente recreativo. Divirta-se e boa sorte! 🍀\n"""
    sobre_message += "\n/Dezena - _Jogar na modalidade de Dezena_\n"
    sobre_message += "/Centena - _Jogar na modalidade de Centena_\n"
    sobre_message += "/Milhar - _Jogar na modalidade de Milhar_\n"
    sobre_message += "/Grupo - _Jogar na modalidade de Grupo_\n"
    sobre_message += "/Bicho - _Visualizar tabela_\n"
    sobre_message += "\n ☕ Bot desenvolvido por @doiscafe"
    bot.reply_to(message, sobre_message, parse_mode="Markdown")

# handler de boas-vindas, com teclado de opções
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Dezena")
    item2 = types.KeyboardButton("/Centena")
    item3 = types.KeyboardButton("/Milhar")
    item4 = types.KeyboardButton("/Grupo")
    item5 = types.KeyboardButton("/Sobre")
    item6 = types.KeyboardButton("/Bicho")
    markup.add(item1, item2, item3, item4, item5, item6)
    bot.reply_to(message, f"🐊 Bem-vindo ao SimuBicho, seu simulador de jogo do bicho online.\n● Digite /Sobre para obter mais informações.\n● Digite /Bicho para obter a tabela.\nEscolha uma modalidade para jogar:", reply_markup=markup)


######### handlers de modalidades #########
def handle_dezena(message):
        bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*", parse_mode='Markdown')
        bot.register_next_step_handler(message,validar_valor_aposta, 2)

def handle_centena(message):
        bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*", parse_mode='Markdown')
        bot.register_next_step_handler(message,validar_valor_aposta, 3)

def handle_milhar(message):
        bot.reply_to(message, "\n💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*", parse_mode='Markdown')
        bot.register_next_step_handler(message,validar_valor_aposta, 4)

def handle_grupo(message):
    # Solicitar o valor da aposta
    bot.reply_to(message, "💵 *Por favor, informe o valor da aposta em reais (R$) (ex: 10.0).*",parse_mode='Markdown')
    # Aguardar a resposta do usuário para o valor da aposta
    bot.register_next_step_handler(message, validar_valor_aposta_grupo)

def callback_novo_jogo(call):
        bot.send_message(call.message.chat.id, "🦁 Escolha uma nova modalidade para jogar:\n\n /Dezena \n /Centena\n /Milhar\n /Grupo")

