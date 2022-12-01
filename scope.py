from typing import Optional
from type import Type

class Scopes():
  def __init__(self):
    self.top: Scope = Scope()

  def push(self):
    self.top = Scope(self.top)

  def pop(self):
    assert self.top.parent is not None
    self.top = self.top.parent

  def put_var(self, name: str, type: Type):
    self.top.put_var(name, type)
  
  def get_var(self, name: str) -> "Optional[Variable]":
    return self.top.get_var(name)

class Scope():
  def __init__(self, parent: "Optional[Scope]" = None):
    self.parent: Optional[Scope] = parent
    self.variables: dict[str, Variable] = {}

  def put_var(self, name: str, type: Type) -> "Variable":
    assert self.get_var(name) is None
    variable = Variable(self, type)
    self.variables[name] = variable
    return variable
    
  
  def get_var(self, name: str) -> "Optional[Variable]":
    scope: Optional[Scope] = self
    variable: Optional[Variable] = None
    while variable is None and scope is not None:
      variable = scope.variables[name]
      scope = scope.parent
      
    return variable

class Variable():
  def __init__(self, scope: "Scope", type: Type):
    self.scope = scope
    self.type = type
