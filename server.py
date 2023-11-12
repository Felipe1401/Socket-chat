import threading
import socket as skt
import re
from artefactos import *

server = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
server.bind((host, port))
server.listen()
hash = {}
mutex = threading.Lock()

def broadcast(message, sender=None):
    for key,value in hash.items():
        if value["client"] is not sender:
            value["client"].send(message)

def private_message(message, sender:str ,reciever:str=None):
    try:
        message = f"[PRIVADO] {sender}:" + message.replace(reciever, "",1)
        hash[reciever]["client"].send(message.encode("UTF-8", errors="ignore"))
    except:
        hash[sender]["client"].send("ERROR: Usuario no encontrado.".encode("UTF-8", errors="ignore"))

def handle(client):
    while 1:
        try:
            message = client.recv(1024)
            message = message.decode("UTF-8", errors="ignore")
            print(message)
            if ":q" in message:
                client.send("EXIT".encode("UTF-8", errors="ignore"))
                with mutex:
                    nickname = remove(client)
                print(f"[SERVER] Cliente {nickname} se ha desconectado.")
                broadcast(f"[SERVER] Cliente {nickname} se ha desconectado.".encode("UTF-8", errors="ignore"))
                client.close()
                break
            
            elif ":p" in message:
                message = message.split(" ")
                destinatario = message[2]
                nickname = lookup(client)
                mensaje = " ".join(message[2:])
                private_message(mensaje, nickname, destinatario)

            elif ":u" in message:
                message = "Usuarios conectados\n" + "-"*19
                users = list(hash.keys())
                message = message + "\n" +"\n".join(users)
                client.send(message.encode("UTF-8", errors="ignore"))

            elif ":artefactos" in message:
                message = get_inventory(hash, nickname)
                client.send(message.encode("UTF-8", errors="ignore"))
            else:
                message = replace_kaomojis(message)
                broadcast(message.encode("UTF-8", errors="ignore"), client)

        except:
            nickname = remove(client)
            client.close()
            broadcast(f"{nickname} left the chat!".encode("UTF-8", errors="ignore"))
            break

def remove(client):
    nick = lookup(client)
    del hash[nick]
    return nick

def lookup(client):
    nick = ""
    for key, value in hash.items():
        if value["client"] == client:
            nick = key
    return nick

def recive():
    global hash
    while True:
        client, address = server.accept()

        client.send("NICK".encode("UTF-8", errors="ignore"))
        while True:
            nickname = client.recv(1024).decode("UTF-8", errors="ignore")
            with mutex:
                if nickname not in list(hash.keys()):
                    break
            client.send(f"NICK_TAKEN".encode("UTF-8", errors="ignore"))
        ans = "no"
        with mutex:
            hash[nickname] = {}
            hash[nickname]["client"] = client
            hash[nickname]["inventario"] = [0]*42
        
        print(f"[SERVER] Cliente {nickname} conectado.")
        broadcast(f"[SERVER] Cliente {nickname} conectado.".encode("UTF-8", errors="ignore"), client)
        client.send("Bienvenido al chat de granjeros!".encode("UTF-8", errors="ignore"))
        while 1:
            client.send("[SERVER] Cuentame, que artefactos tienes?".encode("UTF-8", errors="ignore"))
            inventory = client.recv(1024).decode("UTF-8", errors="ignore")
            inventory = inventory.replace(nickname+": ", "")
            numeros = inventory.split(", ")
            client.send(f"[SERVER] Tus artefactos son: {id_to_name(numeros)}.\n esta bien? [Si/No]".encode("UTF-8", errors="ignore"))
            confirmacion = client.recv(1024).decode("UTF-8", errors="ignore")
            print(confirmacion.upper().split(" "))
            confirmacion = confirmacion.upper().split(" ")[1]
            if confirmacion == "SI" or confirmacion == "S": break
            else: continue
        with mutex:
            for i in numeros:
                hash[nickname]["inventario"][int(i)-1] = 1
        print(get_inventory(hash, nickname))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("--Servidor en linea--")
recive()