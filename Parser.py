# shigl/parser.py
from typing import List, Optional
from .lexer import Token, TokenType
from .ast import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Token:
        return self.tokens[self.position]
    
    def peek_token(self, offset: int = 1) -> Token:
        if self.position + offset < len(self.tokens):
            return self.tokens[self.position + offset]
        return self.tokens[-1]
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        self.position += 1
        return token
    
    def parse(self) -> Program:
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        token = self.current_token()
        
        if token.type == TokenType.LET:
            return self.parse_let_statement()
        elif token.type == TokenType.FN:
            return self.parse_function_literal()
        elif token.type == TokenType.IF:
            return self.parse_if_expression()
        elif token.type == TokenType.FOR:
            return self.parse_for_expression()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.ANDROID:
            return self.parse_android_app()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self) -> LetStatement:
        self.expect(TokenType.LET)
        name_token = self.expect(TokenType.IDENT)
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return LetStatement(name_token.value, value)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_function_literal(self) -> FunctionLiteral:
        self.expect(TokenType.FN)
        name_token = self.expect(TokenType.IDENT)
        self.expect(TokenType.LPAREN)
        parameters = []
        if self.current_token().type != TokenType.RPAREN:
            while True:
                param = self.expect(TokenType.IDENT)
                parameters.append(param.value)
                if self.current_token().type == TokenType.COMMA:
                    self.expect(TokenType.COMMA)
                else:
                    break
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        return_type = self.expect(TokenType.IDENT)
        body = self.parse_block_statement()
        return FunctionLiteral(parameters, body)
    
    def parse_if_expression(self) -> IfExpression:
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        consequence = self.parse_block_statement()
        alternative = None
        if self.current_token().type == TokenType.ELSE:
            self.expect(TokenType.ELSE)
            alternative = self.parse_block_statement()
        return IfExpression(condition, consequence, alternative)
    
    def parse_for_expression(self) -> ForExpression:
        self.expect(TokenType.FOR)
        var = self.expect(TokenType.IDENT)
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        body = self.parse_block_statement()
        return ForExpression(var.value, iterable, body)
    
    def parse_block_statement(self) -> BlockStatement:
        self.expect(TokenType.LBRACE)
        statements = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return BlockStatement(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        if self.current_token().type == TokenType.SEMICOLON:
            self.expect(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> Expression:
        return self.parse_binary_expression()
    
    def parse_binary_expression(self, precedence: int = 0) -> Expression:
        left = self.parse_primary()
        
        while self.current_token().type != TokenType.SEMICOLON and self.current_token().type != TokenType.RBRACE:
            if self.current_token().type in [TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, 
                                            TokenType.LTE, TokenType.GTE, TokenType.AND, TokenType.OR,
                                            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH]:
                op = self.current_token().value
                self.position += 1
                right = self.parse_primary()
                left = InfixExpression(left, op, right)
            else:
                break
        
        return left
    
    def parse_primary(self) -> Expression:
        token = self.current_token()
        
        if token.type == TokenType.IDENT:
            self.position += 1
            if self.current_token().type == TokenType.LPAREN:
                return self.parse_call_expression(token.value)
            return Identifier(token.value)
        elif token.type == TokenType.NUMBER:
            self.position += 1
            return NumberLiteral(float(token.value))
        elif token.type == TokenType.STRING:
            self.position += 1
            return StringLiteral(token.value)
        elif token.type == TokenType.TRUE:
            self.position += 1
            return BooleanLiteral(True)
        elif token.type == TokenType.FALSE:
            self.position += 1
            return BooleanLiteral(False)
        elif token.type == TokenType.LPAREN:
            self.position += 1
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif token.type == TokenType.FN:
            return self.parse_function_literal()
        else:
            raise SyntaxError(f"Unexpected token: {token.type} at line {token.line}")
    
    def parse_call_expression(self, name: str) -> CallExpression:
        self.expect(TokenType.LPAREN)
        arguments = []
        if self.current_token().type != TokenType.RPAREN:
            while True:
                arg = self.parse_expression()
                arguments.append(arg)
                if self.current_token().type == TokenType.COMMA:
                    self.expect(TokenType.COMMA)
                else:
                    break
        self.expect(TokenType.RPAREN)
        return CallExpression(Identifier(name), arguments)
    
    def parse_android_app(self) -> AndroidApp:
        self.expect(TokenType.ANDROID)
        self.expect(TokenType.APP)
        name_token = self.expect(TokenType.IDENT)
        self.expect(TokenType.LBRACE)
        
        package = "com.example.shigl"
        minSdk = 21
        targetSdk = 34
        activities = []
        permissions = []
        
        while self.current_token().type != TokenType.RBRACE:
            token = self.current_token()
            if token.type == TokenType.IDENT:
                if token.value == "package":
                    self.position += 1
                    self.expect(TokenType.ASSIGN)
                    pkg = self.expect(TokenType.STRING)
                    package = pkg.value
                elif token.value == "minSdk":
                    self.position += 1
                    self.expect(TokenType.ASSIGN)
                    sdk = self.expect(TokenType.NUMBER)
                    minSdk = int(sdk.value)
                elif token.value == "targetSdk":
                    self.position += 1
                    self.expect(TokenType.ASSIGN)
                    sdk = self.expect(TokenType.NUMBER)
                    targetSdk = int(sdk.value)
                elif token.value == "activity":
                    self.position += 1
                    act = self.parse_android_activity()
                    activities.append(act)
                elif token.value == "permission":
                    self.position += 1
                    perm = self.expect(TokenType.STRING)
                    permissions.append(perm.value)
                else:
                    self.position += 1
            else:
                self.position += 1
        
        self.expect(TokenType.RBRACE)
        return AndroidApp(name_token.value, package, minSdk, targetSdk, activities, permissions)
    
    def parse_android_activity(self) -> AndroidActivity:
        name_token = self.expect(TokenType.IDENT)
        self.expect(TokenType.LBRACE)
        
        layout = "activity_main"
        label = "SHIGL App"
        
        while self.current_token().type != TokenType.RBRACE:
            token = self.current_token()
            if token.type == TokenType.IDENT:
                if token.value == "layout":
                    self.position += 1
                    self.expect(TokenType.ASSIGN)
                    lay = self.expect(TokenType.STRING)
                    layout = lay.value
                elif token.value == "label":
                    self.position += 1
                    self.expect(TokenType.ASSIGN)
                    lab = self.expect(TokenType.STRING)
                    label = lab.value
                else:
                    self.position += 1
            else:
                self.position += 1
        
        self.expect(TokenType.RBRACE)
        return AndroidActivity(name_token.value, layout, label)