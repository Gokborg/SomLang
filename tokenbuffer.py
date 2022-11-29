from errortools import gen_error, gen_errormsg
from token import Token, Kind

class TokenBuffer: 
  def set(self, content: [Token]):
    self.pos: int = 0
    self.done: bool = False
    self.content = content
    self.current: Token = self.content[self.pos]
  def next(self) -> Token:
    self.pos += 1
    if(self.pos < len(self.content)):
      self.current = self.content[self.pos]
    else:
      self.done = True
      self.current = Token(Kind.NONE, "\0", "\0", 1, 0)
    return self.current
  def expect_next(self, kind: Kind) -> Token:
    if self.next().eq(kind):
      return self.current
    else:
      gen_error(self.current, "Expected token kind '" + kind.name + "' next, got '" + self.current.kind.name + "'")
  def expect(self, kind: Kind) -> Token:
    if self.current.eq(kind):
      return self.current
    else:
      gen_error(self.current, "Expected token kind '" + kind.name + "', got '" + self.current.kind.name + "'")