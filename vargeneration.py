import asts as ast
from typing import Union


class RegisterHandler:

  def __init__(self):
    #Im just giving 7 regs for now
    self.regs = [False] * 7

  def get_reg(self) -> int:
    for i, reg in enumerate(self.regs):
      if not reg:
        self.regs[i] = True
        return i + 1

    assert False

  def dealloc_reg(self, reg: int):
    self.regs[reg - 1] = False


class LiveRangeGeneration:

  def __init__(self):
    self.reghdlr: RegisterHandler = RegisterHandler()
    self.var_allocation: dict[int, dict[str, int]] = {}
    self.ranges: dict[str, list[int]] = {}
    self.total_reg_used: int = 0

  def get_reg(self, lineno: int, varname: str) -> int:
    #returns the register of a variable at that line number
    return self.var_allocation[lineno][varname]

  def gen_var(self, ast_nodes: "list[ast.Statement]"):
    for node in ast_nodes:
      if isinstance(node, ast.Declaration) or isinstance(node, ast.Assignment):
        self.gen_ranges(node)
      elif isinstance(node, ast.Block):
        self.gen_block_ranges(node)
      elif isinstance(node, ast.IfStatement):
        self.gen_if(node)
      elif isinstance(node, ast.WhileStatement):
        self.gen_while(node)

  def gen_while(self, node: ast.WhileStatement):
    self.gen_expr(node.condition)
    self.gen_block_ranges(node.block)

  def gen_if(self, node: ast.IfStatement):
    self.gen_expr(node.condition)
    self.gen_block_ranges(node.block)
    if isinstance(node.else_, ast.Block):
      self.gen_block_ranges(node.else_)
    elif isinstance(node.else_, ast.IfStatement):
      self.gen_if(node.else_)

  def gen(self, ast_nodes: "list[ast.Statement]"):
    self.gen_var(ast_nodes)
    #new_ranges = {}
    #for live_range, arr in self.ranges.items():
    #new_ranges[live_range] = [ arr[0], arr[len(arr)-1] ]
    ranges_new: "dict[str, list[int]]" = {}
    for live_range, arr in self.ranges.items():
      new_set: "list[int]" = []
      for i in range(arr[0], arr[len(arr) - 1] + 1):
        new_set.append(i)
      ranges_new[live_range] = new_set

    self.ranges = ranges_new
    l: "dict[int, list[str]]" = {}
    for live_range, arr in self.ranges.items():
      for lineno in arr:
        if lineno not in l:
          l[lineno] = [live_range]
        else:
          l[lineno].append(live_range)
    alloc: dict[int, dict[str, int]] = {}
    var_alloc: dict[str, int] = {}
    for lineno, vars in l.items():
      alloc[lineno] = {}
      tmp = var_alloc.copy()
      for key in tmp.keys():
        #Deallocates any regs not in the lineno
        if key not in alloc[lineno]:
          self.reghdlr.dealloc_reg(var_alloc[key])
          del var_alloc[key]

      for item in vars:
        if item not in var_alloc:
          reg = self.reghdlr.get_reg()
          if reg > self.total_reg_used:
            self.total_reg_used = reg
          alloc[lineno][item] = reg
          var_alloc[item] = reg
        else:
          alloc[lineno][item] = var_alloc[item]
    self.var_allocation = alloc

  def gen_block_ranges(self, block: ast.Block):
    self.gen_var(block.content)

  def gen_ranges(self, assign_or_dec_node: Union[ast.Assignment,
                                                 ast.Declaration]):
    self.gen_expr(assign_or_dec_node.identifier)
    if assign_or_dec_node.expr is not None:
      self.gen_expr(assign_or_dec_node.expr)

  def gen_expr(self, expr_node: ast.Expression):
    if isinstance(expr_node, ast.Number) or isinstance(expr_node,
                                                       ast.Identifier):
      if expr_node.token.value not in self.ranges:
        self.ranges[expr_node.token.value] = []
      self.ranges[expr_node.token.value].append(expr_node.token.lineno)
    elif isinstance(expr_node, ast.BinOp):
      self.gen_expr(expr_node.expr1)
      self.gen_expr(expr_node.expr2)

  def __str__(self):
    final_str: str = ""
    final_str += "Total Registers Needed: " + str(self.total_reg_used) + "\n"
    for key, value in self.var_allocation.items():
      final_str += "Line " + str(key) + ": \n"
      for var, reg in value.items():
        final_str += "\t " + var + "-> R" + str(reg) + "\n"
    return final_str
