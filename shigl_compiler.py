#!/usr/bin/env python3
# ============================================
# SHIGL Compiler v1.0
# تبدیل کد SHIGL به پروژه اندروید
# ============================================

import re
import os
import json
from datetime import datetime

class SHIGLCompiler:
    """کامپایلر SHIGL به اندروید"""
    
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.android_config = {
            'app_name': 'SHIGLApp',
            'package': 'com.example.shiglapp',
            'minSdk': 21,
            'targetSdk': 34,
            'activities': [],
            'permissions': []
        }
        self.java_code = ""
        self.xml_code = ""
        
    def compile(self, shigl_code: str) -> dict:
        """کامپایل کد SHIGL و تولید فایل‌های اندروید"""
        
        # تقسیم کد به خطوط
        lines = shigl_code.split('\n')
        
        # پردازش خط به خط
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # نادیده گرفتن خطوط خالی و کامنت‌ها
            if not line or line.startswith('//'):
                i += 1
                continue
            
            # تشخیص دستورات
            if line.startswith('var '):
                self._handle_var(line)
            elif line.startswith('func '):
                i = self._handle_func(lines, i)
            elif line.startswith('say '):
                self._handle_say(line)
            elif line.startswith('if '):
                i = self._handle_if(lines, i)
            elif line.startswith('for '):
                i = self._handle_for(lines, i)
            elif line.startswith('android '):
                i = self._handle_android(lines, i)
            elif line.startswith('permission '):
                self._handle_permission(line)
            else:
                print(f"⚠️  دستور ناشناخته: {line}")
            
            i += 1
        
        # تولید فایل‌های اندروید
        return self._generate_android_files()
    
    # ============================================
    # پردازش دستورات
    # ============================================
    
    def _handle_var(self, line: str):
        """پردازش دستور var"""
        # var name = value
        match = re.match(r'var\s+(\w+)\s*=\s*(.+)', line)
        if match:
            name = match.group(1)
            value = match.group(2).strip()
            
            # حذف گیومه‌ها
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
                self.variables[name] = f'"{value}"'
            elif value.isdigit():
                self.variables[name] = value
            elif value in ['true', 'false']:
                self.variables[name] = value
            else:
                self.variables[name] = value
            
            print(f"✅ متغیر: {name} = {value}")
    
    def _handle_say(self, line: str):
        """پردازش دستور say (تبدیل به Log.d)"""
        # say "Hello"
        match = re.match(r'say\s+(.+)', line)
        if match:
            text = match.group(1).strip()
            # تبدیل به کد جاوا
            self.java_code += f'        Log.d("SHIGL", {text});\n'
    
    def _handle_func(self, lines: list, index: int) -> int:
        """پردازش تابع"""
        line = lines[index].strip()
        match = re.match(r'func\s+(\w+)\((.*?)\)\s*{', line)
        if match:
            func_name = match.group(1)
            params = match.group(2).split(',') if match.group(2) else []
            
            # شروع تابع در جاوا
            self.java_code += f'\n    public void {func_name}({self._params_to_java(params)}) {{\n'
            
            # خواندن بدنه تابع
            index += 1
            while index < len(lines):
                body_line = lines[index].strip()
                if body_line == '}':
                    self.java_code += '    }\n'
                    break
                elif body_line.startswith('say '):
                    self._handle_say(body_line)
                elif body_line.startswith('if '):
                    index = self._handle_if(lines, index)
                index += 1
        
        return index
    
    def _handle_if(self, lines: list, index: int) -> int:
        """پردازش شرط if (تبدیل به جاوا)"""
        line = lines[index].strip()
        match = re.match(r'if\s+(.+?)\s*{', line)
        if match:
            condition = match.group(1).strip()
            self.java_code += f'        if ({self._convert_condition(condition)}) {{\n'
            
            # خواندن بدنه if
            index += 1
            while index < len(lines):
                body_line = lines[index].strip()
                if body_line == '}':
                    self.java_code += '        }\n'
                    break
                elif body_line.startswith('say '):
                    self._handle_say(body_line)
                elif body_line.startswith('var '):
                    self._handle_var(body_line)
                index += 1
        
        return index
    
    def _handle_for(self, lines: list, index: int) -> int:
        """پردازش حلقه for (تبدیل به جاوا)"""
        line = lines[index].strip()
        # for i in 1..5 {
        match = re.match(r'for\s+(\w+)\s+in\s+(\d+)\.\.(\d+)\s*{', line)
        if match:
            var_name = match.group(1)
            start = match.group(2)
            end = match.group(3)
            
            self.java_code += f'        for (int {var_name} = {start}; {var_name} <= {end}; {var_name}++) {{\n'
            
            # خواندن بدنه حلقه
            index += 1
            while index < len(lines):
                body_line = lines[index].strip()
                if body_line == '}':
                    self.java_code += '        }\n'
                    break
                elif body_line.startswith('say '):
                    self._handle_say(body_line)
                index += 1
        
        return index
    
    def _handle_android(self, lines: list, index: int) -> int:
        """پردازش بخش android"""
        line = lines[index].strip()
        match = re.match(r'android\s+app\s+"(.+?)"\s*{', line)
        if match:
            self.android_config['app_name'] = match.group(1)
            
            # خواندن تنظیمات اندروید
            index += 1
            while index < len(lines):
                body_line = lines[index].strip()
                if body_line == '}':
                    break
                elif body_line.startswith('package '):
                    self.android_config['package'] = body_line.split('"')[1]
                elif body_line.startswith('minSdk '):
                    self.android_config['minSdk'] = int(body_line.split(' ')[1])
                elif body_line.startswith('targetSdk '):
                    self.android_config['targetSdk'] = int(body_line.split(' ')[1])
                elif body_line.startswith('activity '):
                    index = self._handle_activity(lines, index)
                index += 1
        
        return index
    
    def _handle_activity(self, lines: list, index: int) -> int:
        """پردازش Activity"""
        line = lines[index].strip()
        match = re.match(r'activity\s+"(.+?)"\s*{', line)
        if match:
            activity_name = match.group(1)
            activity = {
                'name': activity_name,
                'layout': 'activity_main',
                'text': 'Hello from SHIGL!',
                'button': None
            }
            
            # خواندن محتوای Activity
            index += 1
            while index < len(lines):
                body_line = lines[index].strip()
                if body_line == '}':
                    break
                elif body_line.startswith('layout '):
                    activity['layout'] = body_line.split('"')[1]
                elif body_line.startswith('text '):
                    activity['text'] = body_line.split('"')[1]
                elif body_line.startswith('button '):
                    # button "Click Me" { onClick { ... } }
                    button_match = re.match(r'button\s+"(.+?)"\s*{', body_line)
                    if button_match:
                        activity['button'] = button_match.group(1)
                index += 1
            
            self.android_config['activities'].append(activity)
        
        return index
    
    def _handle_permission(self, line: str):
        """پردازش دستور permission"""
        match = re.match(r'permission\s+"(.+?)"', line)
        if match:
            self.android_config['permissions'].append(match.group(1))
    
    # ============================================
    # توابع کمکی
    # ============================================
    
    def _params_to_java(self, params: list) -> str:
        """تبدیل پارامترهای SHIGL به جاوا"""
        if not params:
            return ""
        java_params = []
        for p in params:
            p = p.strip()
            if p:
                java_params.append(f"String {p}")
        return ", ".join(java_params)
    
    def _convert_condition(self, condition: str) -> str:
        """تبدیل شرط SHIGL به جاوا"""
        # تبدیل == به .equals() برای رشته‌ها
        condition = condition.replace('==', '.equals(')
        return condition
    
    # ============================================
    # تولید فایل‌های اندروید
    # ============================================
    
    def _generate_android_files(self) -> dict:
        """تولید فایل‌های پروژه اندروید"""
        files = {}
        
        # ۱. MainActivity.java
        files['MainActivity.java'] = self._generate_main_activity()
        
        # ۲. activity_main.xml
        files['activity_main.xml'] = self._generate_layout()
        
        # ۳. AndroidManifest.xml
        files['AndroidManifest.xml'] = self._generate_manifest()
        
        # ۴. build.gradle
        files['build.gradle'] = self._generate_gradle()
        
        # ۵. strings.xml
        files['strings.xml'] = self._generate_strings()
        
        return files
    
    def _generate_main_activity(self) -> str:
        """تولید کد MainActivity.java"""
        package = self.android_config['package']
        app_name = self.android_config['app_name']
        
        # کد جاوا
        java_code = f"""package {package};

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.util.Log;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.textView);
        textView.setText("{self.android_config['activities'][0]['text'] if self.android_config['activities'] else 'Hello from SHIGL!'}");

"""
        
        # اضافه کردن کدهای تولید شده از SHIGL
        if self.java_code:
            java_code += self.java_code
        
        # اضافه کردن دکمه اگر وجود داشته باشد
        for activity in self.android_config['activities']:
            if activity.get('button'):
                java_code += f"""
        Button button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener() {{
            @Override
            public void onClick(View v) {{
                Log.d("SHIGL", "Button clicked!");
                TextView textView = findViewById(R.id.textView);
                textView.setText("Button Clicked!");
            }}
        }});
"""
        
        java_code += """
    }
}
"""
        return java_code
    
    def _generate_layout(self) -> str:
        """تولید فایل activity_main.xml"""
        return """<?xml version="1.0" encoding="utf-8"?>
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
        android:text="Hello from SHIGL!"
        android:textSize="24sp"
        android:textColor="#FF6200EE"
        android:layout_marginBottom="16dp" />

    <Button
        android:id="@+id/button"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me"
        android:backgroundTint="#FF6200EE" />

</LinearLayout>
"""
    
    def _generate_manifest(self) -> str:
        """تولید AndroidManifest.xml"""
        package = self.android_config['package']
        app_name = self.android_config['app_name']
        
        manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package}">

