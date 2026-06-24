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
___
print("SHIGL v0.3 Started")

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
            print(text.replace('"', ''))

    # شرط
    elif code.startswith("if "):

        condition = code[3:]

        try:

            if ">" in condition:

                left, right = condition.split(">")

                left = left.strip()
                right = right.strip()

                if left in variables:
                    left = variables[left]

                if right in variables:
                    right = variables[right]

                if int(left) > int(right):
                    print("TRUE")
                else:
                    print("FALSE")

            elif "<" in condition:

                left, right = condition.split("<")

                left = left.strip()
                right = right.strip()

                if left in variables:
                    left = variables[left]

                if right in variables:
                    right = variables[right]

                if int(left) < int(right):
                    print("TRUE")
                else:
                    print("FALSE")

            elif "==" in condition:

                left, right = condition.split("==")

                left = left.strip()
                right = right.strip()

                if left in variables:
                    left = variables[left]

                if right in variables:
                    right = variables[right]

                if str(left) == str(right):
                    print("TRUE")
                else:
                    print("FALSE")

        except:
            print("خطا در شرط")

    else:
        print("دستور ناشناخته")
