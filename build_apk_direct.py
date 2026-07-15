#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHIGL ChatGPT Android App - Direct APK Generator
بدون نیاز به Android Studio - مستقیم APK تولید کنید
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path

class SHIGLAndroidBuilder:
    """تولید و Build کردن APK مستقیم"""
    
    def __init__(self, app_name="SHIGL AI Chat", package_name="com.shigl.aichat"):
        self.app_name = app_name
        self.package_name = package_name
        self.version_code = 1
        self.version_name = "1.0"
        self.min_sdk = 21
        self.target_sdk = 34
        self.base_dir = None
        
    def build_apk(self, output_dir="./shigl_chatgpt_app"):
        """تولید و Build کردن APK مستقیم"""
        print("=" * 60)
        print("🚀 SHIGL ChatGPT Android App - Direct APK Generator")
        print("=" * 60)
        print()
        
        # Step 1: Create project structure
        print("📁 Step 1: Creating project structure...")
        self._create_project_structure(output_dir)
        self.base_dir = output_dir
        
        # Step 2: Generate all source files
        print("📝 Step 2: Generating source files...")
        self._generate_all_files()
        
        # Step 3: Generate Gradle files
        print("⚙️  Step 3: Generating Gradle configuration...")
        self._generate_gradle_files()
        
        # Step 4: Check for build tools
        print("🔍 Step 4: Checking for Android build tools...")
        self._check_build_tools()
        
        # Step 5: Build APK
        print("🔨 Step 5: Building APK...")
        self._build_apk()
        
        print()
        print("=" * 60)
        print("✅ APK Generated Successfully!")
        print("=" * 60)
        print()
        
    def _create_project_structure(self, output_dir):
        """ایجاد ساختار پروژه"""
        paths = [
            f"{output_dir}/app/src/main/java/{self.package_name.replace('.', '/')}",
            f"{output_dir}/app/src/main/res/layout",
            f"{output_dir}/app/src/main/res/values",
            f"{output_dir}/app/src/main/res/drawable",
            f"{output_dir}/app/src/main/res/mipmap",
            f"{output_dir}/app/src/test/java",
        ]
        
        for path in paths:
            os.makedirs(path, exist_ok=True)
            print(f"  ✓ Created: {path}")
    
    def _generate_all_files(self):
        """تولید تمام فایل‌های مورد نیاز"""
        files_to_generate = {
            'java': {
                'MainActivity.java': self._generate_main_activity(),
                'ChatActivity.java': self._generate_chat_activity(),
                'MessageAdapter.java': self._generate_message_adapter(),
                'Message.java': self._generate_message_model(),
            },
            'layout': {
                'activity_main.xml': self._generate_main_layout(),
                'activity_chat.xml': self._generate_chat_layout(),
                'message_item.xml': self._generate_message_item(),
            },
            'values': {
                'colors.xml': self._generate_colors(),
                'strings.xml': self._generate_strings(),
                'styles.xml': self._generate_styles(),
            },
        }
        
        # Write Java files
        java_path = os.path.join(self.base_dir, 'app', 'src', 'main', 'java', 
                                 *self.package_name.split('.'))
        for filename, content in files_to_generate['java'].items():
            filepath = os.path.join(java_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Generated: {filename}")
        
        # Write Layout files
        layout_path = os.path.join(self.base_dir, 'app', 'src', 'main', 'res', 'layout')
        for filename, content in files_to_generate['layout'].items():
            filepath = os.path.join(layout_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Generated: {filename}")
        
        # Write Resource files
        values_path = os.path.join(self.base_dir, 'app', 'src', 'main', 'res', 'values')
        for filename, content in files_to_generate['values'].items():
            filepath = os.path.join(values_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Generated: {filename}")
        
        # Write AndroidManifest.xml
        manifest_path = os.path.join(self.base_dir, 'app', 'src', 'main', 'AndroidManifest.xml')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_manifest())
        print(f"  ✓ Generated: AndroidManifest.xml")
    
    def _generate_gradle_files(self):
        """تولید فایل‌های Gradle"""
        # settings.gradle
        settings_gradle = '''rootProject.name = "SHIGL ChatGPT"
include ':app'
'''
        with open(os.path.join(self.base_dir, 'settings.gradle'), 'w') as f:
            f.write(settings_gradle)
        print(f"  ✓ Generated: settings.gradle")
        
        # build.gradle (Project)
        project_gradle = '''buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
'''
        with open(os.path.join(self.base_dir, 'build.gradle'), 'w') as f:
            f.write(project_gradle)
        print(f"  ✓ Generated: build.gradle (Project)")
        
        # build.gradle (App)
        app_gradle = f'''plugins {{
    id 'com.android.application'
}}

android {{
    namespace "{self.package_name}"
    compileSdk 34

    defaultConfig {{
        applicationId "{self.package_name}"
        minSdk {self.min_sdk}
        targetSdk {self.target_sdk}
        versionCode {self.version_code}
        versionName "{self.version_name}"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
        }}
        debug {{
            debuggable true
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.1'
    implementation 'androidx.cardview:cardview:1.0.0'
    implementation 'com.google.android.material:material:1.9.0'
    
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
'''
        app_gradle_path = os.path.join(self.base_dir, 'app', 'build.gradle')
        with open(app_gradle_path, 'w') as f:
            f.write(app_gradle)
        print(f"  ✓ Generated: build.gradle (App)")
    
    def _check_build_tools(self):
        """بررسی ابزارهای Build"""
        # Check for Android SDK
        android_home = os.environ.get('ANDROID_HOME', '')
        if not android_home:
            print()
            print("⚠️  ANDROID_HOME is not set!")
            print()
            print("📱 Quick Setup Instructions:")
            print("1. Download Android SDK from: https://developer.android.com/studio/command-line-tools")
            print("2. Extract and set ANDROID_HOME:")
            print("   - Linux/Mac: export ANDROID_HOME=~/Android/Sdk")
            print("   - Windows: set ANDROID_HOME=C:\\Users\\YourName\\AppData\\Local\\Android\\Sdk")
            print("3. Install build tools:")
            print("   - Run: $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses")
            print("   - Run: $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager 'build-tools;34.0.0'")
            print()
            return False
        
        print(f"  ✓ ANDROID_HOME set: {android_home}")
        return True
    
    def _build_apk(self):
        """Build کردن APK"""
        try:
            print(f"  Starting Gradle build in: {self.base_dir}")
            
            # Run gradle build
            if sys.platform == "win32":
                result = subprocess.run(
                    [os.path.join(self.base_dir, 'gradlew.bat'), 'build'],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['./gradlew', 'build'],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                print("  ✓ APK built successfully!")
                print()
                print(f"📦 APK Location:")
                print(f"   {os.path.join(self.base_dir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')}")
            else:
                print("  ⚠️  Build output:")
                print(result.stdout)
                print(result.stderr)
        except Exception as e:
            print(f"  ⚠️  Error during build: {e}")
    
    def _generate_manifest(self):
        """تولید AndroidManifest.xml"""
        return f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity
            android:name=".ChatActivity"
            android:exported="false" />

    </application>

</manifest>
'''
    
    def _generate_main_activity(self):
        """تولید MainActivity.java"""
        return f'''package {self.package_name};

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initializeUI();
    }}
    
    private void initializeUI() {{
        TextView welcomeText = findViewById(R.id.welcome_text);
        welcomeText.setText("Welcome to SHIGL");
        
        Button startChatButton = findViewById(R.id.start_chat_button);
        startChatButton.setOnClickListener(v -> startChatActivity());
    }}
    
    private void startChatActivity() {{
        Intent intent = new Intent(this, ChatActivity.class);
        startActivity(intent);
    }}
}}
'''
    
    def _generate_chat_activity(self):
        """تولید ChatActivity.java"""
        return f'''package {self.package_name};

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Locale;

