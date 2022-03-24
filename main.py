import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import numpy as np
from dictionary import *
from helperFuncs import *
from time import ctime, time
from datetime import datetime, timedelta
from fakeportfolio import *

class AlpacaError(Exception):
    pass

key = ''
secret = ''
base_url = 'https://paper-api.alpaca.markets'

# instantiate REST API
api = tradeapi.REST(key, secret, base_url, api_version='v2')

def getHistoricalData(ticker: str, timeBack: int, startDate = "2021-03-01", endDate="2022-03-19", curr_day = 0):
    try:
        bars = api.get_bars(ticker, TimeFrame.Day, startDate, endDate, adjustment="raw")
    except:
        raise AlpacaError("Couldn't Get Data") #in case api is not working

    vwaps = []
    times2index = {}
    index2times = {}

    for i in range(len(bars)):
        time_str = bars[i].t.strftime('%Y-%m-%d') #taking time from alpaca and converting to datetime.datetime format
        time_date = datetime.strptime(time_str, '%Y-%m-%d')
        times2index[time_date] = i #times2index and index2times are dicts that help with creating subgraphs to simulate backtesting
        index2times[i] = time_date
        vwaps.append(bars[i].vw) #array of all volume weighted average prices of the stock
      
    indexes = np.arange(len(vwaps))
    priceGraph = Graph(indexes, vwaps)
    volGraph = Graph(indexes, volumes)
    return priceGraph, times2index, index2times


def backTest(startDate: str, endDate: str, ticker: str):

    start_date = datetime.strptime(startDate, '%Y-%m-%d') #end_date and start_date are for constricting graph for subgraph
    start_date = start_date - timedelta(days=365) #we need a one year's worth of data to run algo, so that reason for delta of -365
    

    myPort = FakePortfolio(1000000) #create a fake portfolio of 1m buying power.
    
    end_date = start_date + timedelta(days=365)
    start_str = start_date.strftime('%Y-%m-%d') #convert date with delta to string
    graph, times2index, index2times = getHistoricalData(ticker, 2, start_str, endDate)

    for i in range(graph.x[-1] - times2index[end_date]):
        #create the subgraph for backtesting. Without this we would be making a lot of api calls
        subgraph = graph.getSubGraph(times2index[start_date],times2index[end_date])
        if (i%30 == 0):
            print(start_date, ":", end_date) #print out progression
            
        recom = graphRecommendation_price(subgraph, 2) #algo for deciding buy/sell
        price = subgraph.y[-1] #"current" price of the stock during time of backtest
        #place fake order through fake portfolio
        if recom > 0:
            myPort.placeOrder(ticker, round(abs(recom)), 'buy', price)
        elif recom < 0:
            myPort.placeOrder(ticker, round(abs(recom)), 'sell', price)

        #add one to the day to create new subgraph
        start_date = index2times[times2index[start_date]+1]
        end_date = index2times[times2index[end_date]+1] 
    #print out all valuable info
    print (f'stocks at end: myPort.positions')
    print (f'cash at end: {myPort.bal}')
    print(f'price at end: {graph.y[-1]}')
    print(f'\n total assests: {(myPort.positions["TQQQ"] * graph.y[-1]) + myPort.bal}')    

#backTest('2019-03-30', '2021-01-12', 'TQQQ')
