#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHIGL Android ChatGPT-Style UI Generator
تولید‌کننده اپلیکیشن اندروید با UI شبیه ChatGPT
"""

import os
import json
from datetime import datetime

class ChatGPTStyleGenerator:
    """تولید کننده UI اندروید شبیه ChatGPT"""
    
    def __init__(self, app_name="SHIGL AI Chat", package_name="com.shigl.aichat"):
        self.app_name = app_name
        self.package_name = package_name
        self.version_code = 1
        self.version_name = "1.0"
        self.min_sdk = 21
        self.target_sdk = 34
        
    def generate_project(self, output_dir="./android_chatgpt_app"):
        """تولید کامل پروژه اندروید"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create directory structure
        self._create_directory_structure(output_dir)
        
        # Generate all files
        files = {
            'AndroidManifest.xml': self.generate_manifest(),
            'MainActivity.java': self.generate_main_activity(),
            'ChatActivity.java': self.generate_chat_activity(),
            'MessageAdapter.java': self.generate_message_adapter(),
            'Message.java': self.generate_message_model(),
            'activity_main.xml': self.generate_main_layout(),
            'activity_chat.xml': self.generate_chat_layout(),
            'message_item.xml': self.generate_message_item_layout(),
            'colors.xml': self.generate_colors(),
            'strings.xml': self.generate_strings(),
            'build.gradle': self.generate_gradle(),
        }
        
        # Write files
        self._write_files(output_dir, files)
        print(f"✅ Project generated in: {output_dir}")
        return output_dir
    
    def _create_directory_structure(self, base_dir):
        """ایجاد ساختار دایرکتوری‌های پروژه"""
        java_package_path = os.path.join(
            base_dir, 'app', 'src', 'main', 'java',
            *self.package_name.split('.')
        )
        res_dirs = [
            os.path.join(base_dir, 'app', 'src', 'main', 'res', 'layout'),
            os.path.join(base_dir, 'app', 'src', 'main', 'res', 'values'),
            os.path.join(base_dir, 'app', 'src', 'main', 'res', 'drawable'),
            os.path.join(base_dir, 'app', 'src', 'main', 'res', 'mipmap'),
        ]
        
        os.makedirs(java_package_path, exist_ok=True)
        for d in res_dirs:
            os.makedirs(d, exist_ok=True)
    
    def generate_manifest(self):
        """تولید AndroidManifest.xml"""
        return f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{self.package_name}">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar"
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
            android:exported="false"
            android:label="@string/chat_title" />

    </application>

