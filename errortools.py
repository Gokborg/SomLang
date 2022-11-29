from token import Token
import sys

def gen_error(token: Token, msg: str):
    print("On line " + str(token.lineno) + ", ")
    print("\t" + token.line)
    print("\t" + (' ' * token.start) + "^")
    print("Error: " + msg + "\n")
    print("Purposefully raised exception below for debug")
    raise Exception
    sys.exit(1)

def gen_errormsg(msg: str):
  print(msg)
  print("Purposefully raised exception below for debug")
  raise Exception
  sys.exit(1)