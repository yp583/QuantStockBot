class FakePortfolio():
    def __init__(self, startBal):
        self.bal = startBal
        self.positions = {}
    def placeOrder(self, symbol:str, amount:int, side: str, price: float):
        if not symbol in self.positions:
            self.positions[symbol] = 0
        match side:
            case 'buy':
                if (self.bal > (amount * price)):
                    #print('bal', self.bal)
                    self.positions[symbol] += amount
                    self.bal -= amount * price
            case 'sell':
                if (self.positions[symbol] >= amount):
                    self.positions[symbol] -= amount
                    self.bal += amount * price
            case _:
                print('no side provided')
        