</manifest>
'''
    
    def generate_main_activity(self):
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
        
        // Initialize UI
        initializeUI();
    }}
    
    private void initializeUI() {{
        // Welcome TextView
        TextView welcomeText = findViewById(R.id.welcome_text);
        welcomeText.setText("Welcome to " + getString(R.string.app_name));
        
        // Start Chat Button
        Button startChatButton = findViewById(R.id.start_chat_button);
        startChatButton.setOnClickListener(v -> startChatActivity());
        
        // About Button
        Button aboutButton = findViewById(R.id.about_button);
        aboutButton.setOnClickListener(v -> showAbout());
    }}
    
    private void startChatActivity() {{
        Intent intent = new Intent(this, ChatActivity.class);
        startActivity(intent);
    }}
    
    private void showAbout() {{
        // Show about dialog
        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(this);
        builder.setTitle("About")
            .setMessage("SHIGL AI Chat v{self.version_name}\\n\\nA ChatGPT-style messaging app built with SHIGL")
            .setPositiveButton("OK", (dialog, which) -> dialog.dismiss())
            .show();
    }}
}}
'''
    
    def generate_chat_activity(self):
        """تولید ChatActivity.java"""
        package = self.package_name
        return f'''package {package};

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
        // Initialize RecyclerView
        messageRecyclerView = findViewById(R.id.message_recycler);
        messageRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        
        // Initialize message list
        messages = new ArrayList<>();
        messageAdapter = new MessageAdapter(messages);
        messageRecyclerView.setAdapter(messageAdapter);
        
        // Initialize input
        messageInput = findViewById(R.id.message_input);
        
        // Initialize send button
        sendButton = findViewById(R.id.send_button);
        sendButton.setOnClickListener(v -> sendMessage());
        
        // Add welcome message
        addWelcomeMessage();
    }}
    
    private void addWelcomeMessage() {{
        Message welcome = new Message(
            "👋 Hello! I'm SHIGL AI Chat. How can I help you today?",
            "ai",
            getCurrentTime()
        );
        messages.add(welcome);
        messageAdapter.notifyItemInserted(messages.size() - 1);
        messageRecyclerView.scrollToPosition(messages.size() - 1);
    }}
    
    private void sendMessage() {{
        String text = messageInput.getText().toString().trim();
        
        if (text.isEmpty()) {{
            Toast.makeText(this, "Please enter a message", Toast.LENGTH_SHORT).show();
            return;
        }}
        
        // Add user message
        Message userMessage = new Message(text, "user", getCurrentTime());
        messages.add(userMessage);
        messageAdapter.notifyItemInserted(messages.size() - 1);
        messageRecyclerView.scrollToPosition(messages.size() - 1);
        
        // Clear input
        messageInput.setText("");
        
        // Simulate AI response
        sendButton.setEnabled(false);
        messageInput.setEnabled(false);
        
        // Simulate delay and response
        messageInput.postDelayed(() -> {{
            addAIResponse(text);
            sendButton.setEnabled(true);
            messageInput.setEnabled(true);
        }}, 1500);
    }}
    
    private void addAIResponse(String userMessage) {{
        String response = generateResponse(userMessage);
        Message aiMessage = new Message(response, "ai", getCurrentTime());
        messages.add(aiMessage);
        messageAdapter.notifyItemInserted(messages.size() - 1);
        messageRecyclerView.scrollToPosition(messages.size() - 1);
    }}
    
    private String generateResponse(String userMessage) {{
        // Simple response generation
        userMessage = userMessage.toLowerCase();
        
        if (userMessage.contains("hello") || userMessage.contains("hi")) {{
            return "👋 Hello! How can I assist you?";
        }} else if (userMessage.contains("who are you")) {{
            return "🤖 I'm SHIGL AI, a chatbot powered by the SHIGL programming language!";
        }} else if (userMessage.contains("help")) {{
            return "ℹ️ I can help you with questions! Try asking me anything.";
        }} else if (userMessage.contains("how are you")) {{
            return "😊 I'm doing great! Thanks for asking. How about you?";
        }} else {{
            return "✨ That's interesting! Tell me more about that.\\n\\n(This is a demo response - in production, this would connect to a real AI service)";
        }}
    }}
    
    private String getCurrentTime() {{
        SimpleDateFormat sdf = new SimpleDateFormat("HH:mm", Locale.getDefault());
        return sdf.format(new Date());
    }}
}}
'''
    
    def generate_message_adapter(self):
        """تولید MessageAdapter.java"""
        package = self.package_name
        return f'''package {package};

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
        Message message = messages.get(position);
        return message.getSender().equals("user") ? VIEW_TYPE_USER : VIEW_TYPE_AI;
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
        
        private TextView messageText;
        private TextView messageTime;
        private FrameLayout userContainer;
        private FrameLayout aiContainer;
        
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
            
            if (viewType == VIEW_TYPE_USER) {{
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
    
    def generate_message_model(self):
        """تولید Message.java model"""
        package = self.package_name
        return f'''package {package};

public class Message {{
    
    private String text;
    private String sender; // "user" or "ai"
    private String time;
    
    public Message(String text, String sender, String time) {{
        this.text = text;
        this.sender = sender;
        this.time = time;
    }}
    
    public String getText() {{
        return text;
    }}
    
    public void setText(String text) {{
        this.text = text;
    }}
    
    public String getSender() {{
        return sender;
    }}
    
    public void setSender(String sender) {{
        this.sender = sender;
    }}
    
    public String getTime() {{
        return time;
    }}
    
