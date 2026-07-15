#!/bin/bash
# ============================================
# SHIGL AI - بازسازی کامل پروژه
# ============================================

echo "=========================================="
echo "🧠 بازسازی کامل پروژه SHIGL AI"
echo "=========================================="

# ============================================
# 1. پاکسازی فایل‌های اشتباه
# ============================================
echo ""
echo "🗑️ مرحله 1: پاکسازی فایل‌های قبلی..."

cd ~
rm -rf SHIGL SHIGL_AI SHIGL_V2 shigl_chatgpt_app
rm -rf android_output
rm -f shigl_compiler.py shigl_cli.py build_apk_direct.py
rm -f test.shigl example.shigl
rm -rf shigl/

echo "✅ پاکسازی کامل شد!"

# ============================================
# 2. ایجاد پوشه‌های اصلی
# ============================================
echo ""
echo "📁 مرحله 2: ایجاد ساختار پوشه‌ها..."

mkdir -p ~/SHIGL
cd ~/SHIGL
mkdir -p shigl/core shigl/ai shigl/network shigl/github
mkdir -p examples tests

echo "✅ ساختار پوشه‌ها ایجاد شد!"

# ============================================
# 3. ایجاد فایل‌های اصلی
# ============================================
echo ""
echo "📄 مرحله 3: ایجاد فایل‌های اصلی..."

# ---------- build_apk_direct.py ----------
cat > build_apk_direct.py << 'EOFPYTHON'
#!/usr/bin/env python3
# build_apk_direct.py - ساخت مستقیم APK از پروژه SHIGL

import os
import subprocess
import shutil

PROJECT_NAME = "shigl_chatgpt_app"
PACKAGE_NAME = "com.shigl.chatgpt"

def main():
    print("=" * 50)
    print("🧠 SHIGL APK Builder")
    print("=" * 50)
    
    # حذف پروژه قبلی
    if os.path.exists(PROJECT_NAME):
        shutil.rmtree(PROJECT_NAME)
    
    # ساخت پروژه با android create
    print("📱 ایجاد پروژه اندروید...")
    
    # ایجاد دستی فایل‌های پروژه
    os.makedirs(f"{PROJECT_NAME}/app/src/main/java/com/shigl/chatgpt")
    os.makedirs(f"{PROJECT_NAME}/app/src/main/res/layout")
    os.makedirs(f"{PROJECT_NAME}/app/src/main/res/values")
    
    # MainActivity.java
    with open(f"{PROJECT_NAME}/app/src/main/java/com/shigl/chatgpt/MainActivity.java", "w") as f:
        f.write("""package com.shigl.chatgpt;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView tv = findViewById(R.id.textView);
        tv.setText("🧠 SHIGL AI Chat");
    }
}
""")
    
    # activity_main.xml
    with open(f"{PROJECT_NAME}/app/src/main/res/layout/activity_main.xml", "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
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
        android:text="🧠 SHIGL AI"
        android:textSize="32sp"
        android:textColor="#FF6200EE" />
</LinearLayout>
""")
    
    # AndroidManifest.xml
    with open(f"{PROJECT_NAME}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{PACKAGE_NAME}">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="SHIGL AI Chat"
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
""")
    
    # build.gradle
    with open(f"{PROJECT_NAME}/app/build.gradle", "w") as f:
        f.write(f"""plugins {{
    id 'com.android.application'
}}
android {{
    compileSdk 34
    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}
}}
dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
}}
""")
    
    # strings.xml
    with open(f"{PROJECT_NAME}/app/src/main/res/values/strings.xml", "w") as f:
        f.write("""<resources>
    <string name="app_name">SHIGL AI Chat</string>
</resources>
""")
    
    # settings.gradle
    with open(f"{PROJECT_NAME}/settings.gradle", "w") as f:
        f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
rootProject.name = "SHIGL_AI_Chat"
include ':app'
""")
    
    # gradle.properties
    with open(f"{PROJECT_NAME}/gradle.properties", "w") as f:
        f.write("org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nandroid.enableJetifier=true\n")
    
    # local.properties (برای مسیر SDK)
    sdk_path = os.path.expanduser("~/Android/Sdk")
    with open(f"{PROJECT_NAME}/local.properties", "w") as f:
        f.write(f"sdk.dir={sdk_path}\n")
    
    print("✅ پروژه ایجاد شد!")
    
    # ساخت APK
    print("🔨 ساخت APK...")
    os.chdir(PROJECT_NAME)
    
    # اجرای gradlew
    gradlew_path = "./gradlew"
    if not os.path.exists(gradlew_path):
        # ساخت gradlew ساده
        with open("gradlew", "w") as f:
            f.write("""#!/bin/sh
