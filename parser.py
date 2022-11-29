from token import Token, Kind
from errortools import gen_error, gen_errormsg
import ast

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

class Parser:
  def parse(self, tokens: [Token]):
    ast_nodes = []
    self.buf = TokenBuffer()
    self.buf.set(tokens)
    while not self.buf.done:
      if self.buf.current.eq(Kind.VAR_TYPE):
        ast_nodes.append(self.parse_declaration())
      else:
        self.buf.next()
    return ast_nodes

  def parse_declaration(self) -> ast.Declaration:
    vartype: Token = self.expect(Kind.VAR_TYPE)
    identifier: Token = self.expect_next(Kind.IDENTIFIER)
    self.buf.next()
    #uint a = SOMETHING;
    if self.buf.current.eq(Kind.EQUAL):
      self.buf.next() #Pointing to expr now
      expr: Expression = self.parse_expr()
      decl = ast.Declaration(vartype, ast.Identifier(identifier), expr)
      self.expect(Kind.SEMICOLON)
      self.buf.next()
      return decl
      
    #uint a;
    elif self.buf.current.eq(Kind.SEMICOLON):
      self.buf.next()
      return ast.Declaration(vartype, ast.Identifier(identifier), None)

    else:
      gen_error(identifier, "Missing semicolon?")

  def parse_expr(self) -> ast.Expression:
    current: Token = self.buf.current
    self.buf.next()
    if current.eq(Kind.NUMBER):
      return ast.Number(current)
    elif current.eq(Kind.IDENTIFIER):
      return ast.Identifier(current)
    else:
      gen_error(current, "Failed to parse expression!")
    

  def expect_next(self, kind: Kind):
    if self.buf.next().eq(kind):
      return self.buf.current
    else:
      gen_error(self.buf.current, "Expected token kind '" + kind.name + "' next, got '" + self.buf.current.kind.name + "'")

  def expect(self, kind: Kind):
    if self.buf.current.eq(kind):
      return self.buf.current
    else:
      gen_error(self.buf.current, "Expected token kind '" + kind.name + "', got '" + self.buf.current.kind.name + "'")
    
  