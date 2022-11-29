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
  
  with open(filename) as file:
    buf = Buffer()
    lineno = 1
    
    for line in file:
      buf.set(line)
      while not buf.done:
        if buf.current.isnumeric():
          start: int = buf.pos
          num: str = buf.current
          while buf.next().isnumeric():
            num += buf.current
          tokens.append(Token(Kind.NUMBER, num, lineno, start))

        elif buf.current.isalpha():
          start: int = buf.pos
          word: str = buf.current
          while buf.next().isalpha() or buf.current.isnumeric():
            word += buf.current
          tokens.append(Token(Kind.IDENTIFIER, word, lineno, start))
        
        elif buf.current == '=':
          tokens.append(Token(Kind.EQUAL, buf.current, lineno, buf.pos))
          
        else:
          buf.next()
  
      lineno += 1
  return tokens
 
 