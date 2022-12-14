import os
import sys
from lexer import lex
from parser import Parser
from codegen import CodeGeneration, Asm

def compile(filename: str):
  print("                   LEXER")
  print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  tokens = lex(filename)
  for token in tokens:
    print(token)

  if len(tokens) == 0:
    print("The file contains no tokens")
    return

  print("")

  print("                 PARSER")
  print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  parser = Parser()
  nodes = parser.parse(tokens)
  for node in nodes:
    print(node)

  print("")

  #DISABLING CODE GEN FOR DEBUG
  print("                 CODEGEN")
  print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  codegen = CodeGeneration()
  asm: Asm = codegen.gen(nodes)
  print(asm)


# compile("tests/while.som")
#└── ├──
# compile("tests/while.som")
#compile("tests/test.som")
for filename in os.listdir("tests"):
  print(f"#### {filename}")
  try:
    compile(os.path.join("tests", filename))
  except Exception as e:
    print(e, file=sys.stderr)
"""
multi line stuff
"""
