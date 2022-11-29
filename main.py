from lexer import lex

tokens = lex("test.som")
for token in tokens:
  print(token)