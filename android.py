# shigl/android.py
from .ast import *

class AndroidCodeGenerator:
    def generate(self, ast: AndroidApp) -> dict:
        files = {}
        
        files['MainActivity.java'] = self.generate_activity(ast)
        files['activity_main.xml'] = self.generate_layout(ast)
        files['AndroidManifest.xml'] = self.generate_manifest(ast)
        files['build.gradle'] = self.generate_gradle(ast)
        files['strings.xml'] = self.generate_strings(ast)
        
        return files
    
    def generate_activity(self, app: AndroidApp) -> str:
        activity = app.activities[0] if app.activities else None
        activity_name = activity.name if activity else "MainActivity"
        layout = activity.layout if activity else "activity_main"
        label = activity.label if activity else "SHIGL App"
        
        return f"""package {app.package};

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class {activity_name} extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.{layout});
        
        TextView textView = findViewById(R.id.textView);
        textView.setText("{label}");
    }}
}}"""
    
    def generate_layout(self, app: AndroidApp) -> str:
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
        android:text="Hello SHIGL!"
        android:textSize="24sp"
        android:textColor="#FF6200EE" />
</LinearLayout>"""
    
    def generate_manifest(self, app: AndroidApp) -> str:
        perms = ''.join([f'    <uses-permission android:name="android.permission.{p}" />\n' for p in app.permissions])
        activity = app.activities[0] if app.activities else None
        activity_name = activity.name if activity else "MainActivity"
        
        return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{app.package}">
{perms}
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{app.name}"
        android:theme="@style/Theme.AppCompat.Light">
        <activity
            android:name=".{activity_name}"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>"""
    
    def generate_gradle(self, app: AndroidApp) -> str:
        return f"""plugins {{
    id 'com.android.application'
}}

android {{
    compileSdk 34

    defaultConfig {{
        applicationId "{app.package}"
        minSdk {app.minSdk}
        targetSdk {app.targetSdk}
        versionCode 1
        versionName "1.0"
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.6.1'
}}"""
    
    def generate_strings(self, app: AndroidApp) -> str:
        return f"""<resources>
    <string name="app_name">{app.name}</string>
</resources>"""