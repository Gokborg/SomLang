from abc import ABC, abstractmethod

class AstWalker(ABC):
  def walk(self, nodes: [ast.Statement]):
    ...