from token import Kind, Token

class Buffer:
  def set(self, line: str):
    self.current: str = line[0]
    self.pos: int = 0
    self.done: bool = False
    self.line: str = line

  def next(self) -> str:
    self.pos += 1
    if(self.pos < len(self.line)):
      self.current = self.line[self.pos]
    else:
      self.done = True
      self.current = '\0'
    return self.current

def lex(filename: str) -> [Token]:
  tokens: [Token] = []
  keywords = {
    "uint" : Kind.VAR_TYPE,
    "char" : Kind.VAR_TYPE,
    "if" : Kind.IF,
  }
  symbols = {
    '=' : Kind.EQUAL,
    ';' : Kind.SEMICOLON,
    '{' : Kind.OPEN_BRACE,
    '}' : Kind.CLOSE_BRACE,
    '>' : Kind.COND_G,
    '<' : Kind.COND_L,
    '+' : Kind.PLUS,
    '-' : Kind.MINUS,
    '(' : Kind.OPEN_PARAN,
    ')' : Kind.CLOSE_PARAN,
  }
  double_symbols = {
    "==" : Kind.COND_E,
    ">=" : Kind.COND_GE,
    "<=" : Kind.COND_LE,
  }
  
  with open(filename) as file:
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
            
            tokens.append(Token(symbol_kind, current, line, lineno, buf.pos))
          else:
            buf.next()
  
      lineno += 1
  return tokens
 
 