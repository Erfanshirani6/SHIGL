#!/usr/bin/env python3
# ============================================
# SHIGL v1.0 - Advanced Language Interpreter
# با پشتیبانی کامل از ساخت اپلیکیشن اندروید
# ============================================

import sys
import os
import re
import subprocess
import shutil
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ============================================
# بخش ۱: توکن‌ها (Tokenization)
# ============================================

class TokenType:
    """انواع توکن‌های زبان"""
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    OPERATOR = 'OPERATOR'
    COMMENT = 'COMMENT'
    EOF = 'EOF'

class Token:
    """یک توکن شامل نوع، مقدار و موقعیت"""
    def __init__(self, type_: str, value: Any, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line})"

class Lexer:
    """تجزیه‌کننده واژگان - تبدیل کد به توکن"""
    
    KEYWORDS = {
        'say', 'var', 'ask', 'if', 'else', 'elif', 'while', 'for',
        'func', 'return', 'import', 'class', 'try', 'catch',
        'true', 'false', 'null', 'and', 'or', 'not',
        'time', 'vars', 'clear', 'help', 'exit',
        'android', 'build', 'run', 'activity', 'resource', 'manifest'
    }
    
    OPERATORS = {
        '=', '==', '!=', '>', '<', '>=', '<=',
        '+', '-', '*', '/', '%', '**'
    }
    
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[Token]:
        """تبدیل کل کد به لیست توکن‌ها"""
        while self.pos < len(self.code):
            char = self.code[self.pos]
            
            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue
            
            if char == '#':
                self._read_comment()
                continue
            
            if char.isdigit() or (char == '.' and self._peek().isdigit()):
                self.tokens.append(self._read_number())
                continue
            
            if char in '"\'':
                self.tokens.append(self._read_string())
                continue
            
            if char in self.OPERATORS:
                self.tokens.append(self._read_operator())
                continue
            
            if char.isalpha() or char == '_':
                self.tokens.append(self._read_identifier())
                continue
            
            raise SyntaxError(f"کاراکتر ناشناخته در خط {self.line}, ستون {self.column}: '{char}'")
        
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.line, self.column))
        return self.tokens
    
    def _peek(self, offset: int = 1) -> str:
        pos = self.pos + offset
        return self.code[pos] if pos < len(self.code) else ''
    
    def _read_comment(self):
        self.pos += 1
        self.column += 1
        while self.pos < len(self.code) and self.code[self.pos] != '\n':
            self.pos += 1
            self.column += 1
    
    def _read_number(self) -> Token:
        num = ''
        start_column = self.column
        
        while self.pos < len(self.code):
            char = self.code[self.pos]
            if char.isdigit() or char == '.':
                num += char
                self.pos += 1
                self.column += 1
            else:
                break
        
        value = float(num) if '.' in num else int(num)
        return Token(TokenType.NUMBER, value, self.line, start_column)
    
    def _read_string(self) -> Token:
        quote = self.code[self.pos]
        self.pos += 1
        self.column += 1
        
        string = ''
        start_column = self.column
        
        while self.pos < len(self.code):
            char = self.code[self.pos]
            
            if char == '\\':
                self.pos += 1
                self.column += 1
                if self.pos < len(self.code):
                    esc = self.code[self.pos]
                    if esc == 'n':
                        string += '\n'
                    elif esc == 't':
                        string += '\t'
                    else:
                        string += esc
                self.pos += 1
                self.column += 1
            elif char == quote:
                self.pos += 1
                self.column += 1
                break
            else:
                string += char
                self.pos += 1
                self.column += 1
        
        return Token(TokenType.STRING, string, self.line, start_column)
    
    def _read_operator(self) -> Token:
        start_column = self.column
        op = self.code[self.pos]
        self.pos += 1
        self.column += 1
        
        if self.pos < len(self.code):
            next_char = self.code[self.pos]
            if op + next_char in self.OPERATORS:
                op += next_char
                self.pos += 1
                self.column += 1
        
        return Token(TokenType.OPERATOR, op, self.line, start_column)
    
    def _read_identifier(self) -> Token:
        ident = ''
        start_column = self.column
        
        while self.pos < len(self.code):
            char = self.code[self.pos]
            if char.isalnum() or char == '_':
                ident += char
                self.pos += 1
                self.column += 1
            else:
                break
        
        token_type = TokenType.KEYWORD if ident in self.KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, ident, self.line, start_column)

