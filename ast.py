# shigl/ast.py
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class ASTNode:
    pass

# ===== Statements =====
@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

@dataclass
class LetStatement(ASTNode):
    name: str
    value: 'Expression'

@dataclass
class ReturnStatement(ASTNode):
    value: 'Expression'

@dataclass
class ExpressionStatement(ASTNode):
    expression: 'Expression'

@dataclass
class BlockStatement(ASTNode):
    statements: List[ASTNode]

# ===== Expressions =====
@dataclass
class Identifier(ASTNode):
    value: str

@dataclass
class NumberLiteral(ASTNode):
    value: float

@dataclass
class StringLiteral(ASTNode):
    value: str

@dataclass
class BooleanLiteral(ASTNode):
    value: bool

@dataclass
class InfixExpression(ASTNode):
    left: 'Expression'
    operator: str
    right: 'Expression'

@dataclass
class PrefixExpression(ASTNode):
    operator: str
    right: 'Expression'

@dataclass
class CallExpression(ASTNode):
    function: 'Expression'
    arguments: List['Expression']

@dataclass
class FunctionLiteral(ASTNode):
    parameters: List[str]
    body: BlockStatement

@dataclass
class IfExpression(ASTNode):
    condition: 'Expression'
    consequence: BlockStatement
    alternative: Optional[BlockStatement]

@dataclass
class ForExpression(ASTNode):
    variable: str
    iterable: 'Expression'
    body: BlockStatement

@dataclass
class RangeLiteral(ASTNode):
    start: 'Expression'
    end: 'Expression'

# ===== Android =====
@dataclass
class AndroidApp(ASTNode):
    name: str
    package: str
    minSdk: int
    targetSdk: int
    activities: List['AndroidActivity']
    permissions: List[str]

@dataclass
class AndroidActivity(ASTNode):
    name: str
    layout: str
    label: str