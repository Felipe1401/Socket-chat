dict = {}
nick_from = "J"
nick_to = "M"
dict[0] = {"state": 1, nick_from: "accepted", nick_to: "accepted"}

for key,values in dict[0].items():
    trigger = 0
    print(f"{key} : {values}")
    if values != "accepted":
        trigger = 1
        break

print(list(dict[0].keys())[1:])