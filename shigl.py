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
___
print("SHIGL v0.2 Started")

variables = {}

while True:
    code = input("SHIGL> ")

    if code == "exit":
        break

    elif code.startswith("var "):
        try:
            left, right = code[4:].split("=")
            name = left.strip()
            value = right.strip().replace('"', '')
            variables[name] = value
        except:
            print("خطا در متغیر")

    elif code.startswith("say "):
        text = code[4:].strip()

        if text in variables:
            print(variables[text])
        else:
            print(text.replace('"', ''))

    else:
        print("دستور ناشناخته")