# ============================================
# بخش ۲: مفسر اصلی
# ============================================

class SHIGLInterpreter:
    """مفسر اصلی SHIGL با پشتیبانی از اندروید"""
    
    def __init__(self, debug: bool = False):
        self.variables = {}
        self.functions = {}
        self.output_buffer = []
        self.debug = debug
        self.line_number = 0
        self.current_path = os.getcwd()
    
    def execute_file(self, filename: str) -> bool:
        """اجرای فایل .shigl"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.execute(code, filename=filename)
        except FileNotFoundError:
            print(f"❌ فایل {filename} پیدا نشد")
            return False
        except Exception as e:
            print(f"❌ خطا در اجرای فایل: {e}")
            return False
    
    def execute(self, code: str, filename: str = '<repl>') -> bool:
        """اجرای کد SHIGL"""
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            if self.debug:
                print("🔍 توکن‌ها:")
                for token in tokens[:-1]:
                    print(f"  {token}")
                print()
            
            i = 0
            while i < len(tokens) - 1:
                token = tokens[i]
                
                if token.type == TokenType.KEYWORD:
                    result = self._execute_command(tokens, i)
                    if result is not None:
                        if isinstance(result, tuple) and len(result) == 2:
                            output, i = result
                            if output is not None:
                                print(output)
                        else:
                            if result is not None:
                                print(result)
                            i += 1
                    else:
                        i += 1
                else:
                    i += 1
            
            return True
            
        except SyntaxError as e:
            print(f"❌ خطای نحوی: {e}")
            return False
        except Exception as e:
            print(f"❌ خطای اجرا: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return False
    
    def _execute_command(self, tokens: List[Token], pos: int) -> Optional[Any]:
        """اجرای یک دستور"""
        token = tokens[pos]
        cmd = token.value
        
        # دستورات پایه
        if cmd == 'say':
            return self._cmd_say(tokens, pos)
        elif cmd == 'var':
            return self._cmd_var(tokens, pos)
        elif cmd == 'ask':
            return self._cmd_ask(tokens, pos)
        elif cmd == 'time':
            return self._cmd_time(tokens, pos)
        elif cmd == 'vars':
            return self._cmd_vars(tokens, pos)
        elif cmd == 'clear':
            return self._cmd_clear(tokens, pos)
        elif cmd == 'help':
            return self._cmd_help(tokens, pos)
        elif cmd in ['add', 'sub', 'mul', 'div']:
            return self._cmd_math(tokens, pos, cmd)
        elif cmd == 'if':
            return self._cmd_if(tokens, pos)
        elif cmd == 'cd':
            return self._cmd_cd(tokens, pos)
        
        # ============ دستورات اندروید ============
        elif cmd == 'android':
            return self._cmd_android(tokens, pos)
        elif cmd == 'build':
            return self._cmd_build(tokens, pos)
        elif cmd == 'run':
            return self._cmd_run(tokens, pos)
        elif cmd == 'activity':
            return self._cmd_activity(tokens, pos)
        elif cmd == 'resource':
            return self._cmd_resource(tokens, pos)
        elif cmd == 'manifest':
            return self._cmd_manifest(tokens, pos)
        
        elif cmd == 'exit':
            sys.exit(0)
        else:
            return f"❌ دستور ناشناخته: {cmd}"
    
    def _get_value(self, token: Token) -> Any:
        """دریافت مقدار از توکن"""
        if token.type == TokenType.NUMBER:
            return token.value
        elif token.type == TokenType.STRING:
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            return self.variables.get(token.value, token.value)
        elif token.type == TokenType.KEYWORD:
            if token.value == 'true': return True
            if token.value == 'false': return False
            if token.value == 'null': return None
        return token.value
    
    def _cmd_say(self, tokens: List[Token], pos: int) -> Optional[str]:
        if pos + 1 >= len(tokens):
            return "❌ say نیاز به یک مقدار دارد"
        value_token = tokens[pos + 1]
        value = self._get_value(value_token)
        return str(value)
    
    def _cmd_var(self, tokens: List[Token], pos: int) -> Optional[str]:
        if pos + 3 >= len(tokens):
            return "❌ فرمت: var name = value"
        
        name_token = tokens[pos + 1]
        if name_token.type != TokenType.IDENTIFIER:
            return f"❌ نام متغیر نامعتبر: {name_token.value}"
        
        if tokens[pos + 2].value != '=':
            return "❌ انتظار '=' بود"
        
        value_token = tokens[pos + 3]
        value = self._get_value(value_token)
        
        self.variables[name_token.value] = value
        return f"✅ {name_token.value} = {value}"
    
    def _cmd_ask(self, tokens: List[Token], pos: int) -> Optional[str]:
        if pos + 1 >= len(tokens):
            return "❌ ask نیاز به نام متغیر دارد"
        
        var_name = tokens[pos + 1].value
        user_input = input(f"{var_name}: ")
        
        if user_input.isdigit():
            user_input = int(user_input)
        elif user_input.replace('.', '').isdigit():
            user_input = float(user_input)
        elif user_input.lower() == 'true':
            user_input = True
        elif user_input.lower() == 'false':
            user_input = False
        elif user_input.lower() == 'null':
            user_input = None
        
        self.variables[var_name] = user_input
        return f"✅ {var_name} = {user_input}"
    
    def _cmd_time(self, tokens: List[Token], pos: int) -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def _cmd_vars(self, tokens: List[Token], pos: int) -> str:
        if not self.variables:
            return "📦 هیچ متغیری تعریف نشده"
        
        result = "📦 متغیرهای تعریف‌شده:\n"
        for name, value in self.variables.items():
            result += f"  {name} = {value} ({type(value).__name__})\n"
        return result.strip()
    
    def _cmd_clear(self, tokens: List[Token], pos: int) -> str:
        count = len(self.variables)
        self.variables.clear()
        return f"🧹 {count} متغیر پاک شد"
    
    def _cmd_cd(self, tokens: List[Token], pos: int) -> str:
        """تغییر دایرکتوری"""
        if pos + 1 >= len(tokens):
            return f"📁 مسیر فعلی: {self.current_path}"
        
        path = tokens[pos + 1].value
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            self.current_path = os.getcwd()
            return f"📁 مسیر تغییر کرد به: {self.current_path}"
        else:
            return f"❌ مسیر {path} وجود ندارد"
    
    def _cmd_math(self, tokens: List[Token], pos: int, op: str) -> Optional[str]:
        if pos + 2 >= len(tokens):
            return f"❌ {op} نیاز به دو مقدار دارد"
        
        a = self._get_value(tokens[pos + 1])
        b = self._get_value(tokens[pos + 2])
        
        try:
            a = float(a) if not isinstance(a, (int, float)) else a
            b = float(b) if not isinstance(b, (int, float)) else b
        except:
            return f"❌ عملوندها باید عدد باشند: {a}, {b}"
        
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            return f"❌ عملوندها باید عدد باشند: {a}, {b}"
        
        operations = {
            'add': a + b,
            'sub': a - b,
            'mul': a * b,
            'div': a / b if b != 0 else None
        }
        
        result = operations.get(op)
        if result is None:
            return "❌ تقسیم بر صفر!"
        
        return f"📊 {a} {op} {b} = {result}"
    
    def _cmd_if(self, tokens: List[Token], pos: int) -> Optional[str]:
        if pos + 3 >= len(tokens):
            return "❌ فرمت: if a == b"
        
        a = self._get_value(tokens[pos + 1])
        op = tokens[pos + 2].value
        b = self._get_value(tokens[pos + 3])
        
        if op == '==':
            result = str(a) == str(b)
        elif op == '!=':
            result = str(a) != str(b)
        elif op == '>':
            result = float(a) > float(b)
        elif op == '<':
            result = float(a) < float(b)
        elif op == '>=':
            result = float(a) >= float(b)
        elif op == '<=':
            result = float(a) <= float(b)
        else:
            return f"❌ عملگر نامشخص: {op}"
        
        return f"📊 شرط: {result}"
    
    # ============================================
    # دستورات اندروید - بخش اصلی
    # ============================================
    
    def _cmd_android(self, tokens: List[Token], pos: int) -> str:
        """ایجاد پروژه جدید اندروید"""
        if pos + 1 >= len(tokens):
            return "❌ فرمت: android create <project_name>"
        
        project_name = tokens[pos + 1].value
        
        # اعتبارسنجی نام
        if not project_name.isalnum():
            return "❌ نام پروژه باید فقط شامل حروف و اعداد باشد"
        
        project_path = os.path.join(self.current_path, project_name)
        
        if os.path.exists(project_path):
            return f"❌ پوشه {project_name} از قبل وجود دارد"
        
        try:
            # ایجاد ساختار پروژه
            self._create_android_project(project_path, project_name)
            
            return f"""
