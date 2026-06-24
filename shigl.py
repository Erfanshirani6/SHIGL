print("SHIGL Started")

while True:
    code = input("SHIGL> ")

    if code == "exit":
        break

    elif code.startswith("say "):
        print(code[4:].replace('"', ''))

    else:
        print("دستور ناشناخته")
___
print("SHIGL Started")

while True:
    code = input("SHIGL> ")

    if code == "exit":
        break

    elif code.startswith("say "):
        print(code[4:].replace('"', ''))

    else:
        print("دستور ناشناخته")
