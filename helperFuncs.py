import numpy as np
import matplotlib.pyplot as plt
from dictionary import *
from sigmoidFuncs import *

class ArrayError(Exception):
    pass
def calcSlope(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    plt.plot(x, y)

    if x.ndim != y.ndim or x.ndim > 1 :
        raise ArrayError(f'Arrays Cannot be Multidimensional: {x.shape}, {y.shape}')
    else:
        polyline = np.linspace(1, x[-1], 5 * x[-1])
        model = np.poly1d(np.polyfit(x, y, 1))
        slope = model[1]
        return slope, model
    
def graphRecommendation(priceGraph: Graph, volGraph: Graph, timeBack: int):
    shortTerm, _= calcSlope(priceGraph.x[-timeBack:], priceGraph.y[-timeBack:])
    longTerm, _ = calcSlope(priceGraph.x, priceGraph.y)

    rating = (shortTerm-longTerm)/abs(longTerm)
    
    return np.tanh(ratingPrice) * np.tanh(ratingVol) #squeeze to between -1 and 1
def graphRecommendation_price(graph: Graph, timeBack: int):
    shortTerm, _= calcSlope(graph.x[-timeBack:], graph.y[-timeBack:])
    longTerm, _ = calcSlope(graph.x, graph.y)
    rating = (shortTerm - longTerm)/abs(longTerm)

    if(abs(rating) < 10 and abs(rating) > - 10):
        rating = 0
    
    return rating

    
    
    
"""
graph = alpacaAPI.getHistoricalData()
model1, degree = calcSlope(graph.x[-3:], graph.y[-3:])
model2, degree1 = calcSlope(graph.x, graph.y)
polyline = np.linspace(1, len(graph.x), 5*len(graph.x))
plt.plot(polyline, model1(polyline))
plt.plot(polyline, model2(polyline))
plt.show()
"""