    public void setTime(String time) {{
        this.time = time;
    }}
}}
'''
    
    def generate_main_layout(self):
        """تولید activity_main.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:gravity="center"
    android:padding="24dp"
    android:background="@color/background"
    tools:context=".MainActivity">

    <!-- Logo / App Name -->
    <ImageView
        android:id="@+id/app_logo"
        android:layout_width="100dp"
        android:layout_height="100dp"
        android:src="@drawable/ic_chat"
        android:contentDescription="@string/app_name"
        android:layout_marginBottom="24dp"
        android:tint="@color/primary" />

    <!-- Welcome Text -->
    <TextView
        android:id="@+id/welcome_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome_message"
        android:textSize="28sp"
        android:textStyle="bold"
        android:textColor="@color/on_background"
        android:gravity="center"
        android:layout_marginBottom="16dp" />

    <!-- Subtitle -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome_subtitle"
        android:textSize="16sp"
        android:textColor="@android:color/darker_gray"
        android:gravity="center"
        android:layout_marginBottom="48dp" />

    <!-- Start Chat Button -->
    <Button
        android:id="@+id/start_chat_button"
        android:layout_width="match_parent"
        android:layout_height="60dp"
        android:text="@string/start_chat"
        android:textSize="18sp"
        android:textStyle="bold"
        android:background="@drawable/button_primary"
        android:textColor="@color/on_primary"
        android:layout_marginBottom="16dp" />

    <!-- About Button -->
    <Button
        android:id="@+id/about_button"
        android:layout_width="match_parent"
        android:layout_height="60dp"
        android:text="@string/about"
        android:textSize="18sp"
        android:background="@drawable/button_secondary"
        android:textColor="@color/primary"
        android:layout_marginBottom="16dp" />

    <!-- Spacer -->
    <View
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

    <!-- Footer -->
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/footer"
        android:textSize="12sp"
        android:textColor="@android:color/darker_gray"
        android:gravity="center" />

</LinearLayout>
'''
    
    def generate_chat_layout(self):
        """تولید activity_chat.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="@color/background">

    <!-- Messages RecyclerView -->
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/message_recycler"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        android:padding="8dp"
        android:background="@color/surface" />

    <!-- Divider -->
    <View
        android:layout_width="match_parent"
        android:layout_height="1dp"
        android:background="@android:color/darker_gray" />

    <!-- Message Input Section -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="12dp"
        android:background="@color/surface">

        <!-- EditText -->
        <EditText
            android:id="@+id/message_input"
            android:layout_width="0dp"
            android:layout_height="48dp"
            android:layout_weight="1"
            android:hint="@string/chat_hint"
            android:paddingStart="16dp"
            android:paddingEnd="16dp"
            android:textSize="14sp"
            android:textColorHint="@android:color/darker_gray"
            android:background="@drawable/input_field_background"
            android:layout_marginEnd="8dp"
            android:inputType="text|textAutoCorrect"
            android:maxLines="1" />

        <!-- Send Button -->
        <Button
            android:id="@+id/send_button"
            android:layout_width="48dp"
            android:layout_height="48dp"
            android:text="→"
            android:textSize="24sp"
            android:textStyle="bold"
            android:background="@drawable/button_send"
            android:textColor="@color/on_primary"
            android:contentDescription="@string/send" />

    </LinearLayout>

</LinearLayout>
'''
    
    def generate_message_item_layout(self):
        """تولید message_item.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:padding="8dp">

    <!-- User Message Container (Right Aligned) -->
    <LinearLayout
        android:id="@+id/user_message_container"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="end"
        android:orientation="vertical"
        android:paddingEnd="8dp"
        android:paddingStart="64dp">

        <androidx.cardview.widget.CardView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginEnd="8dp"
            app:cardBackgroundColor="@color/primary"
            app:cardCornerRadius="16dp"
            app:cardElevation="0dp">

            <LinearLayout
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:orientation="vertical">

                <TextView
                    android:id="@+id/message_text"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:maxWidth="280dp"
                    android:text="User Message"
                    android:textSize="14sp"
                    android:textColor="@color/on_primary"
                    android:padding="12dp" />

            </LinearLayout>

        </androidx.cardview.widget.CardView>

        <TextView
            android:id="@+id/message_time"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="12:34"
            android:textSize="12sp"
            android:textColor="@android:color/darker_gray"
            android:layout_marginTop="4dp"
            android:layout_gravity="end"
            android:paddingEnd="8dp" />

    </LinearLayout>

    <!-- AI Message Container (Left Aligned) -->
    <LinearLayout
        android:id="@+id/ai_message_container"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="start"
        android:orientation="vertical"
        android:paddingStart="8dp"
        android:paddingEnd="64dp"
        android:visibility="gone">

        <androidx.cardview.widget.CardView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_marginStart="8dp"
            app:cardBackgroundColor="@android:color/lighter_gray"
            app:cardCornerRadius="16dp"
            app:cardElevation="0dp">

            <LinearLayout
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:orientation="vertical">

                <TextView
                    android:id="@+id/message_text"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:maxWidth="280dp"
                    android:text="AI Message"
                    android:textSize="14sp"
                    android:textColor="@android:color/black"
                    android:padding="12dp" />

            </LinearLayout>

        </androidx.cardview.widget.CardView>

        <TextView
            android:id="@+id/message_time"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="12:34"
            android:textSize="12sp"
            android:textColor="@android:color/darker_gray"
            android:layout_marginTop="4dp"
            android:layout_gravity="start"
            android:paddingStart="8dp" />

    </LinearLayout>

