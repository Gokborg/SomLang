from tokens import Token, Kind
from errortools import gen_error, gen_errormsg
import asts as ast
import tokenbuffer
import exprparser


class Parser:

  def parse(self, tokens: "list[Token]") -> "list[ast.Statement]":
    ast_nodes: "list[ast.Statement]" = []
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
    elif self.buf.current.eq(Kind.WHILE):
      return self.parse_while()
    elif self.buf.current.eq(Kind.MACRO):
      return self.parse_macro()
    elif self.buf.current.eq(Kind.MACROCALL):
      return self.parse_macro_call()
    else:
      gen_error(self.buf.current, "Failed to parse statement!")

  def parse_macro_call(self):
    self.buf.expect_current(Kind.MACROCALL)
    name_token = self.buf.current
    self.buf.next()
    
    arguments = self.parse_arguments()
    self.buf.expect(Kind.SEMICOLON)
    
    return ast.MacroCall(ast.Identifier(name_token), arguments)

  def parse_if(self) -> ast.IfStatement:
    # FIXME: maybe check if it is if or elif
    self.buf.next()
    cond_node = self.expr_parser.parse()
    if_block = self.parse_block()
    
    if self.buf.current.eq(Kind.ELSE):
      self.buf.next()
      else_block = self.parse_block()
      return ast.IfStatement(cond_node, if_block, else_block)
      
    elif self.buf.current.eq(Kind.ELIF):
      else_part = self.parse_if()
      return ast.IfStatement(cond_node, if_block, else_part)
    
    return ast.IfStatement(cond_node, if_block, None)

  def parse_while(self) -> ast.WhileStatement:
    self.buf.expect(Kind.WHILE)
    cond_node = self.expr_parser.parse()
    if isinstance(cond_node, ast.Number) or isinstance(cond_node, ast.Identifier):
        binop = ast.BinOp(
          cond_node, 
          Token(Kind.COND_NE, "!=", cond_node.token.line, cond_node.token.lineno, cond_node.token.start), 
          ast.Number(Token(Kind.NUMBER, "0", cond_node.token.line, cond_node.token.lineno, cond_node.token.start)))
        cond_node = binop
    assert isinstance(cond_node, ast.BinOp)
    block = self.parse_block()
    return ast.WhileStatement(cond_node, block)

  def parse_macro(self) -> ast.MacroDeclaration:
    self.buf.expect(Kind.MACRO)
    name = ast.Identifier(self.buf.expect(Kind.IDENTIFIER))
    args= self.parse_arguments()
    return ast.MacroDeclaration(name, args, self.parse_block())

  def parse_arguments(self) -> "list[ast.Expression]":
    arguments: "list[ast.Expression]" = []
    self.buf.expect(Kind.OPEN_PARAN)
    if self.buf.current.eq(Kind.CLOSE_PARAN):
      self.buf.next()
      return arguments
    arguments.append(self.expr_parser.parse())

    while not self.buf.current.eq(Kind.CLOSE_PARAN):
      self.buf.expect(Kind.COMMA)
      arguments.append(self.expr_parser.parse())

    self.buf.next()
    return arguments

  def parse_block(self) -> ast.Block:
    self.buf.expect(Kind.OPEN_BRACE)
    block = ast.Block()
    while not self.buf.current.eq(Kind.CLOSE_BRACE):
      block.content.append(self.parse_stmt())
    self.buf.next()
    return block

  def parse_assignment(self) -> ast.Assignment:
    identifier: Token = self.buf.expect(Kind.IDENTIFIER)
    self.buf.expect(Kind.EQUAL)
    expr: ast.Expression = self.expr_parser.parse()
    self.buf.expect(Kind.SEMICOLON)
    return ast.Assignment(ast.Identifier(identifier), expr)

  def parse_declaration(self) -> ast.Declaration:
    vartype: Token = self.buf.expect(Kind.VAR_TYPE)
    identifier: Token = self.buf.expect(Kind.IDENTIFIER)
    #uint a = SOMETHING;
    if self.buf.current.eq(Kind.EQUAL):
      self.buf.next()  #Pointing to expr now
      expr: ast.Expression = self.expr_parser.parse()
      decl = ast.Declaration(vartype, ast.Identifier(identifier), expr)
      self.buf.expect(Kind.SEMICOLON)
      return decl
    #uint a;
    elif self.buf.current.eq(Kind.SEMICOLON):
      self.buf.next()
      return ast.Declaration(vartype, ast.Identifier(identifier), None)
    else:
      gen_error(identifier, "Missing semicolon?")
