print("SHIGL v0.4 Started 🚀")

variables = {}

while True:

    code = input("SHIGL> ")

    if code == "exit":
        break

    # متغیر
    elif code.startswith("var "):

        try:
            left, right = code[4:].split("=")

            name = left.strip()
            value = right.strip().replace('"', '')

            if value.isdigit():
                value = int(value)

            variables[name] = value

        except:
            print("خطا در متغیر")

    # چاپ
    elif code.startswith("say "):

        text = code[4:].strip()

        if text in variables:
            print(variables[text])
        else:
            print(text)

    # جمع
    elif code.startswith("add "):

        try:
            _, a, b = code.split()

            if a in variables:
                a = variables[a]

            if b in variables:
                b = variables[b]

            print(int(a) + int(b))

        except:
            print("خطا در add")

    # تفریق
    elif code.startswith("sub "):

        try:
            _, a, b = code.split()

            if a in variables:
                a = variables[a]

            if b in variables:
                b = variables[b]

            print(int(a) - int(b))

        except:
            print("خطا در sub")

    # ضرب
    elif code.startswith("mul "):

        try:
            _, a, b = code.split()

            if a in variables:
                a = variables[a]

            if b in variables:
                b = variables[b]

            print(int(a) * int(b))

        except:
            print("خطا در mul")

    # تقسیم
    elif code.startswith("div "):

        try:
            _, a, b = code.split()

            if a in variables:
                a = variables[a]

            if b in variables:
                b = variables[b]

            print(int(a) / int(b))

        except:
            print("خطا در div")

    # شرط
    elif code.startswith("if "):

        try:

            condition = code[3:]

            if "==" in condition:

                a, b = condition.split("==")

                a = a.strip()
                b = b.strip()

                if a in variables:
                    a = variables[a]

                if b in variables:
                    b = variables[b]

                print(str(a) == str(b))

            elif "!=" in condition:

                a, b = condition.split("!=")

                a = a.strip()
                b = b.strip()

                if a in variables:
                    a = variables[a]

                if b in variables:
                    b = variables[b]

                print(str(a) != str(b))

        except:
            print("خطا در شرط")

    else:
        print("دستور ناشناخته")
        ---
        SHIGL> ask name
    while True:

    code = input("SHIGL> ")

    if code == "exit":
        break

    elif code.startswith("say "):
        ...

    elif code.startswith("ask "):
        name = code[4:].strip()
        value = input(name + ": ")
        variables[name] = value
