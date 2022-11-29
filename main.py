from lexer import lex
from parser import Parser
from codegen import CodeGeneration, Asm

print("                 LEXER")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
tokens = lex("test.som")
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


print("                 CODEGEN")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
codegen = CodeGeneration()
asm: Asm = codegen.gen(nodes)
print(asm)