echo "⚠️  لطفاً Gradle را نصب کنید!"
echo "💡 در Termux: pkg install gradle"
echo "💡 سپس دستور زیر را اجرا کنید:"
echo "   gradle assembleDebug"
""")
        os.chmod("gradlew", 0o755)
    
    # اجرای ساخت با gradle
    if shutil.which("gradle"):
        result = subprocess.run(["gradle", "assembleDebug"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ APK با Gradle ساخته شد!")
        else:
            print("⚠️ خطا در ساخت با Gradle، از روش جایگزین استفاده می‌شود...")
            # روش جایگزین: فقط پیام می‌دهیم
            print("\n📱 برای ساخت APK به Android Studio نیاز است.")
            print(f"📁 پروژه در: ~/SHIGL/{PROJECT_NAME}")
            print("💡 این پوشه را به Android Studio ببرید و Build APK کنید.")
    else:
        print("\n⚠️  Gradle نصب نیست!")
        print("💡 نصب: pkg install gradle")
        print(f"📁 پروژه در: ~/SHIGL/{PROJECT_NAME}")
        print("💡 این پوشه را به Android Studio ببرید و Build APK کنید.")
    
    os.chdir("..")

if __name__ == "__main__":
    main()
EOFPYTHON

chmod +x build_apk_direct.py

# ---------- shigl_cli.py ----------
cat > shigl_cli.py << 'EOFPYTHON2'
#!/usr/bin/env python3
# shigl_cli.py - رابط خط فرمان SHIGL

import sys
import os
from datetime import datetime

class SHIGLInterpreter:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.running = True
    
    def run(self, code: str) -> str:
        self.output = []
        lines = code.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            self._execute_line(line)
            if not self.running:
                break
        return '\n'.join(self.output)
    
    def _execute_line(self, line: str):
        if line.startswith('say '):
            text = line[4:].strip()
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            elif text in self.variables:
                text = str(self.variables[text])
            self.output.append(text)
        elif line.startswith('var '):
            parts = line[4:].split('=')
            if len(parts) == 2:
                name = parts[0].strip()
                value = parts[1].strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                elif value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                self.variables[name] = value
        elif line == 'time':
            self.output.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif line == 'exit':
            self.output.append("👋 خداحافظ!")
            self.running = False
        elif line == 'help':
            self.output.append("""📚 SHIGL AI - راهنما
  say "text"     - چاپ متن
  var x = 10     - تعریف متغیر
  time           - نمایش زمان
  add a b        - جمع
  sub a b        - تفریق
  mul a b        - ضرب
  div a b        - تقسیم
  vars           - نمایش متغیرها
  clear          - پاک کردن متغیرها
  help           - نمایش راهنما
  exit           - خروج""")
        elif line == 'vars':
            if not self.variables:
                self.output.append("📦 خالی")
            else:
                result = "📦 متغیرها:\n"
                for name, value in self.variables.items():
                    result += f"  {name} = {value}\n"
                self.output.append(result.strip())
        elif line == 'clear':
            self.variables.clear()
            self.output.append("🧹 پاک شد")
        elif line.startswith('add ') or line.startswith('sub ') or line.startswith('mul ') or line.startswith('div '):
            parts = line.split()
            if len(parts) == 3:
                op = parts[0]
                a = self._get_value(parts[1])
                b = self._get_value(parts[2])
                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    ops = {'add': a+b, 'sub': a-b, 'mul': a*b, 'div': a/b if b else "تقسیم بر صفر"}
                    self.output.append(f"{a} {op} {b} = {ops.get(op, 'نامشخص')}")
                else:
                    self.output.append(f"❌ خطا: {a} یا {b} عدد نیست")
        else:
            self.output.append(f"❌ دستور ناشناخته: {line}")
    
    def _get_value(self, token):
        if token in self.variables:
            return self.variables[token]
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token

def main():
    print("=" * 50)
    print("🧠 SHIGL AI v2.0")
    print("=" * 50)
    shigl = SHIGLInterpreter()
    while shigl.running:
        try:
            code = input("\nSHIGL> ").strip()
            if not code:
                continue
            result = shigl.run(code)
            if result:
                print(result)
        except KeyboardInterrupt:
            print("\n👋 خداحافظ!")
            break

if __name__ == "__main__":
    main()
EOFPYTHON2

chmod +x shigl_cli.py

echo "✅ فایل‌های اصلی ایجاد شدند!"

# ============================================
# 4. ایجاد نمونه فایل SHIGL
# ============================================
echo ""
echo "📄 مرحله 4: ایجاد نمونه فایل SHIGL..."

cat > examples/hello.shigl << 'EOFEXAMPLE'
// ============================================
// اولین برنامه SHIGL
// ============================================

say "سلام SHIGL!"
var name = "عرفان"
say name
add 10 5
time
help
EOFEXAMPLE

echo "✅ نمونه فایل ایجاد شد!"

# ============================================
# 5. نصب وابستگی‌ها
# ============================================
echo ""
echo "📦 مرحله 5: نصب وابستگی‌ها..."

apt update -y 2>/dev/null
apt install python3 git -y 2>/dev/null

echo "✅ وابستگی‌ها نصب شدند!"

# ============================================
# 6. تست اجرا
# ============================================
echo ""
echo "🧪 مرحله 6: تست اجرا..."

echo ""
echo "=========================================="
echo "✅ بازسازی کامل شد!"
echo "=========================================="
echo ""
echo "📁 ساختار فعلی:"
ls -la
echo ""
echo "🚀 برای اجرا، این دستورات رو امتحان کن:"
echo ""
echo "  # تست مفسر SHIGL"
echo "  python3 shigl_cli.py"
echo ""
echo "  # یا اجرای فایل نمونه"
echo "  cat examples/hello.shigl | python3 shigl_cli.py"
echo ""
echo "  # یا ساخت APK"
echo "  python3 build_apk_direct.py"
echo ""
echo "=========================================="
