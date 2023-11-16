import threading
import socket as skt
from artefactos import *

server = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
server.bind((host, port))
server.listen()
hash = {}
mutex = threading.Lock()
current_trans = 0
transactions = {}
def accept(from_id, trans_id):
    loc_trans = None
    with mutex:
        loc_trans = transactions[trans_id]
    if(from_id == loc_trans["emit"]):
        from_nick, to_nick = loc_trans["nicks"][0], loc_trans["nicks"][1]
        with mutex:
            from_inv,to_inv = hash[from_nick]["inventario"], hash[to_nick]["inventario"]
        from_item, to_item = loc_trans["arts"][0], loc_trans["arts"][1]
        from_idx = hash[from_nick]["inventario"].index(int(from_item))
        to_idx = hash[to_nick]["inventario"].index(int(to_item))
        swap = from_item

        hash[from_nick]["inventario"][from_idx] = int(to_item)
        hash[to_nick]["inventario"][to_idx] = int(swap)
        hash[to_nick]["pending"] = 0
        hash[from_nick]["pending"] = 0
        hash[from_nick]["client"].send(f"accept: La transaccion {trans_id} con el usuario {to_nick} ha sido realizada con éxito!".encode("UTF-8"))
        hash[to_nick]["client"].send(f"accept: La transaccion {trans_id} con el usuario {from_nick} ha sido realizada con éxito!".encode("UTF-8"))

def reject(from_nick, trans_id):
    with mutex:
        loc_trans = transactions[int(trans_id)]
    to_nick = loc_trans["nicks"][1]
    from_nick = loc_trans["nicks"][0]
    if (to_nick in list(hash.keys())):
        hash[to_nick]["pending"] = 0
        hash[to_nick]["client"].send(f"reject:".encode("UTF-8", errors="ignore"))
    hash[from_nick]["pending"] = 0
    hash[from_nick]["client"].send(f"reject:".encode("UTF-8", errors="ignore"))
def broadcast(message, sender=None, ):
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
    global current_trans
    while 1:
        try:
            message = client.recv(1024)
            message = message.decode("UTF-8", errors="ignore")
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
                nickname = message.split(":")[0]
                message = get_inventory(hash, nickname)
                client.send(message.encode("UTF-8", errors="ignore"))
                
            elif ":offer" in message:
                params = message.split(" ")[1:]
                nick_from, nick_to, my_id, to_id = params[0], params[1], params[2], params[3]
                if (nick_to in list(hash.keys()) and hash[nick_to]["pending"] == 0 and int(to_id) in hash[nick_to]["inventario"] and int(my_id) in hash[nick_from]["inventario"]):
                    with mutex:
                        loc_trans = current_trans
                        current_trans+=1
                        hash[nick_to]["pending"] = 1
                        hash[nick_from]["pending"] = 1
                    transactions[loc_trans] = {"state": 1, "nicks":[nick_from, nick_to], "arts" :[my_id, to_id], "emit": nick_to}
                    msg = f":transaction {loc_trans}"
                    hash[nick_from]["client"].send(msg.encode("UTF-8", errors="ignore"))
                    hash[nick_to]["client"].send(msg.encode("UTF-8", errors="ignore"))
                    hash[nick_to]["client"].send(f"{nick_from} propoen un intercambio de tu {id_to_name(to_id)} por su {id_to_name(my_id)}".encode("UTF-8", errors="ignore"))
                else:
                    if nick_to not in list(hash.keys()):
                        hash[nick_from]["client"].send("El cliente no existe.".encode("UTF-8", errors="ignore"))
                    elif hash[nick_from]["pending"]:
                        hash[nick_from]["client"].send("Termine transacciones pendientes antes de iniciar una nueva".encode("UTF-8", errors="ignore"))
                    elif int(to_id) not in hash[nick_to]["inventario"]:
                        hash[nick_from]["client"].send(f"El cliente {nick_to} no tiene el item {id_to_name([to_id])}".encode("UTF-8", errors="ignore"))
                    elif int(my_id) not in hash[nick_from]["inventario"]:
                        hash[nick_from]["client"].send(f"No tienes el item {id_to_name([my_id])}".encode("UTF-8", errors="ignore"))
            elif message.startswith(":accept") and len(message.split(" ")) == 3:
                message = message.split(" ")
                who = message[1]
                trans_id = message[2]
                accept(who, int(trans_id))
            elif message.startswith(":reject") and len(message.split(" ")) == 3:
                message = message.split(" ")
                reject(message[1], message[2])
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
        
        print(f"[SERVER] Cliente {nickname} conectado.")
        broadcast(f"[SERVER] Cliente {nickname} conectado.".encode("UTF-8", errors="ignore"), client)
        client.send("Bienvenido al chat de granjeros!".encode("UTF-8", errors="ignore"))
        while 1:
            client.send("[SERVER] Cuentame, que artefactos tienes?".encode("UTF-8", errors="ignore"))
            inventory = client.recv(1024).decode("UTF-8", errors="ignore")
            inventory = inventory.replace(nickname+": ", "")
            numeros = id_to_list(inventory)
            client.send(f"[SERVER] Tus artefactos son: {id_to_name(numeros)}.\n esta bien? [Si/No]".encode("UTF-8", errors="ignore"))
            confirmacion = client.recv(1024).decode("UTF-8", errors="ignore")
            confirmacion = confirmacion.upper().split(" ")[1]
            if confirmacion == "SI" or confirmacion == "S": break
            else: continue
        with mutex:

            hash[nickname]["inventario"] = [int(i) for i in numeros]
            hash[nickname]["pending"] = 0

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("--Servidor en linea--")
recive()