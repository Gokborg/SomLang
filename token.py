from enum import Enum, auto

class Pos:
  def __init__(self, line: str, lineno: int, start: int, end: int):
    self.line = line
    self.lineno = lineno
    self.start = start
    self.end = end

  def __str__(self):
    return "Pos(line#:" + str(self.lineno) + ", start: " + str(self.start) + ", end: " + str(self.end) + ")"
		

class Kind(Enum):
  
  IDENTIFIER = auto()
  NUMBER = auto()
  EQUAL = auto()

  NONE = auto()

class Token:
  def __init__(self, kind: Kind, value: str, pos: Pos):
    self.kind = kind
    self.value = value
    self.pos = pos
		
  def eq(self, kind: Kind):
    return self.kind == kind
		
  def __str__(self):
    return "Token(kind: "+str(self.kind.name)+", value: " + self.value + ", " + self.pos.__str__() + ")"