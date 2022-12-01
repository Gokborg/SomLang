import tokens as token
from typing import Union, Optional


#Expressions (Numbers/Identifiers/BinOp)
#=======================================
class Expression:
  pass


class Identifier(Expression):

  def __init__(self, token: token.Token):
    self.token = token

  def __repr__(self):
    return "Identifier(" + self.token.value + ")"

  def __str__(self):
    return "Identifier(" + self.token.value + ")"


class Number(Expression):

  def __init__(self, token: token.Token):
    self.token = token

  def __repr__(self):
    return "Number(" + self.token.value + ")"

  def __str__(self):
    return "Number(" + self.token.value + ")"


class BinOp(Expression):

  def __init__(self, expr1: Expression, op: token.Token, expr2: Expression):
    self.expr1 = expr1
    self.op = op
    self.expr2 = expr2

  def __str__(self):
    return "BinOp(" + str(self.expr1) + ", " + self.op.value + ", " + str(
      self.expr2) + ")"


#Statements (Declaration/Assignment/etc..)
#=======================================
class Statement:
  pass


class Block:

  def __init__(self, content: "Optional[list[Statement]]" = None):
    self.content = content if content is not None else []

  def __str__(self):
    s = ""
    for stmt in self.content:
      s += "\t\t" + str(stmt) + "\n"
    return s + ""

class IfStatement(Statement):

  def __init__(self, condition: Expression, block: Block, _else: "Union[None, Block, IfStatement]"):
    self.condition = condition
    self.block = block
    self.else_ = _else

  def __str__(self):
    return "If\n\tCond: " + str(self.condition) + "\n\tBlock: " + str(
      self.block) + "\n\telse: " + str(self.else_)

class WhileStatement(Statement):

  def __init__(self, condition: Expression, block: Block):
    self.condition = condition
    self.block = block

  def __str__(self):
    return "While\n\tCond: " + str(self.condition) + "\n\tBlock: " + str(
      self.block)


class MacroDeclaration(Statement):

  def __init__(self, name: Identifier, arguments: "list[Expression]", body: Block):
    self.name = name
    self.arguments = arguments
    self.body = body

  def __str__(self):
    return "Inline\n\tArgs: " + str(self.arguments) + "\n\tBlock:\n" + str(
      self.body)


class MacroCall(Statement):

  def __init__(self, name: Identifier, arguments: "list[Expression]"):
    self.name = name
    self.arguments = arguments

  def __str__(self):
    return f"MacroCall(name: {self.name} Args: {str(self.arguments)})"


class Declaration(Statement):

  def __init__(self, vartype: token.Token, identifier: Identifier,
               expr: Optional[Expression]):
    self.vartype = vartype
    self.identifier = identifier
    self.expr = expr

  def __str__(self):
    return "Declaration(type: " + self.vartype.value + ", name: " + str(
      self.identifier) + ", expr: " + str(self.expr) + ")"


class Assignment(Statement):

  def __init__(self, identifier: Identifier, expr: Expression):
    self.identifier = identifier
    self.expr = expr

  def __str__(self):
    return "Assign(name: " + str(self.identifier) + ", expr: " + str(
      self.expr) + ")"
