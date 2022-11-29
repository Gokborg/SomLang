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

#Statements (Declaration/Assignment/etc..)
#=======================================
class Declaration:
  def __init__(self, vartype: token.Token, identifier: Identifier, expr: Expression):
    self.vartype = vartype
    self.identifier = identifier
    self.expr = expr
  def __str__(self):
    return "Declaration(" + self.vartype.value + ", " + str(self.identifier) + ", " + str(self.expr) + ")"