"""
        
        # اضافه کردن دسترسی‌ها
        for perm in self.android_config['permissions']:
            manifest += f'    <uses-permission android:name="android.permission.{perm}" />\n'
        
        manifest += f"""
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app_name}"
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
"""
        return manifest
    
    def _generate_gradle(self) -> str:
        """تولید build.gradle"""
        package = self.android_config['package']
        minSdk = self.android_config['minSdk']
        targetSdk = self.android_config['targetSdk']
        
        return f"""plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 34

    defaultConfig {{
        applicationId "{package}"
        minSdk {minSdk}
        targetSdk {targetSdk}
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
"""
    
    def _generate_strings(self) -> str:
        """تولید strings.xml"""
        app_name = self.android_config['app_name']
        return f"""<resources>
    <string name="app_name">{app_name}</string>
</resources>
"""


# ============================================
# رابط کاربری کامپایلر
# ============================================

def main():
    print("=" * 60)
    print("🚀 SHIGL Compiler v1.0")
    print("📱 تبدیل کد SHIGL به پروژه اندروید")
    print("=" * 60)
    
    compiler = SHIGLCompiler()
    
    # خواندن فایل SHIGL
    filename = input("\n📁 نام فایل SHIGL: ").strip()
    
    if not os.path.exists(filename):
        print(f"❌ فایل {filename} پیدا نشد!")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        shigl_code = f.read()
    
    print("\n🔨 در حال کامپایل...")
    files = compiler.compile(shigl_code)
    
    if not files:
        print("❌ خطا در کامپایل!")
        return
    
    # ایجاد پوشه خروجی
    output_dir = "android_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # ذخیره فایل‌ها
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} ساخته شد")
    
    print(f"""
✅ کامپایل با موفقیت انجام شد!

📁 خروجی در پوشه: {output_dir}/

🔧 مراحل بعدی:
   1. فایل‌های خروجی را به کامپیوتر منتقل کنید
   2. در Android Studio باز کنید
   3. Build -> Build APK

📱 کد SHIGL شما به یک اپلیکیشن اندروید تبدیل شد!
""")

if __name__ == "__main__":
    main()
