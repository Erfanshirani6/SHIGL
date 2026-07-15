# shigl/github/client.py
from typing import Optional, List, Dict, Any
from pathlib import Path
import os

class GitHubClient:
    """
    کلاینت گیت‌هاب برای SHIGL
    قابلیت‌ها: Clone, Commit, Push, PR, Issue, Code Search
    """
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self._init_client()
    
    def _init_client(self):
        """راه‌اندازی کلاینت گیت‌هاب"""
        try:
            from githubkit import GitHub
            
            if self.token:
                self.client = GitHub(self.token)
                print("✅ GitHub client initialized")
            else:
                print("⚠️ GitHub token not found. Some features may not work.")
                self.client = GitHub()
                
        except ImportError:
            print("❌ githubkit نصب نیست!")
            print("💡 pip install githubkit")
            self.client = None
    
    def clone_repo(self, repo_url: str, target_dir: str) -> bool:
        """کلون کردن مخزن"""
        import subprocess
        
        try:
            subprocess.run(
                ["git", "clone", repo_url, target_dir],
                check=True,
                capture_output=True
            )
            print(f"✅ Repository cloned to {target_dir}")
            return True
        except Exception as e:
            print(f"❌ خطا در کلون: {e}")
            return False
    
    def create_pr(self, repo: str, title: str, body: str, 
                  head: str, base: str = "main") -> Optional[Dict]:
        """ایجاد Pull Request"""
        if not self.client:
            return None
        
        try:
            # تقسیم repo به owner/name
            parts = repo.split("/")
            if len(parts) != 2:
                return None
            
            response = self.client.rest.pulls.create(
                owner=parts[0],
                repo=parts[1],
                title=title,
                body=body,
                head=head,
                base=base
            )
            
            data = response.parsed_data
            print(f"✅ PR created: {data.html_url}")
            return {
                "url": data.html_url,
                "number": data.number,
                "state": data.state
            }
            
        except Exception as e:
            print(f"❌ خطا در ایجاد PR: {e}")
            return None
    
    def create_issue(self, repo: str, title: str, body: str) -> Optional[Dict]:
        """ایجاد Issue"""
        if not self.client:
            return None
        
        try:
            parts = repo.split("/")
            if len(parts) != 2:
                return None
            
            response = self.client.rest.issues.create(
                owner=parts[0],
                repo=parts[1],
                title=title,
                body=body
            )
            
            data = response.parsed_data
            print(f"✅ Issue created: {data.html_url}")
            return {
                "url": data.html_url,
                "number": data.number,
                "state": data.state
            }
            
        except Exception as e:
            print(f"❌ خطا در ایجاد Issue: {e}")
            return None
    
    def search_code(self, query: str) -> List[Dict]:
        """جستجوی کد در گیت‌هاب"""
        if not self.client:
            return []
        
        try:
            response = self.client.rest.search.code(
                q=query,
                per_page=10
            )
            
            results = []
            for item in response.parsed_data.items:
                results.append({
                    "name": item.name,
                    "path": item.path,
                    "url": item.html_url,
                    "repo": item.repository.full_name
                })
            
            return results
            
        except Exception as e:
            print(f"❌ خطا در جستجو: {e}")
            return []
    
    def auto_fix_code(self, repo: str, file_path: str, issue_description: str) -> str:
        """
        تحلیل و رفع خودکار باگ با استفاده از AI
        """
        # دریافت محتوای فایل
        if not self.client:
            return "❌ GitHub client not initialized"
        
        try:
            parts = repo.split("/")
            if len(parts) != 2:
                return "❌ Invalid repo format"
            
            # دریافت فایل
            response = self.client.rest.repos.get_content(
                owner=parts[0],
                repo=parts[1],
                path=file_path
            )
            
            # اینجا باید محتوا را decode کنیم
            import base64
            content = base64.b64decode(
                response.parsed_data.content
            ).decode('utf-8')
            
            # استفاده از SHIGL AI برای تحلیل
            from shigl.ai.agent import SHIGLAgent
            agent = SHIGLAgent()
            
            prompt = f"""کد زیر را بررسی کن و باگ‌های آن را پیدا کن:

```python
{content}
