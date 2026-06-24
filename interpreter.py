# SHIGL Interpreter v0.1

print("SHIGL Language Started")

while True:
    code = input("SHIGL> ")

    if code == "exit":
        break

    elif code.startswith("say "):
        print(code[4:].replace('"', ''))

    elif code.startswith("ask "):
        var = code[4:]
        value = input(var + ": ")
        print(value)

    elif code == "time":
        from datetime import datetime
        print(datetime.now().strftime("%H:%M:%S"))

    else:
        print("Unknown command")
