import numpy as np
class GraphError(Exception):
    pass
class Graph():
    def __init__(self, x, y = []):
        self.x = np.asarray(x)
        if len(y) != len(x):
            raise GraphError("lists are not of same length")
        else:
            self.y = np.asarray(y)
    def getSubGraph(self, st, en):
        return Graph(self.x[st:en], self.y[st:en])
    