✅ پروژه اندروید {project_name} با موفقیت ایجاد شد!

📁 مسیر: {project_path}

ساختار پروژه:
  app/
    src/main/
      java/com/example/{project_name.lower()}/
        MainActivity.java
      res/
        layout/
          activity_main.xml
        values/
          strings.xml
      AndroidManifest.xml
  build.gradle
  settings.gradle

🔧 مراحل بعدی:
  1. cd {project_name}
  2. build apk
  3. run emulator
"""
        except Exception as e:
            return f"❌ خطا در ایجاد پروژه: {e}"
    
    def _create_android_project(self, project_path: str, project_name: str):
        """ایجاد فایل‌های پروژه اندروید"""
        package_name = f"com.example.{project_name.lower()}"
        
        # پوشه‌ها
        os.makedirs(os.path.join(project_path, 'app', 'src', 'main', 'java', 'com', 'example', project_name.lower()))
        os.makedirs(os.path.join(project_path, 'app', 'src', 'main', 'res', 'layout'))
        os.makedirs(os.path.join(project_path, 'app', 'src', 'main', 'res', 'values'))
        os.makedirs(os.path.join(project_path, 'app', 'src', 'main', 'res', 'drawable'))
        
        # 1. MainActivity.java
        main_activity = f'''package {package_name};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        TextView textView = findViewById(R.id.textView);
        textView.setText("Hello from SHIGL!");
    }}
}}
'''
        with open(os.path.join(project_path, 'app', 'src', 'main', 'java', 'com', 'example', project_name.lower(), 'MainActivity.java'), 'w') as f:
            f.write(main_activity)
        
        # 2. activity_main.xml
        layout_xml = '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        android:textSize="24sp"
        android:textColor="#FF6200EE" />

</LinearLayout>
'''
        with open(os.path.join(project_path, 'app', 'src', 'main', 'res', 'layout', 'activity_main.xml'), 'w') as f:
            f.write(layout_xml)
        
        # 3. strings.xml
        strings_xml = f'''<resources>
    <string name="app_name">{project_name}</string>
</resources>
'''
        with open(os.path.join(project_path, 'app', 'src', 'main', 'res', 'values', 'strings.xml'), 'w') as f:
            f.write(strings_xml)
        
        # 4. AndroidManifest.xml
        manifest_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.Light">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
'''
        with open(os.path.join(project_path, 'app', 'src', 'main', 'AndroidManifest.xml'), 'w') as f:
            f.write(manifest_xml)
        
        # 5. build.gradle (app)
        build_gradle = f'''plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 34

    defaultConfig {{
        applicationId "{package_name}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
}}
'''
        with open(os.path.join(project_path, 'app', 'build.gradle'), 'w') as f:
            f.write(build_gradle)
        
        # 6. settings.gradle
        settings_gradle = f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolutionManagement {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{project_name}"
include ':app'
'''
        with open(os.path.join(project_path, 'settings.gradle'), 'w') as f:
            f.write(settings_gradle)
        
        # 7. gradle.properties
        gradle_props = '''org.gradle.jvmargs=-Xmx2048m
android.useAndroidX=true
android.enableJetifier=true
'''
        with open(os.path.join(project_path, 'gradle.properties'), 'w') as f:
            f.write(gradle_props)
    
    def _cmd_build(self, tokens: List[Token], pos: int) -> str:
        """ساخت APK یا AAB"""
        if pos + 1 >= len(tokens):
            return "❌ فرمت: build <apk|aab>"
        
        build_type = tokens[pos + 1].value
        
        if build_type not in ['apk', 'aab']:
            return "❌ نوع ساخت نامشخص. استفاده: build apk یا build aab"
        
        project_path = self.current_path
        
        if not os.path.exists(os.path.join(project_path, 'app')):
            return f"❌ پروژه اندروید در {project_path} پیدا نشد"
        
        try:
            os.chdir(project_path)
            
            # بررسی وجود gradlew
            gradlew_path = os.path.join(project_path, 'gradlew')
            if not os.path.exists(gradlew_path):
                return "❌ فایل gradlew پیدا نشد. مطمئن شوید در مسیر پروژه هستید"
            
            # اجرای Gradle
            if build_type == 'apk':
                print("🔨 در حال ساخت APK...")
                result = subprocess.run(['./gradlew', 'assembleDebug'], 
                                       capture_output=True, text=True, cwd=project_path)
                
                if result.returncode == 0:
                    apk_path = os.path.join(project_path, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
                    if os.path.exists(apk_path):
                        size = os.path.getsize(apk_path) / 1024 / 1024
                        return f"""
