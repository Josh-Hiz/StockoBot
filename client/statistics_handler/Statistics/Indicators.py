import yfinance as yf 
import pandas as pd
from pandas_datareader import data as pdr
import datetime
from datetime import datetime
import matplotlib.pyplot as plt

# Perform override to grab data easily
yf.pdr_override()

class IndicatorsTA:
    def __init__(self, tickerSymbol: str, startDate: str, endDate: str):
        self.tickerSymbol = tickerSymbol
        self.startDate = startDate
        self.endDate = endDate
        
        start_date = datetime.strptime(self.startDate, '%Y/%m/%d').date()
        end_date = datetime.strptime(self.endDate, '%Y/%m/%d').date()
        self.stockdf = pdr.get_data_yahoo(self.tickerSymbol, start_date, end_date)
        self.stockdf.index = self.stockdf.index.date
        
        self.algodf=self.getIndicators()
    
    def __getRSI(self, window: int = 14)->pd.DataFrame:
        delta = self.stockdf['Close'].diff()
        up = delta.clip(lower=0)
        down = -1*delta.clip(upper=0)
        
        ema_up = up.ewm(com=window-1, adjust=False).mean()
        ema_down = down.ewm(com=window-1, adjust=False).mean()
        
        rs = ema_up/ema_down
        rsi = 100 - (100/(1+rs))
        rsiTable = pd.DataFrame()
        rsiTable[f"RSI({window})"] = rsi
        return rsiTable
    
    def __getBBands(self,period: int =20, stdev: int = 2)->pd.DataFrame:
        # Calculate simple moving average:
        sma = self.stockdf['Close'].rolling(window = period).mean()
        lower_band = sma - stdev * 2
        higher_band = sma + stdev * 2
        bandTable = pd.DataFrame()
        bandTable[f'LBand({period},{stdev})'] = lower_band
        bandTable[f'MBand({period},{stdev})'] = sma
        bandTable[f'HBand({period},{stdev})'] = higher_band
        return bandTable
    
    def __getVWAP(self)->pd.DataFrame:
        df = self.stockdf
        v = df['Volume'].values
        tp = (df['Low'] + df['Close'] + df['High']).div(3).values
        vwapTable = self.stockdf.copy(deep=True)
        vwapTable=vwapTable.assign(vwap=(tp * v).cumsum() / v.cumsum())
        vwapTable=vwapTable.drop(['Open','High','Low','Close','Adj Close','Volume'],axis=1)
        return vwapTable
    
    def getIndicators(self)->pd.DataFrame:
        rsi = self.__getRSI()
        bbands = self.__getBBands()
        vwap = self.__getVWAP()
        indicators = pd.DataFrame()
        indicators = pd.concat([rsi,bbands,vwap],axis=1)
        indicators['Adj Close'] = self.stockdf['Adj Close']
        return indicators
    
    def plotIndicators(self):
        self.algodf.plot(kind="line",figsize=(25,10),title="Indicators")
        plt.savefig('output.png')