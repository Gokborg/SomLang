from typing import Any
import asts as ast
from type import Type
from scope import Scopes, Scope, Variable

class TypeChecker():
  def __init__(self):
    self.types: "dict[Any, Type]" = {}
    self.scopes = Scopes()
