from enum import Enum, auto

class Kind(Enum):
  VAR_TYPE = auto()
  IDENTIFIER = auto()
  NUMBER = auto()
  EQUAL = auto()
  SEMICOLON = auto()

  NONE = auto()

class Token:
  def __init__(self, kind: Kind, value: str, line: str, lineno: int, start: int):
    self.kind = kind
    self.value = value
    self.line = line
    self.lineno = lineno
    self.start = start
		
  def eq(self, kind: Kind):
    return self.kind == kind
		
  def __str__(self):
    return "Token(kind: "+str(self.kind.name)+", value: " + self.value + ", lineno: " + str(self.lineno) + ", start: " + str(self.start) + ")"