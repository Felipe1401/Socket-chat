host = "127.0.0.2" 
port = 55_551

import re

with open("artefactos.json","r") as f:
    artefactos = f.read()
artefactos = eval(artefactos)

kaomojis = {
    ":smile": ":)",
    ":angry": ">:(",
    ":combito": "Q('- 'Q)",
    ":larva": "(:o)OOOooo",
    ":arrow":"|----->",
}

def replace_kaomojis(message, emojis=kaomojis):
    for key, value in emojis.items():
        message = message.replace(key, value)
    return message

def id_to_name(items:list):
    items = list(map(str, items))
    for i in range(len(items)):
        try:
            items[i] = artefactos[items[i]]
        except:
            pass
    items = ", ".join(items)
    items = list(items)
    for i in range(len(items)):
        if items[-i] == ",":
            items[-i] = " y"
            break
    return "".join(items)

def get_inventory(hash:dict, nickname:str):
    message = "Tu inventario es:\n"
    l = hash[nickname]["inventario"]
    for i in l:
        message+= f"{artefactos[str(i)]}\n"
    return message

def id_to_list(texto):
    numeros_encontrados = re.findall(r'\d+', texto)
    numeros = [int(numero) for numero in numeros_encontrados]
    return numeros