import socket
import threading
from artefactos import *

artefactos = []
def receive():
    global nickname
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
            
            #elif message == "INVENTORY_REQUEST":
                #print("[SERVER] Cuéntame, ¿qué artefactos tienes?")
                #inventory = input("id: ")
                #client.send(inventory.encode("UTF-8", errors="ignore"))
            
            else:
                print(message)
        except:
            print("An error occurred!")
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