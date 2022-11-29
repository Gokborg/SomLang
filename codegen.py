#THIS CODE GENERATION IS VERY PRIMITIVE
#JUST TO GET A WORKING OUTPUT
#SUBJECT TO HEAVY CHANGE
#USE AS A TEMPLATE TO UNDERSTAND HOW TO GO THROUGH THE AST NODES 
#AND GENERATE ASSEMBLY
import ast

class Asm:
  def __init__(self):
    self.instrs: [str] = []
    
  def put_li(self, dest: int, value: int):
    self.instrs.append("LI R"+str(dest)+", "+str(value))

  def __str__(self):
    instrs_str: str = ""
    for instr in self.instrs:
      instrs_str += instr + "\n"
    return instrs_str

class RegisterHandler:
  def __init__(self):
    #Im just giving 7 regs for now
    self.regs = [False] * 7

  def get_reg(self) -> int:
    for i, reg in enumerate(self.regs):
      if not reg:
        self.regs[i] = True
        return i

class CodeGeneration:
  def __init__(self):
    self.asm: Asm = Asm()
    self.reghdlr: RegisterHandler = RegisterHandler()

  def gen(self, ast_nodes) -> Asm:
    for node in ast_nodes:
      if isinstance(node, ast.Declaration):
        self.gen_declaration(node)
    return self.asm

  def gen_declaration(self, declaration_node: ast.Declaration):
    varname: str = declaration_node.identifier.token.value
    register: int = self.gen_expr(declaration_node.expr)
    #Do some registering of the variable to that particular register

  def gen_expr(self, expr_node: ast.Expression):
    if isinstance(expr_node, ast.Number):
      self.asm.put_li(self.reghdlr.get_reg(), int(expr_node.token.value))
    
    