# ============================================
# SHIGL 2.0 - Advanced Interpreter
# ============================================

import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

class TokenType:
    """انواع توکن‌های زبان"""
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    OPERATOR = 'OPERATOR'
    EOF = 'EOF'

class Token:
    def __init__(self, type_: str, value: Any, line: int):
        self.type = type_
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    """تجزیه‌کننده واژگان - مرحله ۱"""
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.tokens = []
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.code):
            char = self.code[self.pos]
            
            # نادیده گرفتن فاصله‌ها
            if char.isspace():
                if char == '\n':
                    self.line += 1
                self.pos += 1
                continue
            
            # شناسایی اعداد
            if char.isdigit():
                self.tokens.append(self._read_number())
                continue
            
            # شناسایی رشته‌ها
            if char == '"' or char == "'":
                self.tokens.append(self._read_string())
                continue
            
            # شناسایی عملگرها
            if char in '=+-*/<>!':
                self.tokens.append(self._read_operator())
                continue
            
            # شناسایی کلمات کلیدی و شناسه‌ها
            if char.isalpha() or char == '_':
                self.tokens.append(self._read_identifier())
                continue
            
            raise SyntaxError(f"کاراکتر ناشناخته در خط {self.line}: {char}")
        
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.line))
        return self.tokens
    
    def _read_number(self) -> Token:
        num = ''
        while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == '.'):
            num += self.code[self.pos]
            self.pos += 1
        return Token(TokenType.NUMBER, float(num) if '.' in num else int(num), self.line)
    
    def _read_string(self) -> Token:
        quote = self.code[self.pos]
        self.pos += 1
        string = ''
        while self.pos < len(self.code) and self.code[self.pos] != quote:
            if self.code[self.pos] == '\\':
                self.pos += 1
                if self.pos < len(self.code):
                    string += self.code[self.pos]
            else:
                string += self.code[self.pos]
            self.pos += 1
        self.pos += 1  # رد شدن از quote پایانی
        return Token(TokenType.STRING, string, self.line)
    
    def _read_operator(self) -> Token:
        op = self.code[self.pos]
        self.pos += 1
        # عملگرهای دوکاراکتری
        if self.pos < len(self.code) and self.code[self.pos] in '=<>':
            op += self.code[self.pos]
            self.pos += 1
        return Token(TokenType.OPERATOR, op, self.line)
    
    def _read_identifier(self) -> Token:
        ident = ''
        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
            ident += self.code[self.pos]
            self.pos += 1
        return Token(TokenType.KEYWORD if ident in KEYWORDS else TokenType.IDENTIFIER, ident, self.line)

# ============================================
# کلمات کلیدی زبان SHIGL 2.0
# ============================================

KEYWORDS = {
    'say', 'var', 'if', 'else', 'elif', 'while', 'for',
    'func', 'return', 'import', 'class', 'try', 'catch',
    'true', 'false', 'null', 'and', 'or', 'not'
}

# ============================================
# مفسر اصلی
# ============================================

class SHIGLInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.output_buffer = []
        self.debug = False
    
    def evaluate(self, code: str) -> Any:
        """ورودی را تجزیه، اجرا و نتیجه را برمی‌گرداند"""
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            return self._parse_and_execute(tokens)
        except Exception as e:
            return f"❌ خطا: {e}"
    
    def _parse_and_execute(self, tokens: List[Token]) -> Any:
        """مرحله ۲ - تجزیه و اجرا"""
        # فعلاً ساده: فقط دستورات اولیه
        if not tokens:
            return None
        
        first = tokens[0]
        
        # دستور say
        if first.type == TokenType.KEYWORD and first.value == 'say':
            if len(tokens) < 2:
                return "❌ say نیاز به یک مقدار دارد"
            value = self._get_value(tokens[1])
            self.output_buffer.append(str(value))
            return value
        
        # دستور var
        elif first.type == TokenType.KEYWORD and first.value == 'var':
            if len(tokens) < 4 or tokens[2].value != '=':
                return "❌ ساختار var: var name = value"
            var_name = tokens[1].value
            var_value = self._get_value(tokens[3])
            self.variables[var_name] = var_value
            return var_value
        
        # دستورات ریاضی
        elif first.type == TokenType.KEYWORD and first.value in ['add', 'sub', 'mul', 'div']:
            if len(tokens) < 3:
                return f"❌ {first.value} نیاز به دو مقدار دارد"
            a = self._get_value(tokens[1])
            b = self._get_value(tokens[2])
            op = first.value
            return self._math_operation(op, a, b)
        
        else:
            # بررسی متغیرها در عبارات ساده
            if len(tokens) == 1 and tokens[0].type == TokenType.IDENTIFIER:
                var_name = tokens[0].value
                return self.variables.get(var_name, f"❌ متغیر {var_name} تعریف نشده")
            
            return f"❌ دستور ناشناخته: {first.value if tokens else ''}"
    
    def _get_value(self, token: Token) -> Any:
        """دریافت مقدار از توکن"""
        if token.type == TokenType.NUMBER:
            return token.value
        elif token.type == TokenType.STRING:
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            return self.variables.get(token.value, token.value)
        elif token.type == TokenType.KEYWORD:
            if token.value == 'true': return True
            if token.value == 'false': return False
            if token.value == 'null': return None
        return token.value
    
    def _math_operation(self, op: str, a: Any, b: Any) -> Any:
        """انجام عملیات ریاضی"""
        # تبدیل به عدد
        try:
            a = float(a) if not isinstance(a, (int, float)) else a
            b = float(b) if not isinstance(b, (int, float)) else b
        except:
            return f"❌ عملوندها باید عدد باشند: {a}, {b}"
        
        operations = {
            'add': a + b,
            'sub': a - b,
            'mul': a * b,
            'div': a / b if b != 0 else "❌ تقسیم بر صفر"
        }
        return operations.get(op, "❌ عملگر نامشخص")
    
    def repl(self):
        """حلقه تعاملی"""
        print("="*50)
        print("🚀 SHIGL 2.0 - Advanced Language")
        print("📝 دستورات: say, var, add/sub/mul/div, exit")
        print("="*50)
        
        while True:
            try:
                code = input("\nSHIGL> ").strip()
                if not code:
                    continue
                if code.lower() == 'exit':
                    print("👋 خروج از SHIGL")
                    break
                
                result = self.evaluate(code)
                if result is not None:
                    print(f"⬇️  {result}")
                
                if self.debug:
                    print(f"📦 متغیرها: {self.variables}")
                
            except KeyboardInterrupt:
                print("\n👋 خروج")
                break
            except Exception as e:
                print(f"❌ خطای سیستمی: {e}")

# ============================================
# اجرا
# ============================================

if __name__ == "__main__":
    interpreter = SHIGLInterpreter()
    interpreter.repl()
