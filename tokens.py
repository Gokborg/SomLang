from enum import Enum, auto

class Kind(Enum):
  VAR_TYPE = auto()

  IDENTIFIER = auto()
  NUMBER = auto()
  EQUAL = auto()
  PLUS = auto()
  MINUS = auto()
  MULT = auto()
  DIV = auto()

  MACROCALL = auto()

  COMMENT = auto()

  OPEN_BRACE = auto()
  CLOSE_BRACE = auto()
  IF = auto()
  ELSE = auto()
  ELIF = auto()
  WHILE = auto()
  MACRO = auto()
  COND_G = auto()
  COND_L = auto()
  COND_E = auto()
  COND_LE = auto()
  COND_NE = auto()
  COND_GE = auto()
  COMMA = auto()

  OPEN_PARAN = auto()
  CLOSE_PARAN = auto()

  SEMICOLON = auto()

  NONE = auto()


class Token:

  def __init__(self, kind: Kind, value: str, line: str, lineno: int,
               start: int):
    self.kind = kind
    self.value = value
    self.line = line
    self.lineno = lineno
    self.start = start

  def eq(self, kind: Kind):
    return self.kind == kind

  def __str__(self):
    return "Token(kind: " + str(
      self.kind.name) + ", value: " + self.value + ", lineno: " + str(
        self.lineno) + ", start: " + str(self.start) + ")"
