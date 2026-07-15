# shigl/ai/agent.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from .local_llm import LocalLLM

@dataclass
class AgentGoal:
    """یک هدف برای عامل"""
    description: str
    status: str = "pending"  # pending, in_progress, done, failed
    result: Optional[str] = None

@dataclass
class AgentMemory:
    """حافظه عامل"""
    short_term: List[str] = field(default_factory=list)
    long_term: Dict[str, Any] = field(default_factory=dict)

class SHIGLAgent:
    """
    عامل هوشمند SHIGL
    می‌تواند: فکر کند، تصمیم بگیرد، ابزارها را فراخوانی کند، یاد بگیرد
    """
    
    def __init__(self, name: str = "SHIGL-Agent"):
        self.name = name
        self.llm = LocalLLM()
        self.memory = AgentMemory()
        self.goals: List[AgentGoal] = []
        self.tools: Dict[str, callable] = {}
        self._register_default_tools()
        
    def _register_default_tools(self):
        """ثبت ابزارهای پیش‌فرض"""
        self.tools["think"] = self.think
        self.tools["plan"] = self.plan
        self.tools["execute"] = self.execute
        self.tools["learn"] = self.learn
        self.tools["reflect"] = self.reflect
    
    def think(self, prompt: str) -> str:
        """تفکر عمیق"""
        print(f"🧠 {self.name} در حال تفکر...")
        result = self.llm.think(prompt)
        self.memory.short_term.append(f"Think: {prompt[:50]}...")
        return result.get("answer", "")
    
    def plan(self, goal: str) -> List[str]:
        """برنامه‌ریزی برای رسیدن به هدف"""
        print(f"📋 {self.name} در حال برنامه‌ریزی...")
        
        prompt = f"""هدف: {goal}

لطفاً یک برنامه عملیاتی گام‌به‌گام برای رسیدن به این هدف ارائه دهید.
هر گام باید مشخص، قابل اندازه‌گیری و عملی باشد.

فرمت پاسخ:
گام ۱: ...
گام ۲: ...
گام ۳: ...
"""
        
        response = self.llm.generate(prompt, max_tokens=512)
        steps = []
        for line in response.split('\n'):
            if line.strip().startswith('گام') or line.strip().startswith('Step'):
                steps.append(line.strip())
        
        self.goals.append(AgentGoal(description=goal, status="in_progress"))
        return steps if steps else [response]
    
    def execute(self, task: str) -> str:
        """اجرای یک کار"""
        print(f"⚡ {self.name} در حال اجرا: {task[:50]}...")
        
        # بررسی آیا کار نیاز به ابزار خاصی دارد
        for tool_name, tool_func in self.tools.items():
            if tool_name in task.lower():
                print(f"🔧 استفاده از ابزار: {tool_name}")
                try:
                    result = tool_func(task)
                    return f"✅ {result}"
                except Exception as e:
                    return f"❌ خطا در اجرا: {e}"
        
        # استفاده از LLM برای انجام کار
        prompt = f"""کار: {task}

لطفاً این کار را انجام دهید و نتیجه را گزارش کنید.
اگر به اطلاعات بیشتری نیاز دارید، بپرسید.
"""
        return self.llm.generate(prompt, max_tokens=256)
    
    def learn(self, experience: str) -> str:
        """یادگیری از تجربه"""
        print(f"📚 {self.name} در حال یادگیری...")
        
        # ذخیره در حافظه بلندمدت
        key = f"experience_{len(self.memory.long_term)}"
        self.memory.long_term[key] = {
            "experience": experience,
            "timestamp": "now"
        }
        
        prompt = f"""تجربه جدید: {experience}

از این تجربه چه چیزی یاد گرفتی؟ چگونه می‌توانی در آینده بهتر عمل کنی؟
"""
        return self.llm.generate(prompt, max_tokens=256)
    
    def reflect(self, question: str) -> str:
        """تفکر و تأمل"""
        print(f"🪞 {self.name} در حال تأمل...")
        
        # جمع‌آوری حافظه کوتاه‌مدت
        memory_text = "\n".join(self.memory.short_term[-10:])
        
        prompt = f"""سوال: {question}

حافظه اخیر:
{memory_text}

لطفاً با استفاده از تجربیات و حافظه خود، به این سوال پاسخ دهید.
"""
        return self.llm.generate(prompt, max_tokens=512)
    
    def run(self, task: str, autonomous: bool = True) -> str:
        """
        اجرای خودکار یک کار
        اگر autonomous=True باشد، عامل خودش تصمیم می‌گیرد چکار کند
        """
        print(f"🚀 {self.name} شروع به کار: {task}")
        
        if autonomous:
            # مرحله ۱: تفکر
            thought = self.think(f"چگونه می‌توانم این کار را انجام دهم: {task}")
            print(f"💭 فکر: {thought[:200]}...")
            
            # مرحله ۲: برنامه‌ریزی
            plan = self.plan(task)
            print(f"📋 برنامه: {plan}")
            
            # مرحله ۳: اجرا
            result = self.execute(task)
            
            # مرحله ۴: یادگیری
            self.learn(f"کار {task} انجام شد. نتیجه: {result[:100]}...")
            
            return f"""
✅ کار با موفقیت انجام شد!

💭 تفکر: {thought[:200]}...
📋 برنامه: {plan}
📊 نتیجه: {result}
"""
        else:
            return self.execute(task)
