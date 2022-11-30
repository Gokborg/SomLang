from token import Token, Kind
from errortools import gen_error, gen_errormsg
import ast
import tokenbuffer

class ExpressionParser:
  def __init__(self, buf: tokenbuffer.TokenBuffer):
    self.buf = buf

  #Generically parses a binary op used for all the binop parsing
  def generic_parse_binop(self, func, kinds: [Kind]) -> ast.BinOp:
    expr1 = func()
    while self.buf.current.kind in kinds:
      op: Token = self.buf.current
      self.buf.next()
      expr2 = func()
      expr1 = ast.BinOp(expr1, op, expr2)
    return expr1
   
  def parse(self) -> ast.Expression:
    return self.generic_parse_binop(
      self.parse_expr_l3,
      [Kind.COND_E, Kind.COND_GE, Kind.COND_LE, Kind.COND_G, Kind.COND_L]
    )
  
  def parse_expr_l3(self) -> ast.BinOp:
    return self.generic_parse_binop(
      self.parse_expr_l2,
      [Kind.PLUS, Kind.MINUS]
    )

  def parse_expr_l2(self) -> ast.BinOp:
    return self.generic_parse_binop(
      self.parse_expr_l1,
      [Kind.MULT, Kind.DIV]
    )

  def parse_expr_l1(self) -> ast.Expression:
    current: Token = self.buf.current
    self.buf.next()
    if current.eq(Kind.NUMBER):
      return ast.Number(current)
    elif current.eq(Kind.IDENTIFIER):
      return ast.Identifier(current)
    elif current.eq(Kind.OPEN_PARAN):
      expr = self.parse()
      self.buf.expect_legacy(Kind.CLOSE_PARAN)
      self.buf.next()
      return expr
    else:
      gen_error(current, "Failed to parse expression!")
    
    
    