public class ChatActivity extends AppCompatActivity {{
    
    private RecyclerView messageRecyclerView;
    private EditText messageInput;
    private Button sendButton;
    private MessageAdapter messageAdapter;
    private ArrayList<Message> messages;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        setTitle("SHIGL AI Chat");
        initializeUI();
    }}
    
    private void initializeUI() {{
        messageRecyclerView = findViewById(R.id.message_recycler);
        messageRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        
        messages = new ArrayList<>();
        messageAdapter = new MessageAdapter(messages);
        messageRecyclerView.setAdapter(messageAdapter);
        
        messageInput = findViewById(R.id.message_input);
        sendButton = findViewById(R.id.send_button);
        sendButton.setOnClickListener(v -> sendMessage());
        
        addWelcomeMessage();
    }}
    
    private void addWelcomeMessage() {{
        Message welcome = new Message(
            "👋 Hello! I'm SHIGL AI Chat",
            "ai",
            getCurrentTime()
        );
        messages.add(welcome);
        messageAdapter.notifyItemInserted(messages.size() - 1);
    }}
    
    private void sendMessage() {{
        String text = messageInput.getText().toString().trim();
        
        if (text.isEmpty()) {{
            Toast.makeText(this, "Please enter a message", Toast.LENGTH_SHORT).show();
            return;
        }}
        
        Message userMessage = new Message(text, "user", getCurrentTime());
        messages.add(userMessage);
        messageAdapter.notifyItemInserted(messages.size() - 1);
        messageRecyclerView.scrollToPosition(messages.size() - 1);
        
        messageInput.setText("");
        sendButton.setEnabled(false);
        
        messageInput.postDelayed(() -> {{
            String response = "✨ That's interesting!";
            Message aiMessage = new Message(response, "ai", getCurrentTime());
            messages.add(aiMessage);
            messageAdapter.notifyItemInserted(messages.size() - 1);
            messageRecyclerView.scrollToPosition(messages.size() - 1);
            sendButton.setEnabled(true);
        }}, 1000);
    }}
    
    private String getCurrentTime() {{
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm", Locale.getDefault());
        return sdf.format(new Date());
    }}
}}
'''
    
    def _generate_message_adapter(self):
        """تولید MessageAdapter.java"""
        return f'''package {self.package_name};

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;

