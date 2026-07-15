# shigl/ai/local_llm.py
import subprocess
import json
from typing import Optional, Dict, Any
from pathlib import Path

class LocalLLM:
    """
    اجرای مدل‌های زبانی بزرگ به صورت کاملاً محلی
    پشتیبانی از: llama.cpp, Ollama, Atomic Chat
    """
    
    def __init__(self, model_path: Optional[str] = None, backend: str = "llama.cpp"):
        self.backend = backend
        self.model_path = model_path or self._get_default_model()
        self.is_running = False
        
    def _get_default_model(self) -> str:
        """پیدا کردن مدل پیش‌فرض"""
        # بررسی وجود مدل در مسیرهای رایج
        paths = [
            Path.home() / ".shigl" / "models" / "llama-3.2-3b.Q4_K_M.gguf",
            Path.home() / "models" / "llama-3.2-3b.Q4_K_M.gguf",
            Path("/usr/local/share/models/llama-3.2-3b.Q4_K_M.gguf")
        ]
        for p in paths:
            if p.exists():
                return str(p)
        return ""
    
    def start_server(self, host: str = "127.0.0.1", port: int = 8080) -> bool:
        """راه‌اندازی سرور OpenAI-compatible"""
        if not self.model_path:
            print("❌ مدلی پیدا نشد! لطفاً یک مدل نصب کنید.")
            print("💡 راهنما: shigl ai install-model")
            return False
        
        try:
            # استفاده از llama.cpp به عنوان سرور
            cmd = [
                "llama-server",
                "-m", self.model_path,
                "--host", host,
                "--port", str(port),
                "-c", "4096",
                "--api-key", "shigl-local-key"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.is_running = True
            self.host = host
            self.port = port
            print(f"✅ سرور محلی روی http://{host}:{port} در حال اجراست")
            return True
            
        except FileNotFoundError:
            print("❌ llama-server نصب نیست!")
            print("💡 نصب: pip install llama-cpp-python")
            return False
    
    def generate(self, prompt: str, system_prompt: str = "", 
                 max_tokens: int = 512) -> str:
        """تولید متن با مدل محلی"""
        if not self.is_running:
            print("⚠️ سرور اجرا نیست! راه‌اندازی...")
            if not self.start_server():
                return "❌ خطا: مدل محلی در دسترس نیست"
        
        import requests
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/v1/chat/completions",
                json={
                    "model": "local",
                    "messages": messages,
                    "max_tokens": max_tokens
                },
                headers={"Authorization": "Bearer shigl-local-key"},
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"❌ خطا در ارتباط با مدل: {response.status_code}"
                
        except Exception as e:
            return f"❌ خطا: {e}"
    
    def think(self, question: str, context: str = "") -> Dict[str, Any]:
        """تفکر عمیق با مدل محلی"""
        system = """شما SHIGL-AI هستید، یک هوش مصنوعی خودمختار.
        وظیفه شما: تحلیل عمیق، استدلال منطقی و ارائه راه‌حل‌های خلاقانه.
        پاسخ‌های خود را به صورت ساختاریافته و با دلایل ارائه دهید.
        """
        
        if context:
            prompt = f"""زمینه:
{context}

سوال:
{question}

لطفاً عمیقاً فکر کنید، گام‌به‌گام استدلال کنید و پاسخ کامل دهید."""
        else:
            prompt = f"""سوال: {question}

لطفاً عمیقاً فکر کنید، گام‌به‌گام استدلال کنید و پاسخ کامل دهید."""
        
        response = self.generate(prompt, system_prompt=system, max_tokens=1024)
        
        return {
            "question": question,
            "answer": response,
            "model": self.model_path,
            "backend": self.backend
              }
