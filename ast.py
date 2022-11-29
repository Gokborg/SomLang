import token

#Expressions (Numbers/Identifiers/BinOp)
#=======================================
class Expression:
  pass
  
class Identifier(Expression):
  def __init__(self, token: token.Token):
    self.token = token
  def __str__(self):
    return "Identifier(" + self.token.value + ")"

class Number(Expression):
  def __init__(self, token: token.Token):
    self.token = token
  def __str__(self):
    return "Number(" + self.token.value + ")"

class BinOp(Expression):
  def __init__(self, expr1: Expression, op: token.Token, expr2: Expression):
    self.expr1 = expr1
    self.op = op
    self.expr2 = expr2
  def __str__(self):
    return "BinOp(" + str(self.expr1) + ", " + self.op.value + ", " + str(self.expr2) + ")"

#Statements (Declaration/Assignment/etc..)
#=======================================
class Statement:
  pass

class Block:
  def __init__(self, content: [Statement] = []):
    self.content = content
  def __str__(self):
    s = ""
    for stmt in self.content:
      s += str(stmt) + "\n"
    return s

class IfStatement(Statement):
  def __init__(self, condition: Expression, block: Block):
    self.condition = condition
    self.block = block
  def __str__(self):
    return "If\n\tCond: " + str(self.condition) + "\n\tBlock:\n\t\t" + str(self.block)
  
class Declaration(Statement):
  def __init__(self, vartype: token.Token, identifier: Identifier, expr: Expression):
    self.vartype = vartype
    self.identifier = identifier
    self.expr = expr
  def __str__(self):
    return "Declaration(type: " + self.vartype.value + ", name: " + str(self.identifier) + ", expr: " + str(self.expr) + ")"

class Assignment(Statement): 
  def __init__(self, identifier: Identifier, expr: Expression):
    self.identifier = identifier
    self.expr = expr
  def __str__(self):
    return "Assign(name: " + str(self.identifier) + ", expr: " + str(self.expr) + ")"