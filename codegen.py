#THIS CODE GENERATION IS VERY PRIMITIVE
#JUST TO GET A WORKING OUTPUT
#SUBJECT TO HEAVY CHANGE
#USE AS A TEMPLATE TO UNDERSTAND HOW TO GO THROUGH THE AST NODES
#AND GENERATE ASSEMBLY
from typing import Optional

import asts as ast
from vargeneration import LiveRangeGeneration
from errortools import gen_error, gen_errormsg


class Asm:

  def __init__(self):
    self.instrs: "list[str]" = []

  def put_li(self, dest: int, value: int):
    self.instrs.append("IMM R" + str(dest) + " " + str(value))

  def put_add(self, dest: int, srcA: int, srcB: int):
    self.instrs.append("ADD R" + str(dest) + " R" + str(srcA) + " R" +
                       str(srcB))

  def put_sub(self, dest: int, srcA: int, srcB: int):
    self.instrs.append("SUB R" + str(dest) + " R" + str(srcA) + " R" +
                       str(srcB))

  def put_mult(self, dest: int, srcA: int, srcB: int):
    self.instrs.append("MLT R" + str(dest) + " R" + str(srcA) + " R" +
                       str(srcB))
  def put_div(self, dest: int, srcA: int, srcB: int):
    self.instrs.append("DIV R" + str(dest) + " R" + str(srcA) + " R" +
                       str(srcB))
  def put_gt(self, dest: int, srcA: int, srcB: int):
    self.instrs.append("SETG R" + str(dest) + " R" + str(srcA) + " R" +
                       str(srcB))
  def put_cmp(self, srcA: int, srcB: int):
    self.instrs.append("CMP R" + str(srcA) + " R" + str(srcB))

  def put_branch(self, inst: str, label: str, left: int, right: int):
    self.instrs.append(f"{inst} {label} R{left} R{right}")

  def put_jmp(self, label: str):
    self.instrs.append("JMP " + label)
    
  def put_label(self, label: str):
    self.instrs.append(label)
    
  def __str__(self):
    instrs_str: str = ""
    for instr in self.instrs:
      instrs_str += instr + "\n"
    return instrs_str


class CodeGeneration:

  def __init__(self):
    self.asm: Asm = Asm()
    self.live_range: LiveRangeGeneration = LiveRangeGeneration()
    self.label = 0

  def gen(self, ast_nodes: "list[ast.Statement]") -> Asm:
    #Creates ranges of which lines the variable exists in
    self.live_range.gen(ast_nodes)

    #Debug for var allocation
    print(self.live_range)
    print("")

    for node in ast_nodes:
      self.gen_statement(node)
    return self.asm

  def gen_statement(self, statement: ast.Statement):
    if isinstance(statement, ast.Declaration):
      self.gen_declaration(statement)
    elif isinstance(statement, ast.Assignment):
      self.gen_assignment(statement)
    elif isinstance(statement, ast.IfStatement):
      self.gen_ifstatement(statement, None, None)
    elif isinstance(statement, ast.WhileStatement):
      self.gen_whilestatement(statement)
    else:
      gen_errormsg("sad")

  def gen_whilestatement(self, whileStatement: ast.WhileStatement):
    end_label: str = self.gen_label()
    start_label: str = self.gen_label()
    self.asm.put_label(start_label)
    self.gen_condition(whileStatement.condition, end_label)
    self.gen_block(whileStatement.block)
    self.asm.put_jmp(start_label)
    self.asm.put_label(end_label)

  def gen_label(self) -> str:
    self.label += 1
    return ".IF_" + str(self.label)

  def gen_ifstatement(self, ifStatement: ast.IfStatement, label: Optional[str], end_label: Optional[str]):
    if label == None:
      label = self.gen_label()
    if end_label == None and ifStatement.else_ != None:
      end_label = self.gen_label()
    self.gen_condition(ifStatement.condition, label)
    self.gen_block(ifStatement.block)
    if end_label != None:
      self.asm.put_jmp(end_label)
    self.asm.put_label(label)
      
    if isinstance(ifStatement.else_, ast.Block):
      for statement in ifStatement.else_.content:
        self.gen_statement(statement)
      assert end_label is not None
      self.asm.put_label(end_label)
    elif isinstance(ifStatement.else_, ast.IfStatement):
      self.gen_ifstatement(ifStatement.else_, None, end_label)
    
  
  def gen_condition(self, condition: ast.Expression, end_block_label: str):
    assert isinstance(condition, ast.BinOp)
    reg1: int = self.gen_expr(condition.expr1)
    reg2: int = self.gen_expr(condition.expr2)
    op = condition.op.value
    if op == ">":
      self.asm.put_branch("BLE", end_block_label, reg1, reg2)
    elif op == ">=":
      self.asm.put_branch("BRL", end_block_label, reg1, reg2)
    elif op == "<":
      self.asm.put_branch("BGE", end_block_label, reg1, reg2)
    elif op == "<=":
      self.asm.put_branch("BRG", end_block_label, reg1, reg2)
    elif op == "==":
      self.asm.put_branch("BNE", end_block_label, reg1, reg2)
    elif op == "!=":
      self.asm.put_branch("BRE", end_block_label, reg1, reg2)
    else:
      gen_error(condition.op, "Unknown condition operator used!")
                

  def gen_block(self, block: ast.Block):
    for statement in block.content:
      self.gen_statement(statement)

  def gen_assignment(self, assignment: ast.Assignment):
    varname: str = assignment.identifier.token.value
    dest_reg: int = self.live_range.get_reg(assignment.identifier.token.lineno,
                                            varname)
    self.gen_expr(assignment.expr, dest_reg)

  def gen_declaration(self, declaration: ast.Declaration):
    vartype: str = declaration.vartype.value
    varname: str = declaration.identifier.token.value
    dest_reg: int = self.live_range.get_reg(
      declaration.identifier.token.lineno, varname)
    if declaration.expr is not None:
      self.gen_expr(declaration.expr, dest_reg)

  #returns the register the expr is held in
  def gen_expr(self, expr: ast.Expression, reg: Optional[int] = None) -> int:
    if isinstance(expr, ast.Number):
      if reg == None:
        reg = self.live_range.get_reg(expr.token.lineno, expr.token.value)
      self.asm.put_li(reg, int(expr.token.value))
      return reg
    elif isinstance(expr, ast.Identifier):
      return self.live_range.get_reg(expr.token.lineno, expr.token.value)
    elif isinstance(expr, ast.BinOp):
      reg1: int = self.gen_expr(expr.expr1)
      reg2: int = self.gen_expr(expr.expr2)
      dest_reg: int = reg if reg is not None else reg1
      if expr.op.value == "+":
        self.asm.put_add(dest_reg, reg1, reg2)
      elif expr.op.value == "-":
        self.asm.put_sub(dest_reg, reg1, reg2)
      elif expr.op.value == "*":
        self.asm.put_mult(dest_reg, reg1, reg2)
      elif expr.op.value == "/":
        self.asm.put_div(dest_reg, reg1, reg2)
      return dest_reg
    else:
      assert False
