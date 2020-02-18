import os, math
import sys
import pandas as pd
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 50),
              ('slow', 200),
              ('order_pct', 0.95),
              ('ticker', 'SPY'))

    def __init__(self):
        self.fastma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.p.fast, 
            plotname='50 day'
        )

        self.slowma = bt.indicators.SimpleMovingAverage(
            self.data.close, 
            period=self.p.slow, 
            plotname='200 day'
        )

        self.crossover = bt.indicators.CrossOver(
            self.fastma, 
            self.slowma
        )

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.p.order_pct * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.buy(size=self.size)
            
        if self.position.size > 0:
            if (self.crossover < 0):
                print("Sell {} shares of {} at {}".format(self.size, self.p.ticker, self.data.close[0]))
                self.close()