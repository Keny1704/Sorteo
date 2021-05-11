import telebot
#from telebot import types
import numpy as np
import random
bot = telebot.TeleBot("1821210569:AAHkE7MLUSqu4oUCQQhoG9PgXAiyKIflgNA")

participantes = []
tp = [0]
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Apriete /sortear para empezar")
@bot.message_handler(commands=['sortear'])
def bienvenida(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id,"Que TP es?")
    bot.register_next_step_handler(msg, TP)

def TP (message):
    chat_id =message.chat.id
    if message.text == "/sortear":
        msg = bot.send_message(chat_id,"Que TP es?")
        bot.register_next_step_handler(msg, bienvenida)
    else:
        nro_TP = message.text
        tp[0] = nro_TP
        msg = bot.send_message(chat_id, "Nombre a los participantes uno debajo del otro, por ejemplo:\n\n"
                                        "Quintero\n"
                                        "Pratto\n"
                                        "Martinez")
        bot.register_next_step_handler(msg, part)

def part(message):
    chat_id = message.chat.id
    if message.text == "/sortear":
        msg = bot.send_message(chat_id,"Que TP es?")
        bot.register_next_step_handler(msg, bienvenida)
    else:
        part = message.text
        for line in part.splitlines():
            participantes.append(line)
        msg = bot.send_message(chat_id, "Cuantos ejercicios son?")
        bot.register_next_step_handler(msg, ejer)

def ejer(message):
    chat_id = message.chat.id
    if message.text == "/sortear":
        msg = bot.send_message(chat_id,"Que TP es?")
        bot.register_next_step_handler(msg, bienvenida)
    else:
        n = message.text
    #Cantidad de ejercicios TOTAL
        n_i = int(n)
    #Cantidad de ejercicios por participante
        c = n_i/len(participantes)
        c_i = round(c,0)
        if c_i<c:
            c = c_i + 1
            ci = int (c)
        else:
            ci = int(c_i)
        lista_ejer = list(range(1,n_i+1))
        random.shuffle(lista_ejer)
        lista_ejer_final = [0]*(len(participantes)*ci)
        for i in range(n_i):
            lista_ejer_final [i] = lista_ejer[i]
        random.shuffle(participantes)
        cant_part = len(participantes)
        matriz = np.array(lista_ejer_final).reshape(ci,cant_part)
        matriz_final = np.array(matriz).T
        mensaje = "TP" +str(tp[0])+ "\n"
        for i in range(cant_part):
            nombre = participantes[i]
            ejer = ":  "
            for j in range(ci):
                ejer += str(matriz_final[i][j]) +"    "
            mensaje += "- "+ nombre + ejer +"\n"
        bot.send_message(chat_id, mensaje)
        bot.send_message(chat_id, "Apriete /sortear para empezar")
        participantes.clear()
        print(chat_id)
#    else:
#        chat_id = message.chat.id
#        msg = bot.send_message(chat_id, "Ingresaste texto, donde se esperaba numero\nCuantos ejercicios son?")
#        bot.register_next_step_handler(msg, ejer)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

print("el bot se esta ejecutando")

bot.polling()
