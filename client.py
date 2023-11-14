import socket
import threading
from artefactos import *

artefactos = []
current_trans = None
def initTrans(nickname_from,nickname_to, my_itemid, to_itemid):
    msg = f":offer {nickname_from} {nickname_to} {my_itemid} {to_itemid}" 
    if current_trans == None and nickname_to!=nickname:
        print("Puedes realizar la transaccion")
        #Llamar al servidor para iniciar la transaccion
        client.send(msg.encode("UTF-8", errors = "ignore"))
        #En el server llamar a makeTrans
    else:
        print("Revisa si tienes una transaccion pendiete o el id del remitente!")
def accept():
    global nickname
    global current_trans
    if(current_trans!=None):
        #aceptamos la ultima transaccion
        print(f"Aceptando la transacción n: {current_trans}")
        msg = f":accept {nickname} {current_trans}"
        client.send(msg.encode("UTF-8", errors="ignore"))
        
def reject():
    global nickname
    global current_trans
    msg = f":reject {nickname} {current_trans}"
    client.send(msg.encode("UTF-8", errors = "ignore"))

def receive():
    global nickname
    global current_trans
    while True:
        try:
            message = client.recv(1024).decode("UTF-8", errors="ignore")
            with open("a.txt", "a") as f: f.write(message)
            if message == "NICK":
                client.send(nickname.encode("UTF-8", errors="ignore"))
            elif message == "NICK_TAKEN":
                print("Nickname ocupado.")
                nickname = input("Ingresa uno nuevo: ")
                client.send(nickname.encode("UTF-8", errors="ignore"))
                continue
            elif message == "EXIT":
                break
            elif message.startswith(":transaction"):
                current_trans=(int(message.split(" ")[1]))

            elif message.startswith("accept:"):
                current_trans = None
            elif message.startswith("reject:"):
                current_trans = None
            else:
                print(message)
        except:
            print("Adios!")
            client.close()
            break


def write():
    while 1:
        content = input()
        message = f"{nickname}: {content}"
        if content == ":q":
            client.send(":q".encode("UTF-8", errors="ignore"))
            client.close()
            break
        elif ":offer" in content:
            if (len(content.split(" ")) == 4):
                params = content.split(" ")
                nick_from = nickname
                nick_to, my_art, to_art = params[1], params[2], params[3]
                initTrans(nick_from, nick_to, my_art, to_art)
                
        elif content == ":accept":
            accept()
        elif content == ":reject":
            if current_trans!=None:
                reject()
                print("Has rechazado tu transaccion pendiente!")
            else:
                print("No tienes ninguna transaccion pendiente")
        else:
            client.send(message.encode("UTF-8", errors="ignore"))
            print(f"Yo: {replace_kaomojis(content)}")


if __name__ == "__main__":
    nickname = input("Choose a nickname: ")

    client = socket.socket(socket. AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()