✅ APK با موفقیت ساخته شد!

📱 مسیر APK: {apk_path}
📦 حجم: {size:.2f} MB

🔧 نصب روی دستگاه:
  run device
  
🌐 اجرا روی شبیه‌ساز:
  run emulator
"""
                    else:
                        return "❌ APK ساخته شد اما فایل پیدا نشد"
                else:
                    return f"❌ خطا در ساخت APK:\n{result.stderr}"
            
            elif build_type == 'aab':
                print("🔨 در حال ساخت AAB...")
                result = subprocess.run(['./gradlew', 'bundleDebug'], 
                                       capture_output=True, text=True, cwd=project_path)
                
                if result.returncode == 0:
                    aab_path = os.path.join(project_path, 'app', 'build', 'outputs', 'bundle', 'debug', 'app-debug.aab')
                    if os.path.exists(aab_path):
                        size = os.path.getsize(aab_path) / 1024 / 1024
                        return f"""
✅ AAB با موفقیت ساخته شد!

📱 مسیر AAB: {aab_path}
📦 حجم: {size:.2f} MB

📤 آپلود در Google Play Console
"""
                    else:
                        return "❌ AAB ساخته شد اما فایل پیدا نشد"
                else:
                    return f"❌ خطا در ساخت AAB:\n{result.stderr}"
                
        except Exception as e:
            return f"❌ خطا در ساخت: {e}"
    
    def _cmd_run(self, tokens: List[Token], pos: int) -> str:
        """اجرای پروژه روی شبیه‌ساز یا دستگاه"""
        if pos + 1 >= len(tokens):
            return "❌ فرمت: run <emulator|device>"
        
        run_target = tokens[pos + 1].value
        
        if run_target not in ['emulator', 'device']:
            return "❌ هدف نامشخص. استفاده: run emulator یا run device"
        
        project_path = self.current_path
        
        if not os.path.exists(os.path.join(project_path, 'app')):
            return f"❌ پروژه اندروید در {project_path} پیدا نشد"
        
        try:
            os.chdir(project_path)
            
            print(f"📱 در حال اجرا روی {run_target}...")
            
            # ساخت و نصب
            result = subprocess.run(['./gradlew', 'installDebug'], 
                                   capture_output=True, text=True, cwd=project_path)
            
            if result.returncode != 0:
                return f"❌ خطا در نصب:\n{result.stderr}"
            
            # دریافت package name
            package_name = f"com.example.{os.path.basename(project_path).lower()}"
            
            # اجرا
            run_result = subprocess.run(['adb', 'shell', 'am', 'start', 
                                        '-n', f'{package_name}/.MainActivity'],
                                      capture_output=True, text=True)
            
            if 'Error' in run_result.stderr:
                return f"⚠️  برنامه نصب شد اما خطا در اجرا:\n{run_result.stderr}"
            
            return "✅ برنامه با موفقیت اجرا شد!"
                
        except Exception as e:
            return f"❌ خطا در اجرا: {e}"
    
    def _cmd_activity(self, tokens: List[Token], pos: int) -> str:
        """ایجاد Activity جدید"""
        if pos + 1 >= len(tokens):
            return "❌ فرمت: activity <name>"
        
        activity_name = tokens[pos + 1].value
        
        if not activity_name[0].isupper():
            return "❌ نام Activity باید با حرف بزرگ شروع شود"
        
        project_path = self.current_path
        
        package_path = os.path.join(project_path, 'app', 'src', 'main', 'java', 'com', 'example')
        
        if not os.path.exists(package_path):
            return "❌ پروژه اندروید پیدا نشد"
        
        try:
            # پیدا کردن پکیج
            package_dirs = os.listdir(package_path)
            if not package_dirs:
                return "❌ پکیج پروژه پیدا نشد"
            
            package_name = f"com.example.{package_dirs[0]}"
            
            # ایجاد Activity
            activity_content = f'''package {package_name};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class {activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{activity_name.lower()});
        
        TextView textView = findViewById(R.id.textView);
        textView.setText("Activity: {activity_name}");
    }}
}}
'''
            activity_path = os.path.join(package_path, package_dirs[0], f'{activity_name}.java')
            with open(activity_path, 'w') as f:
                f.write(activity_content)
            
            # ایجاد layout
            layout_content = f'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="16dp">

    <TextView
        android:id="@+id/textView"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Activity: {activity_name}"
        android:textSize="24sp"
        android:textColor="#FF6200EE" />

</LinearLayout>
'''
            layout_path = os.path.join(project_path, 'app', 'src', 'main', 'res', 'layout', f'activity_{activity_name.lower()}.xml')
            with open(layout_path, 'w') as f:
                f.write(layout_content)
            
            return f"""
