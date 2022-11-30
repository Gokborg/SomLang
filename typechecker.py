import ast
from type import Type
from scope import Scopes, Scope, Variable

class TypeChecker():
  def __init__(self):
    self.types: "dict[,]" = {}
    self.scopes = Scopes()

  def push_scope(self,)
  
  def gen(self, ast_nodes: [ast.Statement]):
    #Creates ranges of which lines the variable exists in
    self.live_range.gen(ast_nodes)

    #Debug for var allocation
    print(self.live_range)
    print("")

    for node in ast_nodes:
        self.gen_statement(node)
    return self.asm

  def gen_ifstatement(self, ifStatement: ast.IfStatement):
    #reg: int = self.gen_condition(ifStatement.condition)
    #for stmt in ifStatement.block.content:
      #print(stmt)
    pass

  def gen_condition(self, condition: ast.Expression):
    reg1: int = self.gen_expr(condition.expr1)
    reg2: int = self.gen_expr(condition.expr2)
    self.asm.put_cmp(reg1, reg2)

  def gen_statement(self, statement: ast.Statement):
    if isinstance(statement, ast.Declaration):
      self.gen_declaration(statement)
    elif isinstance(statement, ast.Assignment):
      self.gen_assignment(statement)
    elif isinstance(node, ast.IfStatement):
        self.gen_ifstatement(node)

  def gen_assignment(self, assignment: ast.Assignment):
    varname: str = assignment.identifier.token.value
    dest_reg: int = self.live_range.get_reg(assignment.identifier.token.lineno,
                                            varname)
    self.gen_expr(assignment.expr, dest_reg)

  def gen_declaration(self, declaration: ast.Declaration):
    vartype: str = declaration.vartype.value
    varname: str = declaration.identifier.token.value
    self.scopes.put_var(varname, vartype)
    
    self.gen_expr(declaration.expr, dest_reg)

  #returns the register the expr is held in
  def gen_expr(self, expr: ast.Expression, reg: int = None) -> int:
    if isinstance(expr, ast.Number):
      if reg == None:
        reg = self.live_range.get_reg(expr.token.lineno, expr.token.value)
      self.asm.put_li(reg, expr.token.value)
      return reg
    elif isinstance(expr, ast.Identifier):
      return self.live_range.get_reg(expr.token.lineno, expr.token.value)
    elif isinstance(expr, ast.BinOp):
      reg1: int = self.gen_expr(expr.expr1)
      reg2: int = self.gen_expr(expr.expr2)
      dest_reg: int = reg
      if reg == None:
        dest_reg = reg1
      if expr.op.value == "+":
        self.asm.put_add(dest_reg, reg1, reg2)
      elif expr.op.value == "-":
        self.asm.put_sub(dest_reg, reg1, reg2)
      elif expr.op.value == "*":
        self.asm.put_mult(dest_reg, reg1, reg2)
      elif expr.op.value == "/":
        self.asm.put_div(dest_reg, reg1, reg2)
      return dest_reg
