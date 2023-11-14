host = "127.0.0.1" 
port = 8000

artefactos = {
    "1": "Rollo enano I",
    "2": "Rollo enano II",
    "3": "Rollo enano III",
    "4": "Rollo enano IV",
    "5": "\u00c1nfora quebrada",
    "6": "Punta de flecha",
    "7": "Mu\u00f1eco antiguo",
    "8": "Joyer\u00eda \u00e9lfica",
    "9": "Palo de mascar",
    "10": "Abanico ornamental",
    "11": "Huevo de dinosaurio",
    "12": "Disco raro",
    "13": "Espada antigua",
    "14": "Cuchara oxidada",
    "15": "Espuela oxidada",
    "16": "Engranaje oxidado",
    "17": "Estatua de gallina",
    "18": "Semilla milenaria",
    "19": "Herramienta prehist\u00f3rica",
    "20": "Estrella de mar seca",
    "21": "Ancla",
    "22": "Trocitos de cristal",
    "23": "Flauta de hueso",
    "24": "Hacha prehist\u00f3rica",
    "25": "Yelmo enano",
    "26": "Dispositivo enano",
    "27": "Tambor antiguo",
    "28": "M\u00e1scara dorada",
    "29": "Reliquia dorada",
    "30": "Mu\u00f1eco extra\u00f1o (verde)",
    "31": "Mu\u00f1eco extra\u00f1o (amarillo)",
    "32": "Es\u00e1pula prehist\u00f3rica",
    "33": "Tibia prehist\u00f3rica",
    "34": "Cr\u00e1neo prehist\u00f3rico",
    "35": "Mano esquel\u00e9tica",
    "36": "Costilla prehist\u00f3rica",
    "37": "V\u00e9rtebra prehist\u00f3rica",
    "38": "Cola esquel\u00e9tica",
    "39": "F\u00f3sil de nautilo",
    "40": "F\u00f3sil de anfibio",
    "41": "F\u00f3sil de palmera",
    "42": "Trilobites"
}

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
    print(l)
    for i in l:
        message+= f"{artefactos[str(i)]}\n"
    print(message)
    return message