✅ Activity {activity_name} با موفقیت ایجاد شد!

📁 فایل‌های ایجاد شده:
  - {activity_path}
  - {layout_path}

🔧 برای استفاده در AndroidManifest.xml:
  <activity android:name=".{activity_name}" />
"""
        except Exception as e:
            return f"❌ خطا در ایجاد Activity: {e}"
    
    def _cmd_resource(self, tokens: List[Token], pos: int) -> str:
        """مدیریت منابع"""
        if pos + 2 >= len(tokens):
            return "❌ فرمت: resource <string|color|dimen> <name> <value>"
        
        resource_type = tokens[pos + 1].value
        
        if resource_type not in ['string', 'color', 'dimen']:
            return "❌ نوع منبع نامشخص. استفاده: resource string|color|dimen"
        
        resource_name = tokens[pos + 2].value
        
        if pos + 3 >= len(tokens):
            return "❌ مقدار منبع را وارد کنید"
        
        resource_value = tokens[pos + 3].value
        
        project_path = self.current_path
        
        if resource_type == 'string':
            strings_path = os.path.join(project_path, 'app', 'src', 'main', 'res', 'values', 'strings.xml')
            
            if not os.path.exists(strings_path):
                return "❌ فایل strings.xml پیدا نشد"
            
            try:
                with open(strings_path, 'r') as f:
                    content = f.read()
                
                new_string = f'    <string name="{resource_name}">{resource_value}</string>\n'
                content = content.replace('</resources>', new_string + '</resources>')
                
                with open(strings_path, 'w') as f:
                    f.write(content)
                
                return f"✅ رشته {resource_name} = '{resource_value}' اضافه شد"
            except Exception as e:
                return f"❌ خطا در اضافه کردن رشته: {e}"
        
        return "⚠️  فعلاً فقط resource string پشتیبانی می‌شود"
    
    def _cmd_manifest(self, tokens: List[Token], pos: int) -> str:
        """ویرایش AndroidManifest.xml"""
        if pos + 2 >= len(tokens):
            return "❌ فرمت: manifest <permission|feature> <value>"
        
        manifest_type = tokens[pos + 1].value
        
        if manifest_type not in ['permission', 'feature']:
            return "❌ نوع نامشخص. استفاده: manifest permission|feature"
        
        manifest_value = tokens[pos + 2].value
        
        project_path = self.current_path
        manifest_path = os.path.join(project_path, 'app', 'src', 'main', 'AndroidManifest.xml')
        
        if not os.path.exists(manifest_path):
            return "❌ فایل AndroidManifest.xml پیدا نشد"
        
        try:
            with open(manifest_path, 'r') as f:
                content = f.read()
            
            if manifest_type == 'permission':
                permission = f'    <uses-permission android:name="{manifest_value}" />\n'
                content = content.replace('<manifest', f'<manifest\n{permission}')
                
            elif manifest_type == 'feature':
                feature = f'    <uses-feature android:name="{manifest_value}" />\n'
                content = content.replace('<application', f'{feature}    <application')
            
            with open(manifest_path, 'w') as f:
                f.write(content)
            
            return f"✅ {manifest_type} {manifest_value} اضافه شد"
        except Exception as e:
            return f"❌ خطا: {e}"
    
    def _cmd_help(self, tokens: List[Token], pos: int) -> str:
        """راهنمای کامل"""
        return """
