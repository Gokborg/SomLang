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
      self.parse_expr_l2,
      [Kind.COND_G, Kind.COND_L]
    )
     
  def parse_expr_l2(self) -> ast.BinOp:
    return self.generic_parse_binop(
      self.parse_expr_l1,
      [Kind.PLUS, Kind.MINUS]
    )

  def parse_expr_l1(self) -> ast.Expression:
    current: Token = self.buf.current
    self.buf.next()
    if current.eq(Kind.NUMBER):
      return ast.Number(current)
    elif current.eq(Kind.IDENTIFIER):
      return ast.Identifier(current)
    else:
      gen_error(current, "Failed to parse expression!")
    
    
    