from tokens import Kind, Token
import io


class Buffer:

  def set(self, line: str):
    self.current: str = line[0]
    self.pos: int = 0
    self.done: bool = False
    self.line: str = line

  def next(self) -> str:
    self.pos += 1
    if (self.pos < len(self.line)):
      self.current = self.line[self.pos]
    else:
      self.done = True
      self.current = '\0'
    return self.current


def lex(filename: str) -> "list[Token]":
  with open(filename) as file:
    return lex_file(file)


def lex_file(file: io.TextIOWrapper) -> "list[Token]":
  tokens: "list[Token]"= []
  keywords = {
    "uint": Kind.VAR_TYPE,
    "char": Kind.VAR_TYPE,
    "if": Kind.IF,
    "else": Kind.ELSE,
    "elif": Kind.ELIF,
    "while": Kind.WHILE,
    "macro": Kind.MACRO,
  }
  symbols = {
    '=': Kind.EQUAL,
    ';': Kind.SEMICOLON,
    '{': Kind.OPEN_BRACE,
    '}': Kind.CLOSE_BRACE,
    '>': Kind.COND_G,
    '<': Kind.COND_L,
    '+': Kind.PLUS,
    '-': Kind.MINUS,
    '*': Kind.MULT,
    '(': Kind.OPEN_PARAN,
    ')': Kind.CLOSE_PARAN,
    ',': Kind.COMMA,
    '/': Kind.DIV,
  }
  double_symbols = {
    "==": Kind.COND_E,
    ">=": Kind.COND_GE,
    "<=": Kind.COND_LE,
    "!=" : Kind.COND_NE,
    "//": Kind.COMMENT,
  }

  buf = Buffer()
  lineno = 1

  for line in file:
    buf.set(line)
    while not buf.done:
      #NUMBER TOKEN GENERATION
      if buf.current.isnumeric():
        start: int = buf.pos
        num: str = buf.current
        while buf.next().isnumeric():
          num += buf.current
        tokens.append(Token(Kind.NUMBER, num, line, lineno, start))

      #IDENTIFIER/KEYWORD TOKEN GENERATION
      elif buf.current.isalpha():
        start: int = buf.pos
        word: str = buf.current
        while buf.next().isalpha() or buf.current.isnumeric():
          word += buf.current
        kind: Kind = Kind.IDENTIFIER
        if word in keywords:
          kind = keywords[word]
        if buf.current == "!":
          buf.next()
          kind = Kind.MACROCALL
        
        tokens.append(Token(kind, word, line, lineno, start))

      else:
        if buf.current in symbols:
          current = buf.current
          symbol_kind: Kind = symbols[current]
          #Going to check for a double symbol here
          buf.next()
          double_symbol = buf.current + current
          if double_symbol in double_symbols:
            symbol_kind = double_symbols[double_symbol]
            current = double_symbol
            buf.next()

          if symbol_kind == Kind.COMMENT:
            buf.done = True
          else:
            tokens.append(Token(symbol_kind, current, line, lineno, buf.pos))
        else:
          buf.next()

    lineno += 1
  return tokens
