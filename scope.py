from typing import Optional

class Scopes():
  def __init__(self):
    self.top = Scope()

  def push(self):
    self.top = scope(self.top)

  def pop(self):
    self.top = self.top.parent
    assert self.top is not None

  def put_var(self, name: str, type: Type):
    self.top.put_var(name, type)
  
  def get_var(self, name: str) -> "Optional[Variable]":
    return self.top.get_var(name)

class Scope():
  def __init__(self, parent: Optional[Scope] = None):
    self.parent = parent
    self.variables: dict[str, Variable] = {}

  def put_var(self, name: str, type: Type) -> Variable:
    assert get_var(name) is None
    self.variables[name] = Variable(self, type)
    
  
  def get_var(self, name: str) -> "Optional[Variable]":
    scope = self
    variable = scope.variables[name]
    while variable is None and scope is not None:
      scope = scope.parent
      variable = scope.variables[name]
      
    return variable

class Variable():
  def __init__(self, scope: "Scope", type: Type, start: int, end: int):
    self.scope = scope
    self.type = type
    self.start = start
    self.end = end