📚 راهنمای SHIGL v1.0

دستورات پایه:
  say "Hello"     - چاپ متن
  var x = 10      - تعریف متغیر
  ask name        - دریافت ورودی
  time            - نمایش زمان
  cd path         - تغییر مسیر
  vars            - نمایش متغیرها
  clear           - پاک کردن متغیرها

عملیات ریاضی:
  add x 5         - جمع
  sub x 3         - تفریق
  mul x 2         - ضرب
  div x 4         - تقسیم

شرط‌ها:
  if x == 5       - بررسی برابری
  if x > 10       - بررسی بزرگ‌تر

🚀 دستورات اندروید:
  android create <name>     - ایجاد پروژه جدید
  build apk                 - ساخت APK
  build aab                 - ساخت AAB
  run emulator              - اجرا روی شبیه‌ساز
  run device                - اجرا روی دستگاه
  activity <name>           - ایجاد Activity جدید
  resource string <n> <v>   - اضافه کردن رشته
  manifest permission <n>   - اضافه کردن دسترسی

📱 مثال:
  android create MyApp
  cd MyApp
  build apk
  run emulator
"""

# ============================================
# بخش ۳: اجرای اصلی
# ============================================

def main():
    """ورودی اصلی برنامه"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SHIGL Programming Language')
    parser.add_argument('file', nargs='?', help='فایل .shigl برای اجرا')
    parser.add_argument('--debug', action='store_true', help='حالت دیباگ')
    parser.add_argument('--version', action='version', version='SHIGL v1.0')
    
    args = parser.parse_args()
    
    interpreter = SHIGLInterpreter(debug=args.debug)
    
    if args.file:
        if not args.file.endswith('.shigl'):
            print("⚠️  فایل باید پسوند .shigl داشته باشد")
        interpreter.execute_file(args.file)
        return
    
    print("=" * 60)
    print("🚀 SHIGL v1.0 - Advanced Language Interpreter")
    print("📱 با پشتیبانی کامل از ساخت اپلیکیشن اندروید")
    print("=" * 60)
    print("💡 برای راهنما 'help' را تایپ کنید")
    print("📁 مسیر فعلی:", os.getcwd())
    print("=" * 60)
    
    while True:
        try:
            code = input("\nSHIGL> ").strip()
            if not code:
                continue
            
            if code == 'exit':
                print("👋 Goodbye!")
                break
            
            interpreter.execute(code)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ خطای غیرمنتظره: {e}")
            if args.debug:
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    main()