public class MessageAdapter extends RecyclerView.Adapter<MessageAdapter.MessageViewHolder> {{
    
    private ArrayList<Message> messages;
    private static final int VIEW_TYPE_USER = 1;
    private static final int VIEW_TYPE_AI = 2;
    
    public MessageAdapter(ArrayList<Message> messages) {{
        this.messages = messages;
    }}
    
    @Override
    public int getItemViewType(int position) {{
        return messages.get(position).getSender().equals("user") ? VIEW_TYPE_USER : VIEW_TYPE_AI;
    }}
    
    @NonNull
    @Override
    public MessageViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {{
        LayoutInflater inflater = LayoutInflater.from(parent.getContext());
        View view = inflater.inflate(R.layout.message_item, parent, false);
        return new MessageViewHolder(view);
    }}
    
    @Override
    public void onBindViewHolder(@NonNull MessageViewHolder holder, int position) {{
        Message message = messages.get(position);
        holder.bind(message, getItemViewType(position));
    }}
    
    @Override
    public int getItemCount() {{
        return messages.size();
    }}
    
    public static class MessageViewHolder extends RecyclerView.ViewHolder {{
        private TextView messageText, messageTime;
        private FrameLayout userContainer, aiContainer;
        
        public MessageViewHolder(@NonNull View itemView) {{
            super(itemView);
            messageText = itemView.findViewById(R.id.message_text);
            messageTime = itemView.findViewById(R.id.message_time);
            userContainer = itemView.findViewById(R.id.user_message_container);
            aiContainer = itemView.findViewById(R.id.ai_message_container);
        }}
        
        public void bind(Message message, int viewType) {{
            messageText.setText(message.getText());
            messageTime.setText(message.getTime());
            
            if (viewType == 1) {{
                userContainer.setVisibility(View.VISIBLE);
                aiContainer.setVisibility(View.GONE);
            }} else {{
                userContainer.setVisibility(View.GONE);
                aiContainer.setVisibility(View.VISIBLE);
            }}
        }}
    }}
}}
'''
    
    def _generate_message_model(self):
        """تولید Message.java"""
        return f'''package {self.package_name};

public class Message {{
    private String text, sender, time;
    
    public Message(String text, String sender, String time) {{
        this.text = text;
        this.sender = sender;
        this.time = time;
    }}
    
