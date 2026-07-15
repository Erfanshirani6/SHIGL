#!/bin/bash
# ============================================
# SHIGL ChatGPT App - Termux Installation Script
# اسکریپت نصب اتوماتیک برای Termux
# ============================================

set -e

echo "============================================"
echo "🚀 SHIGL ChatGPT - Termux Installer"
echo "============================================"
echo ""

# رنگ‌ها
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Update و Upgrade
echo -e "${BLUE}📦 Step 1: Updating packages...${NC}"
apt update && apt upgrade -y
echo -e "${GREEN}✓ Packages updated${NC}"
echo ""

# Step 2: نصب پکیج‌های مورد نیاز
echo -e "${BLUE}📦 Step 2: Installing required packages...${NC}"
apt install python3 git openjdk-17 wget unzip -y
echo -e "${GREEN}✓ All packages installed${NC}"
echo ""

# Step 3: نصب Android SDK
echo -e "${BLUE}📱 Step 3: Installing Android SDK...${NC}"
mkdir -p ~/Android/Sdk
cd ~/Android/Sdk

# دانلود SDK
echo "Downloading Android SDK Command Line Tools..."
wget -q https://dl.google.com/android/repository/commandlinetools-linux-10406996_latest.zip
echo -e "${GREEN}✓ Downloaded${NC}"

# استخراج
echo "Extracting..."
unzip -q commandlinetools-linux-10406996_latest.zip
rm commandlinetools-linux-10406996_latest.zip
echo -e "${GREEN}✓ Extracted${NC}"
echo ""

# Step 4: تنظیم متغیرهای محیطی
echo -e "${BLUE}⚙️  Step 4: Setting environment variables...${NC}"
echo "export ANDROID_HOME=$HOME/Android/Sdk" >> ~/.bashrc
echo "export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin:\$ANDROID_HOME/platform-tools" >> ~/.bashrc
source ~/.bashrc
echo -e "${GREEN}✓ Environment variables set${NC}"
echo ""

# Step 5: قبول مجوزها
echo -e "${BLUE}📋 Step 5: Accepting Android licenses...${NC}"
yes | sdkmanager --licenses > /dev/null 2>&1
echo -e "${GREEN}✓ Licenses accepted${NC}"
echo ""

# Step 6: نصب Platform و Build Tools
echo -e "${BLUE}🔧 Step 6: Installing Android Platform & Build Tools...${NC}"
sdkmanager "platforms;android-34" "build-tools;34.0.0" 2>&1 | grep -E "Installing|Installed|%"
echo -e "${GREEN}✓ Platform and Build Tools installed${NC}"
echo ""

# Step 7: دانلود SHIGL
echo -e "${BLUE}📥 Step 7: Downloading SHIGL project...${NC}"
cd ~
if [ -d "SHIGL" ]; then
    echo "SHIGL already exists, updating..."
    cd SHIGL
    git pull
else
    git clone https://github.com/Erfanshirani6/SHIGL.git
    cd SHIGL
fi
echo -e "${GREEN}✓ SHIGL downloaded${NC}"
echo ""

# Step 8: ساخت APK
echo -e "${BLUE}🔨 Step 8: Building APK...${NC}"
echo "This may take 3-5 minutes..."
echo ""
python3 build_apk_direct.py
echo ""

# Step 9: مکان فایل APK
APK_PATH="$HOME/SHIGL/shigl_chatgpt_app/app/build/outputs/apk/debug/app-debug.apk"
DOWNLOADS_PATH="$HOME/storage/downloads/"

if [ -f "$APK_PATH" ]; then
    echo -e "${GREEN}✅ APK created successfully!${NC}"
    echo ""
    echo "📁 APK Location: $APK_PATH"
    echo ""
    
    # کپی به دانلودها
    mkdir -p "$DOWNLOADS_PATH"
    cp "$APK_PATH" "$DOWNLOADS_PATH/shigl_chatgpt.apk"
    echo -e "${GREEN}✓ Copied to: $DOWNLOADS_PATH/shigl_chatgpt.apk${NC}"
    echo ""
    
    echo "============================================"
    echo "✨ Installation Complete!"
    echo "============================================"
    echo ""
    echo "📱 Next steps:"
    echo "1. Open File Manager"
    echo "2. Go to Downloads folder"
    echo "3. Find: shigl_chatgpt.apk"
    echo "4. Tap to install"
    echo "5. Launch SHIGL AI Chat app"
    echo ""
    echo "🎉 Enjoy your SHIGL ChatGPT App!"
    echo ""
else
    echo -e "${YELLOW}⚠️  APK not found!${NC}"
    echo "Build may have failed. Check the output above."
fi
