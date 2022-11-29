from token import Kind, Token, Pos

class Buffer:
  def set(self, line: str):
    self.current: str = line[0]
    self.pos: int = 0
    self.done: bool = False
    self.line: str = line

  def next(self):
    self.pos += 1
    
    if(self.pos < len(self.line)):
      self.current = self.line[self.pos]
    else:
      self.done = True
      self.current = '\0'

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
          while buf.current.isnumeric():
            buf.next()
          num: str = buf.line[start:buf.pos]
          tokens.append(
            Token(Kind.NUMBER, num, 
                  Pos(line, lineno, start, buf.pos))
          )

        elif buf.current.isalpha():
          start: int = buf.pos
          while buf.current.isalpha() or buf.current.isnumeric():
            buf.next()
          word: str = buf.line[start:buf.pos]
          tokens.append(
            Token(Kind.IDENTIFIER, word, 
                  Pos(line, lineno, start, buf.pos))
          )
        
        elif buf.current == '=':
          tokens.append(
            Token(Kind.EQUAL, buf.current,
                 Pos(line, lineno, buf.pos, buf.pos))
          )
        else:
          buf.next()
  
      lineno += 1
  return tokens
 
 