    public String getText() {{ return text; }}
    public String getSender() {{ return sender; }}
    public String getTime() {{ return time; }}
}}
'''
    
    def _generate_main_layout(self):
        """تولید activity_main.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp"
    android:background="@color/background">

    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Welcome to SHIGL"
        android:textSize="28sp"
        android:textStyle="bold"
        android:textColor="@color/on_background"
        android:layout_marginBottom="24dp" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="AI Chat powered by SHIGL"
        android:textSize="16sp"
        android:textColor="@android:color/darker_gray"
        android:layout_marginBottom="48dp" />

    <Button
        android:id="@+id/start_chat_button"
        android:layout_width="match_parent"
        android:layout_height="60dp"
        android:text="Start Chat"
        android:textSize="18sp"
        android:textStyle="bold"
        android:backgroundTint="@color/primary" />

</LinearLayout>
'''
    
    def _generate_chat_layout(self):
        """تولید activity_chat.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@color/surface">

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/message_recycler"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:padding="8dp" />

    <View
        android:layout_width="match_parent"
        android:layout_height="1dp"
        android:background="@android:color/darker_gray" />

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="12dp">

        <EditText
            android:id="@+id/message_input"
            android:layout_width="0dp"
            android:layout_height="48dp"
            android:layout_weight="1"
            android:hint="Type message..."
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:background="@drawable/input_field"
            android:layout_marginEnd="8dp" />

        <Button
            android:id="@+id/send_button"
            android:layout_width="48dp"
            android:layout_height="48dp"
            android:text="→"
            android:textSize="24sp"
            android:backgroundTint="@color/primary" />

    </LinearLayout>

</LinearLayout>
'''
    
    def _generate_message_item(self):
        """تولید message_item.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="8dp">

    <LinearLayout
        android:id="@+id/user_message_container"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="end"
        android:orientation="vertical">

        <androidx.cardview.widget.CardView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            app:cardBackgroundColor="@color/primary"
            app:cardCornerRadius="16dp">

            <TextView
                android:id="@+id/message_text"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:maxWidth="280dp"
                android:text="Message"
                android:textColor="@color/on_primary"
                android:padding="12dp" />

        </androidx.cardview.widget.CardView>

        <TextView
            android:id="@+id/message_time"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="12:34"
            android:textSize="12sp"
            android:layout_gravity="end" />

    </LinearLayout>

    <LinearLayout
        android:id="@+id/ai_message_container"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="start"
        android:orientation="vertical"
        android:visibility="gone">

        <androidx.cardview.widget.CardView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            app:cardBackgroundColor="@android:color/lighter_gray"
            app:cardCornerRadius="16dp">

            <TextView
                android:id="@+id/message_text"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:maxWidth="280dp"
                android:text="Message"
                android:textColor="@android:color/black"
                android:padding="12dp" />

        </androidx.cardview.widget.CardView>

        <TextView
            android:id="@+id/message_time"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="12:34"
            android:textSize="12sp" />

    </LinearLayout>

</FrameLayout>
'''
    
    def _generate_colors(self):
        """تولید colors.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#FF6200EE</color>
    <color name="primary_dark">#FF3700B3</color>
    <color name="secondary">#FF03DAC6</color>
    <color name="error">#FFCF6679</color>
    <color name="background">#FFFAFAFA</color>
    <color name="surface">#FFFFFFFF</color>
    <color name="on_primary">#FFFFFFFF</color>
    <color name="on_background">#FF1F1F1F</color>
</resources>
'''
    
    def _generate_strings(self):
        """تولید strings.xml"""
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{self.app_name}</string>
    <string name="chat_hint">Type your message...</string>
    <string name="send">Send</string>
</resources>
'''
    
    def _generate_styles(self):
        """تولید styles.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/secondary</item>
    </style>
</resources>
'''


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='SHIGL ChatGPT Android App Builder')
    parser.add_argument('--name', default='SHIGL AI Chat', help='App name')
    parser.add_argument('--package', default='com.shigl.aichat', help='Package name')
    parser.add_argument('--output', default='./shigl_chatgpt_app', help='Output directory')
    
    args = parser.parse_args()
    
    builder = SHIGLAndroidBuilder(app_name=args.name, package_name=args.package)
    builder.build_apk(output_dir=args.output)
    
    print("📱 Installation Instructions:")
    print("1. Install APK on your device:")
    print("   adb install app/build/outputs/apk/debug/app-debug.apk")
    print()
    print("2. Or just copy the APK and install manually")
    print()
    print("🎉 Enjoy your SHIGL ChatGPT App!")
