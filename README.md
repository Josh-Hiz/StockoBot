# StockoBot! A python based discord bot designed for simplicity
### Features (Or potential features):
- Graphing and plotting of any historical stock price from 1970 to the present including a full MACD!
- Graphing and plotting of any historical volatility data from 1970
- Graphing and plotting of any appropriate ratio you would need from a stock! (Sharpe, M2, etc)
- Real-time price data of a specific stock including: Open, Close, High, Low, and Volume with real-time updates!
- News API to quickly get links to any news outlit you want (IN DEVELOPMENT)
- Possibly trade stocks (IDEA/POTENTIAL THING TO LOOK INTO THE FUTURE)

As you can see its pretty light-weight for now, however more features are soon to come!

### How to use/install:

#### Commands:
So far there are only a few commands (mainly due to the amount of features each command supports):
1. RealTime: Provides a stock ticker of a specified stock based on Yahoo Finance API
2. Graph-Performance: Show stock performance graph for any time point, including upto present
3. Graph-MACD: Shows a stocks full MACD graph, similar to Graph-Performance
4. Graph-Ratio: Shows a stocks ratio, meaning either its historical Sharpe, or Sortino ratio, (more to be added eventually)
5. Graph-Volatility: Shows a stocks historical volatility up to the present time, implied volatility is an additional feature worth looking into

##### Command Syntax:
- RealTime: to use the stock ticker, please type "!stocko RealTime *stock_ticker*", stock_ticker represents the stocks symbol from the NYSE: AAPL, MSFT, etc. I have provided a list all tickers to choose from in symbols.txt.
- Graph-Performance: to see performance charts, please type !stocko Graph-Performance *date_1* *date_2* *stock_ticker* *chart_type* *mav_set*
As you can see, there are alot of things you would have to type to make it properly work, however, they are meant to provide users with full flexibility. Here are some options you can set for *chart_type* and *mav_set*:
1. Chart types: Line, Candle, OHLC, Renko, Point-Figure, typed exactly
2. Mav set: This provides the moving average line based on your graph, the setting is recommended to go from 2-20, with the smaller value being closer to the presented graph
- Graph-MACD: To the see a stocks full MACD, please type !stocko Graph-MACD *date_1* *date_2* *stock_ticker*
- Graph-Volatility: To see a stocks historical volatility dependent on what you want, please type "!stocko Graph-Volatility *date_1* *date_2* *option* *chart_type* *stock_ticker*"
There are a few options for you to use:
1. Chart option: either Historical or Predict
2. Chart types: If you choose Historical, you can choose type either *Histogram*, or a historical *Line* graph. If you choose *Predict*, the only avaliable option is GARCH, to provide you with a GARCH model of your selected stock
- Graph-Ratio: To see a stocks' historical ratios, please type !stocko Graph-Ratio *date_1* *date_2* *option* *stock*, for chart option: Sharpe-Ratio or Sotino-Ratio

Additional docs and or features to be added in the future