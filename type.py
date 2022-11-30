from enum import Enum, auto

class Type():
  ...

class Primitive(Type, Enum):
  VOID = auto()
  UINT = auto()
  CHAR = auto()
  
  # future:
  INT = auto()
  BOOL = auto()

# future:
class Pointer(Type):
  def __init__(self, inner: Type):
    self.inner = inner

class Array(Type):
  def __init__(self, inner: Type):
    self.inner = inner

