# StockoBot! A python based discord bot designed for simplicity
### Features (Or potential features):
- Graphing and plotting of any historical stock price from 1970 to the present including a full MACD!
- Graphing and plotting of any historical volatility data from 1970
- Graphing and plotting of any appropriate ratio you would need from a stock! (Sharpe, M2, etc)
- Real-time stock tickers with accurate price data of a specific stock including: Open, Close, High, Low, and Volume with real-time updates from yahoo finance!
- Stock options chain for both call and put with a compehensive table for easy viewing
- Graphing and plotting of stock RSI, all 3 Bollinger Bands, and VWAP of a stock
- Update next (and most likely second-to last or last feature): Stock conintegration!

### How to use:

#### Commands:
For every command, the stocks that are supported are listed in ```TickerSymbols/symbols.txt```, ETF's are supported as well! Additionally, keep dates in ```Year/Month/Day``` for example: 2021/01/01, or ```Year/Month/Day-Hour:Min:Sec```, for example: 2021/01/01-11:13:04, the keyword ```Present``` (except for indicators) is also allowed if you want the exact date and time of today.
1. RealTime (rt): Provides a stock ticker of a specified stock based on Yahoo Finance API
2. Graph-Performance (gp): Show stock performance graph for any time point, including upto present
3. Graph-MACD (gm): Shows a stocks full MACD graph, similar to Graph-Performance
4. Graph-Ratio (gr): Shows a stocks ratio, meaning either its historical Sharpe, or Sortino ratio, (more to be added eventually)
5. Graph-Volatility (gv): Shows a stocks historical volatility up to the present time, implied volatility is an additional feature worth looking into
6. Options-Chain-Call (opc): Shows the options chain for a selected stock for call's in the form of a table rendered using matplotlib
7. Options-Chain-Put (opp): Shows the options chain for a selected stock for puts's in the form of a table rendered using matplotlib
8. Graph-Indicators (gi): Shows the RSI, all 3 Bollinger Bands, and VWAP of a selected stock and time range

##### Command Syntax:
- RealTime: to use the stock ticker, please type ```!stocko rt stock_ticker```, stock_ticker represents the stocks symbol from the NYSE: AAPL, MSFT, etc. I have provided a list all tickers to choose from in symbols.txt.
- Graph-Performance: to see performance charts, please type ```!stocko gp date_1 date_2 stock_ticker chart_type mav_set```.
As you can see, there are alot of things you can do, however, ```mav_set``` and ```chart_type``` have default values of "10" and "Line" respectively. Here are some options you can set for both:
1. Chart types: Line, Candle, OHLC, Renko, Point-Figure, typed exactly
2. Mav set: This provides the moving average line based on your graph, the setting is recommended to go from 2-20, with the smaller value looking closer to the presented graph
- Graph-MACD: To the see a stocks full MACD, please type ```!stocko gm date_1 date_2 stock_ticker```
- Graph-Volatility: To see a stocks historical volatility dependent on what you want, please type "!stocko gv *date_1* *date_2* *option* *chart_type* *stock_ticker*"
There are a few options for you to use:
1. Chart option: either Historical or Predict
2. Chart types: If you choose Historical, you can choose type either *Histogram*, or a historical *Line* graph. If you choose *Predict*, the only avaliable option is GARCH, to provide you with a GARCH model of your selected stock
- Graph-Ratio: To see a stocks' historical ratios, please type !stocko gr *date_1* *date_2* *option* *stock*, for chart option: Sharpe-Ratio or Sotino-Ratio
- Graph-Indicators: To see a stocks indicators, please type ```!stocko gi date_1 date_2 stock```
- To see the options chain for a stock, please type ```!stocko opc stock``` for call, and ```!stocko opp stock``` for put

Of course, you can always look back at the syntax by using ```!stocko help``` or ```!stocko help command_name``` for more specific help on the command you want to use. 

More commands and features to be added if I feel like it, some ideas include:

- Cointegration of StockoBot and StockoDash (Huge)
- Building an inhouse webscraper possibly with YFinance in order to webscrape data to ease reliance on API's for some features, not sure what though
- Literally working on anything else besides this lmao (i.e my SSG in OCaml that is not going so hot right now lol)