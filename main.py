import os
from lexer import lex
from parser import Parser
from codegen import CodeGeneration, Asm


def compile(filename: str):
  print("                   LEXER")
  print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
  tokens = lex(filename)
  for token in tokens:
    print(token)

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


# compile("tests/functions.som")
#└── ├──
compile("tests/while.som")
compile("tests/if.som")
#for filename in os.listdir("tests"):
#print(f"#### {filename}")
#compile(os.path.join("tests", filename))
"""
multi line stuff
"""
