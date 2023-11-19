import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from artefactos import *

artefactos = []
current_trans = None
global nickname
def initTrans(nickname_from,nickname_to, my_itemid, to_itemid):
    msg = f":offer {nickname_from} {nickname_to} {my_itemid} {to_itemid}" 
    if current_trans == None and nickname_to!=nickname:
        print("Puedes realizar la transaccion")
        client.send(msg.encode("UTF-8", errors = "ignore"))
    else:
        print("Revisa si tienes una transaccion pendiete o el id del remitente!")
def accept():
    global nickname
    global current_trans
    if(current_trans!=None):
        print(f"Aceptando la transacción n: {current_trans}")
        msg = f":accept {nickname} {current_trans}"
        client.send(msg.encode("UTF-8", errors="ignore"))
        
def reject():
    global nickname
    global current_trans
    if (current_trans!=None):
        msg = f":reject {nickname} {current_trans}"
        client.send(msg.encode("UTF-8", errors = "ignore"))

def receive():
    global nickname
    global current_trans
    while True:
        try:
            message = client.recv(1024).decode("UTF-8", errors="ignore")
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


def receive():
    global nickname
    global current_trans
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            elif message == 'NICK_TAKEN':
                nickname = simpledialog.askstring("Nickname", "Por favor elija otro nombre", parent=root)
                client.send(nickname.encode('utf-8'))
            else:
                # Actualizar la interfaz de usuario con el mensaje recibido
                messages_text.config(state='normal')
                messages_text.config(state='normal')
                messages_text.insert(tk.END, message + '\n')
                messages_text.see(tk.END)
                messages_text.config(state='disabled')
    
        except:
            print("An error occured!")
            client.close()
            break
cont = 0

def send_message():
    global cont
    content = message_input.get()
    message = f'{nickname}: {content}'
    client.send(message.encode('utf-8'))
    
    messages_text.config(state='normal')
    messages_text.config(state='normal')
    my_message = message.replace(nickname, "Yo")
    messages_text.insert(tk.END, replace_kaomojis(my_message) + '\n')
    messages_text.config(state='disabled')

    message_input.delete(0, tk.END)


root = tk.Tk()
root.title("Chat Client")

messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)
h_scrollbar = tk.Scrollbar(messages_frame, orient='horizontal')
messages_text = tk.Text(messages_frame, height=15, width=50, wrap='word', yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill='y')
h_scrollbar.pack(side=tk.BOTTOM, fill='x')
messages_text.pack(side=tk.LEFT, fill='both', expand=True)

messages_frame.pack(fill='both', expand=True)


message_input = tk.Entry(root, width=50)
message_input.pack()


send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()
root.bind('<Return>', lambda event: send_message())


nickname = simpledialog.askstring("Nickname", "Elija un nombre", parent=root)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


receive_thread = threading.Thread(target=receive)
receive_thread.start()



messages_text.config(state='disabled')
root.mainloop()