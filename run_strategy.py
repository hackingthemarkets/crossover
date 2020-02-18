import os, sys, argparse
import pandas as pd
import backtrader as bt
from backtrader import Cerebro
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold

cerebro = bt.Cerebro()

prices = pd.read_csv('data/spy_2000-2020.csv', index_col='Date', parse_dates=True)

# initialize the Cerebro engine
cerebro = Cerebro()
cerebro.broker.setcash(100000)

# add OHLC data feed
feed = bt.feeds.PandasData(dataname=prices)
cerebro.adddata(feed)

strategies = {
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold
}

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="Which strategy to run", type=str)
args = parser.parse_args()

if not args.strategy in strategies:
    print("Invalid strategy, must select one of {}".format(strategies.keys()))
    sys.exit()

cerebro.addstrategy(strategy=strategies[args.strategy])
cerebro.run()
cerebro.plot()