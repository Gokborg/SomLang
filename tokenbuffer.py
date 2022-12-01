from errortools import gen_error, gen_errormsg
from tokens import Token, Kind


class TokenBuffer:

  def set(self, content: "list[Token]"):
    self.pos: int = 0
    self.done: bool = False
    self.content = content
    self.current: Token = self.content[self.pos]
    #Saving last token for better errors so when the buffer
    #is finished we can see the last token it was working on
    self.lastToken: Token = self.content[self.pos]

  def next(self) -> Token:
    self.pos += 1
    if (self.pos < len(self.content)):
      self.current = self.content[self.pos]
      self.lastToken = self.current
    else:
      self.done = True
      self.current = Token(Kind.NONE, self.lastToken.value,
                           self.lastToken.line, self.lastToken.lineno,
                           self.lastToken.start)
    return self.current

  def expect_next_legacy(self, kind: Kind) -> Token:
    if self.next().eq(kind):
      return self.current
    else:
      gen_error(
        self.current, "Expected token kind '" + kind.name + "' next, got '" +
        self.current.kind.name + "'")

  def expect_legacy(self, kind: Kind) -> Token:
    if self.current.eq(kind):
      return self.current
    else:
      gen_error(
        self.current, "Expected token kind '" + kind.name + "', got '" +
        self.current.kind.name + "'")

  def expect(self, kind: Kind) -> Token:
    c = self.current
    if c.eq(kind):
      self.next()
      return c
    else:
      gen_error(
        c,
        "Expected token kind '" + kind.name + "', got '" + c.kind.name + "'")

  def expect_current(self, kind: Kind) -> Token:
    c = self.current
    if c.eq(kind):
      return c
    else:
      gen_error(
        c,
        "Expected token kind '" + kind.name + "', got '" + c.kind.name + "'")
