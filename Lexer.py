# shigl/lexer.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Keywords
    LET = "LET"
    FN = "FN"
    IF = "IF"
    ELSE = "ELSE"
    FOR = "FOR"
    IN = "IN"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    ANDROID = "ANDROID"
    APP = "APP"
    ACTIVITY = "ACTIVITY"
    
    # Identifiers & Literals
    IDENT = "IDENT"
    STRING = "STRING"
    NUMBER = "NUMBER"
    
    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    AND = "&&"
    OR = "||"
    NOT = "!"
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COLON = ":"
    SEMICOLON = ";"
    COMMA = ","
    DOT = "."
    ARROW = "->"
    RANGE = ".."
    
    # Special
    COMMENT = "COMMENT"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords map
        self.keywords = {
            'let': TokenType.LET,
            'fn': TokenType.FN,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'in': TokenType.IN,
            'return': TokenType.RETURN,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'android': TokenType.ANDROID,
            'app': TokenType.APP,
            'activity': TokenType.ACTIVITY,
        }
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            char = self.current_char()
            
            if char.isspace():
                self.skip_whitespace()
                continue
            
            if char == '/':
                if self.peek() == '/':
                    self.skip_comment()
                    continue
            
            if char.isdigit():
                self.read_number()
                continue
            
            if char == '"':
                self.read_string()
                continue
            
            if char.isalpha() or char == '_':
                self.read_identifier()
                continue
            
            self.read_operator_or_delimiter()
        
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.line, self.column))
        return self.tokens
    
    def current_char(self) -> str:
        return self.source[self.position] if self.position < len(self.source) else '\0'
    
    def peek(self) -> str:
        if self.position + 1 < len(self.source):
            return self.source[self.position + 1]
        return '\0'
    
    def advance(self):
        self.position += 1
        self.column += 1
    
    def skip_whitespace(self):
        while self.position < len(self.source):
            char = self.current_char()
            if char == '\n':
                self.line += 1
                self.column = 1
                self.advance()
            elif char.isspace():
                self.advance()
            else:
                break
    
    def skip_comment(self):
        self.advance()
        self.advance()
        while self.position < len(self.source) and self.current_char() != '\n':
            self.advance()
    
    def read_number(self):
        start_col = self.column
        num = ''
        while self.position < len(self.source) and self.current_char().isdigit():
            num += self.current_char()
            self.advance()
        
        if self.current_char() == '.' and self.peek().isdigit():
            num += '.'
            self.advance()
            while self.position < len(self.source) and self.current_char().isdigit():
                num += self.current_char()
                self.advance()
        
        self.tokens.append(Token(TokenType.NUMBER, num, self.line, start_col))
    
    def read_string(self):
        start_col = self.column
        self.advance()  # Skip opening quote
        string = ''
        while self.position < len(self.source) and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    string += '\n'
                elif self.current_char() == 't':
                    string += '\t'
                else:
                    string += self.current_char()
            else:
                string += self.current_char()
            self.advance()
        self.advance()  # Skip closing quote
        self.tokens.append(Token(TokenType.STRING, string, self.line, start_col))
    
    def read_identifier(self):
        start_col = self.column
        ident = ''
        while self.position < len(self.source) and (self.current_char().isalnum() or self.current_char() == '_'):
            ident += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(ident, TokenType.IDENT)
        self.tokens.append(Token(token_type, ident, self.line, start_col))
    
    def read_operator_or_delimiter(self):
        char = self.current_char()
        start_col = self.column
        
        # Two-character operators
        if char == '=' and self.peek() == '=':
            self.tokens.append(Token(TokenType.EQ, '==', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '!' and self.peek() == '=':
            self.tokens.append(Token(TokenType.NEQ, '!=', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '<' and self.peek() == '=':
            self.tokens.append(Token(TokenType.LTE, '<=', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '>' and self.peek() == '=':
            self.tokens.append(Token(TokenType.GTE, '>=', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '&' and self.peek() == '&':
            self.tokens.append(Token(TokenType.AND, '&&', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '|' and self.peek() == '|':
            self.tokens.append(Token(TokenType.OR, '||', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '-' and self.peek() == '>':
            self.tokens.append(Token(TokenType.ARROW, '->', self.line, start_col))
            self.advance(); self.advance(); return
        if char == '.' and self.peek() == '.':
            self.tokens.append(Token(TokenType.RANGE, '..', self.line, start_col))
            self.advance(); self.advance(); return
        
        # Single-character operators/delimiters
        single_chars = {
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '<': TokenType.LT,
            '>': TokenType.GT,
            '!': TokenType.NOT,
        }
        
        if char in single_chars:
            self.tokens.append(Token(single_chars[char], char, self.line, start_col))
            self.advance()
        else:
            raise SyntaxError(f"Unexpected character: '{char}' at line {self.line}, column {self.column}")