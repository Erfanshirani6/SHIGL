#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Repository Analysis Tool
تجزیه و تحلیل جامع Repository SHIGL
"""

import os
import json
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class RepositoryAnalyzer:
    """تجزیه‌کننده Repository"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.stats = {
            "python_files": [],
            "shell_files": [],
            "total_lines": 0,
            "functions": 0,
            "classes": 0,
            "comments": 0,
            "commits": 0,
            "contributors": 0
        }
    
    def analyze_languages(self):
        """تجزیه زبان‌های استفاده شده"""
        print("\n" + "="*60)
        print("📊 تجزیه زبان‌های برنامه‌نویسی")
        print("="*60)
        
        language_stats = defaultdict(lambda: {"files": 0, "lines": 0})
        
        # Python files
        for py_file in Path(self.repo_path).rglob("*.py"):
            language_stats["Python"]["files"] += 1
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    language_stats["Python"]["lines"] += len(f.readlines())
                self.stats["python_files"].append(str(py_file))
            except:
                pass
        
        # Shell files
        for sh_file in Path(self.repo_path).rglob("*.sh"):
            language_stats["Shell"]["files"] += 1
            try:
                with open(sh_file, 'r', encoding='utf-8') as f:
                    language_stats["Shell"]["lines"] += len(f.readlines())
                self.stats["shell_files"].append(str(sh_file))
            except:
                pass
        
        # نمایش
        print("\n📘 Python:")
        print(f"   فایل‌ها: {language_stats['Python']['files']}")
        print(f"   خط‌های کد: {language_stats['Python']['lines']:,}")
        
        print("\n📜 Shell:")
        print(f"   فایل‌ها: {language_stats['Shell']['files']}")
        print(f"   خط‌های کد: {language_stats['Shell']['lines']:,}")
        
        self.stats["total_lines"] = (
            language_stats['Python']['lines'] + 
            language_stats['Shell']['lines']
        )
        
        print(f"\n📊 کل خط‌های کد: {self.stats['total_lines']:,}")
        
        return language_stats
    
    def analyze_code_structure(self):
        """تجزیه ساختار کد"""
        print("\n" + "="*60)
        print("🏗️ تجزیه ساختار کد")
        print("="*60)
        
        functions = 0
        classes = 0
        comments = 0
        
        for py_file in Path(self.repo_path).rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("def "):
                            functions += 1
                        elif line.startswith("class "):
                            classes += 1
                        elif line.startswith("#"):
                            comments += 1
            except:
                pass
        
        self.stats["functions"] = functions
        self.stats["classes"] = classes
        self.stats["comments"] = comments
        
        print(f"\n🔧 توابع (Functions): {functions}")
        print(f"📦 کلاس‌ها (Classes): {classes}")
        print(f"💬 تعداد کامنت‌ها: {comments}")
        
        if functions > 0:
            print(f"📈 میانگین توابع در فایل: {functions/len(list(Path(self.repo_path).rglob('*.py'))):.1f}")
    
    def analyze_git_history(self):
        """تجزیه تاریخچه Git"""
        print("\n" + "="*60)
        print("📚 تجزیه تاریخچه Git")
        print("="*60)
        
        try:
            # تعداد commits
            result = subprocess.run(
                ["git", "log", "--oneline"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            commits = len(result.stdout.strip().split('\n')) if result.stdout else 0
            self.stats["commits"] = commits
            print(f"\n📝 کل Commits: {commits}")
            
            # آخرین commit
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ai"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.stdout:
                print(f"📅 آخرین Commit: {result.stdout.strip()}")
            
            # تعداد Contributors
            result = subprocess.run(
                ["git", "shortlog", "-sn"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            contributors = len(result.stdout.strip().split('\n')) if result.stdout else 0
            self.stats["contributors"] = contributors
            print(f"👥 تعداد مشارکین: {contributors}")
            
        except Exception as e:
            print(f"⚠️ خطا در دریافت اطلاعات Git: {e}")
    
    def analyze_project_structure(self):
        """تجزیه ساختار پروژه"""
        print("\n" + "="*60)
        print("📁 ساختار پروژه")
        print("="*60)
        
        print("\n📂 دایرکتوری‌های اصلی:")
        
        main_dirs = set()
        for item in Path(self.repo_path).iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                main_dirs.add(item.name)
                file_count = len(list(item.rglob('*')))
                print(f"   📁 {item.name} ({file_count} فایل)")
        
        print("\n📄 فایل‌های اصلی:")
        
        important_files = {
            "README.md": "📖 مستندات",
            "setup.py": "⚙️ نصب",
            "requirements.txt": "📦 وابستگی‌ها",
            "Dockerfile": "🐳 Docker",
            ".gitignore": "🔐 Git Config",
            "LICENSE": "⚖️ مجوز"
        }
        
        for filename, description in important_files.items():
            path = Path(self.repo_path) / filename
            if path.exists():
                size = path.stat().st_size
                print(f"   {description}: {filename} ({size:,} bytes)")
    
    def generate_report(self):
        """ایجاد گزارش نهایی"""
        print("\n" + "="*60)
        print("📋 خلاصه تجزیه")
        print("="*60)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "repository": "Erfanshirani6/SHIGL",
            "repository_id": 1279180429,
            "language_composition": [
                {"name": "Python", "percent": 93.6},
                {"name": "Shell", "percent": 6.4}
            ],
            "statistics": self.stats
        }
        
        print("\n📊 آمار کلی:")
        print(f"   • کل خط‌های کد: {self.stats['total_lines']:,}")
        print(f"   • فایل‌های Python: {len(self.stats['python_files'])}")
        print(f"   • فایل‌های Shell: {len(self.stats['shell_files'])}")
        print(f"   • کلاس‌ها: {self.stats['classes']}")
        print(f"   • توابع: {self.stats['functions']}")
        print(f"   • کامنت‌ها: {self.stats['comments']}")
        print(f"   • Commits: {self.stats['commits']}")
        print(f"   • مشارکین: {self.stats['contributors']}")
        
        # ذخیره گزارش
        with open("repo_analysis_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("\n✅ گزارش در repo_analysis_report.json ذخیره شد")
        
        return report
    
    def generate_markdown_report(self):
        """ایجاد گزارش Markdown"""
        print("\n" + "="*60)
        print("📝 ایجاد گزارش Markdown")
        print("="*60)
        
        md_content = f"""# 📊 Repository Analysis Report

## Repository Information
- **Name**: Erfanshirani6/SHIGL
- **ID**: 1279180429
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Language Composition
| زبان | درصد | فایل‌ها |
|------|-----|--------|
| Python | 93.6% | {len(self.stats['python_files'])} |
| Shell | 6.4% | {len(self.stats['shell_files'])} |

## Code Statistics
| معیار | مقدار |
|------|-------|
| کل خط‌های کد | {self.stats['total_lines']:,} |
| تعداد کلاس‌ها | {self.stats['classes']} |
| تعداد توابع | {self.stats['functions']} |
| تعداد کامنت‌ها | {self.stats['comments']} |
| Commits | {self.stats['commits']} |
| مشارکین | {self.stats['contributors']} |

## Project Structure
### Python Files
"""
        
        for py_file in sorted(self.stats['python_files'])[:20]:
            md_content += f"- {py_file}\n"
        
        md_content += "\n### Shell Files\n"
        
        for sh_file in sorted(self.stats['shell_files'])[:10]:
            md_content += f"- {sh_file}\n"
        
        md_content += """
## Key Features
- 🤖 هوش مصنوعی مستقل
- 📱 تولید اپلیکیشن اندروید
- 🌐 مدیریت شبکه
- 🐙 یکپارچگی GitHub
- 💻 رابط خط فرمان

## Getting Started

### Requirements
- Python 3.8+
- Android SDK (برای ساخت APK)
- Git

### Installation
```bash
git clone https://github.com/Erfanshirani6/SHIGL.git
cd SHIGL
pip install -r requirements.txt
```

### Usage
```bash
python3 shigl_cli.py
python3 build_apk_direct.py
python3 weather_dashboard.py
```

---

*Generated by Repository Analysis Tool*
"""
        
        with open("ANALYSIS.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print("✅ گزارش Markdown در ANALYSIS.md ذخیره شد")
    
    def run_full_analysis(self):
        """اجرای تجزیه کامل"""
        print("\n" + "🔍 "*20)
        print("🔍 تجزیه جامع Repository SHIGL شروع می‌شود...")
        print("🔍 "*20)
        
        self.analyze_languages()
        self.analyze_code_structure()
        self.analyze_git_history()
        self.analyze_project_structure()
        self.generate_report()
        self.generate_markdown_report()
        
        print("\n" + "="*60)
        print("✅ تجزیه کامل شد!")
        print("="*60)
        print("\n📄 فایل‌های تولید شده:")
        print("   • repo_analysis_report.json")
        print("   • ANALYSIS.md")


def main():
    """تابع اصلی"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Repository Analysis Tool")
    parser.add_argument("--path", default=".", help="مسیر Repository")
    
    args = parser.parse_args()
    
    analyzer = RepositoryAnalyzer(repo_path=args.path)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
