# رفتن به پوشه پروژه
cd SHIGL_V2

# نصب به صورت editable (برای توسعه)
pip install -e .

# یا نصب کامل
pip install .

# نصب با pip3
pip3 install -e .# SHIGL Language

SHIGL is a simple programming language created for learning and experimentation.

## Features
- say (print text)
- ask (input)
- time (show time)

## Run
python interpreter.py# SHIGL



# SHIGL

Smart High-speed Intelligent General Language

SHIGL is an experimental programming language project focused on simplicity, speed, and ease of learning.

---

## Vision

SHIGL aims to provide a simple syntax for beginners while remaining powerful enough for advanced applications.

Goals:

- Easy to learn
- Easy to read
- Fast execution
- Open Source
- Cross Platform
- Expandable architecture

---

## Current Status

Version: 0.1 Alpha

Implemented:

- say
- exit

In Development:

- var
- if
- loop
- func
- modules
- compiler

---

## Example

```shigl
say "Hello World"
```

Output:

```text
Hello World
```

---

## Syntax Roadmap

### Version 0.1

```shigl
say "Hello"
```

### Version 0.2

```shigl
var name = "Erfan"
say name
```

### Version 0.3

```shigl
if score > 10
```

### Version 0.4

```shigl
add 5 10
```

### Version 0.5

```shigl
loop 5 say "Hello"
```

### Version 0.6

```shigl
func hello
```

### Version 0.7

```shigl
run app.shigl
```

### Version 0.8

```shigl
list users
```

### Version 0.9

```shigl
import math
```

### Version 1.0

- Compiler
- Virtual Machine
- GUI
- Network
- Database
- AI Library

---

## Project Structure

```text
SHIGL/
│
├── README.md
├── LICENSE
├── interpreter.py
├── docs/
├── examples/
├── tests/
├── compiler/
├── vm/
└── stdlib/
```

---

## File Extension

```text
.shigl
```

Example:

```text
hello.shigl
game.shigl
app.shigl
```

---

## License

MIT License

---

## Author

Erfan Shirani

Founder of SHIGL Programming Language

---

## Future

SHIGL 1.0

- High Performance Runtime
- Native Compiler
- Package Manager
- Desktop Applications
- Mobile Applications
- Artificial Intelligence Tools

The journey starts with a single command:

```shigl
say "Hello SHIGL"
```
Current Version: 0.1 Alpha
SHIGL 0.2
---------
✓ var
✓ say variable
var name = "Erfan"
say name
---
# SHIGL 2.0 - زبان برنامه‌نویسی پیشرفته

> **نسخه جدید**: بازنویسی کامل با معماری توکن‌محور (Lexer-based)

## ویژگی‌های جدید
- ✅ پشتیبانی از اعداد اعشاری
- ✅ مدیریت خطای پیشرفته
- ✅ معماری ماژولار و قابل گسترش
- ✅ پشتیبانی از رشته‌های با escape
- ✅ نمایش پیام‌های خطای دقیق

## نصب و اجرا
```bash
python shigl.py

┌─────────────────────────────────────────────┐
│              کد SHIGL (.shigl)               │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│    Lexer (تجزیه‌گر واژگان) - مستقل          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│    Parser (تجزیه‌گر دستوری) - مستقل          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│    AST (درخت نحوی انتزاعی) - مستقل           │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│    Code Generator (تولید کد)                │
│    ┌────────────────────────────────────┐   │
│    │  Java / Kotlin / C / Python / WASM │   │
│    └────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              خروجی نهایی                     │
│    📱 Android APK                          │
│    🌐 WebAssembly                         │
│    💻 Native Executable                   │
└─────────────────────────────────────────────┘
