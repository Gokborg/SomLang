from token import Token, Kind
from errortools import gen_error, gen_errormsg
import ast
import tokenbuffer
import exprparser

class Parser:
  def parse(self, tokens: [Token]):
    ast_nodes = []
    self.buf = tokenbuffer.TokenBuffer()
    self.buf.set(tokens)
    self.expr_parser = exprparser.ExpressionParser(self.buf)
    while not self.buf.done:
      ast_nodes.append(self.parse_stmt())
    return ast_nodes

  def parse_stmt(self) -> ast.Statement:
    if self.buf.current.eq(Kind.VAR_TYPE):
      return self.parse_declaration()
    elif self.buf.current.eq(Kind.IDENTIFIER):
      return self.parse_assignment()
    elif self.buf.current.eq(Kind.IF):
      return self.parse_if()
    else:
      gen_error(self.buf.current, "Failed to parse statement!")

  def parse_if(self) -> ast.IfStatement:
    self.buf.expect(Kind.IF)
    self.buf.next()
    cond_node = self.expr_parser.parse()
    return ast.IfStatement(cond_node, self.parse_block())
  
  def parse_block(self) -> ast.Block:
    self.buf.expect(Kind.OPEN_BRACE)
    block = ast.Block()
    self.buf.next()
    while not self.buf.current.eq(Kind.CLOSE_BRACE):
      block.content.append(self.parse_stmt())
    self.buf.next()
    return block

  def parse_assignment(self) -> ast.Assignment:
    identifier: Token = self.buf.expect(Kind.IDENTIFIER)
    self.buf.expect_next(Kind.EQUAL)
    self.buf.next() #Pointing to expr now
    expr: Expression = self.expr_parser.parse()
    return ast.Assignment(ast.Identifier(identifier), expr)
    
  def parse_declaration(self) -> ast.Declaration:
    vartype: Token = self.buf.expect(Kind.VAR_TYPE)
    identifier: Token = self.buf.expect_next(Kind.IDENTIFIER)
    self.buf.next()
    #uint a = SOMETHING;
    if self.buf.current.eq(Kind.EQUAL):
      self.buf.next() #Pointing to expr now
      expr: Expression = self.expr_parser.parse()
      decl = ast.Declaration(vartype, ast.Identifier(identifier), expr)
      self.buf.expect(Kind.SEMICOLON)
      self.buf.next()
      return decl
    #uint a;
    elif self.buf.current.eq(Kind.SEMICOLON):
      self.buf.next()
      return ast.Declaration(vartype, ast.Identifier(identifier), None)
    else:
      gen_error(identifier, "Missing semicolon?")
    
  