</FrameLayout>
'''
    
    def generate_colors(self):
        """تولید colors.xml"""
        return '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#FF6200EE</color>
    <color name="primary_dark">#FF3700B3</color>
    <color name="secondary">#FF03DAC6</color>
    <color name="secondary_dark">#FF018786</color>
    <color name="error">#FFCF6679</color>
    <color name="background">#FFFAFAFA</color>
    <color name="surface">#FFFFFFFF</color>
    <color name="on_primary">#FFFFFFFF</color>
    <color name="on_background">#FF1F1F1F</color>
    <color name="on_surface">#FF1F1F1F</color>
</resources>
'''
    
    def generate_strings(self):
        """تولید strings.xml"""
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{self.app_name}</string>
    <string name="welcome_message">Welcome to SHIGL</string>
    <string name="welcome_subtitle">AI Chat powered by SHIGL Programming Language</string>
    <string name="start_chat">Start Chat</string>
    <string name="about">About</string>
    <string name="chat_title">SHIGL AI Chat</string>
    <string name="chat_hint">Type your message...</string>
    <string name="send">Send</string>
    <string name="footer">© 2024 SHIGL. Made with ❤️</string>
</resources>
'''
    
    def generate_gradle(self):
        """تولید build.gradle"""
        return f'''plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 34

    defaultConfig {{
        applicationId "{self.package_name}"
        minSdk {self.min_sdk}
        targetSdk {self.target_sdk}
        versionCode {self.version_code}
        versionName "{self.version_name}"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }}
}}

dependencies {{
    // Android Support
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.1'
    implementation 'androidx.cardview:cardview:1.0.0'
    
    // Material Design
    implementation 'com.google.android.material:material:1.9.0'
    
    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}}
'''
    
    def _write_files(self, base_dir, files):
        """نوشتن فایل‌های تولید شده"""
        for filename, content in files.items():
            if filename.endswith('.java'):
                path = os.path.join(base_dir, 'app', 'src', 'main', 'java',
                                   *self.package_name.split('.'),
                                   filename)
            elif filename.endswith('.xml') and 'Activity' not in filename and 'Manifest' not in filename:
                # Resource files
                if filename.startswith('activity_') or filename.startswith('message_'):
                    path = os.path.join(base_dir, 'app', 'src', 'main', 'res', 'layout', filename)
                else:
                    path = os.path.join(base_dir, 'app', 'src', 'main', 'res', 'values', filename)
            else:
                # AndroidManifest.xml and build.gradle
                path = os.path.join(base_dir, 'app', 'src', 'main', filename) if filename == 'AndroidManifest.xml' \
                    else os.path.join(base_dir, 'app', filename)
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {filename}")


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 SHIGL ChatGPT-Style Android App Generator")
    print("=" * 50)
    print()
    
    generator = ChatGPTStyleGenerator(
        app_name="SHIGL AI Chat",
        package_name="com.shigl.aichat"
    )
    
    output_dir = generator.generate_project()
    
    print()
    print("=" * 50)
    print("✅ Project Generated Successfully!")
    print("=" * 50)
    print()
    print(f"📁 Location: {output_dir}")
    print()
    print("📝 Next steps:")
    print("1. Open Android Studio")
    print("2. Select 'File' > 'Open'")
    print(f"3. Navigate to: {output_dir}")
    print("4. Wait for Gradle sync to complete")
    print("5. Click 'Run' to build and test on an emulator or device")
    print()
    print("🎉 Enjoy your SHIGL AI Chat App!")
    print()
