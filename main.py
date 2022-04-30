""""
##############################################################################
#######             PROJECT NAME : COIN VS USD                         #######
##############################################################################

                             Synopsis:
This file contains classes which are implementing validation and manipulation and 
plot result with charts.
"""

### imports
from matplotlib import pyplot as plt
from manipulator import DF_Manipulator, Time_manipulator_crypto, Time_manipulator_usd
import pandas as pd


### Base class
class Plot:
    """
    Parameters:
    ------------
        nrows { int }: number of rows in figure containing axes   
        ncols { int }: number of colums in figure containing axes
        time { str }: day/week/month functions for manipulator class

    """
    def __init__(self, nrows, ncols, time) -> None: 
        ### Define variables
        self.time_title = time
        ### Define amount of axes
        self.nrow = nrows
        self.ncol = ncols

        ### Specify plot style
        plt.style.use('seaborn')
        fig, self.ax = plt.subplots(self.nrow, self.ncol, figsize=(35,15))

    def plot_show(self):
        plt.legend()
        plt.tight_layout()
        plt.show()

### Class containing currency dataframes
class Plot_currency(Plot):
    """
    Parameters:
    ------------
        nrows { int }: number of rows in figure containing axes   
        ncols { int }: number of colums in figure containing axes
        time { str }: day/week/month functions for manipulator class

    """
    def __init__(self, nrows, ncols, time) -> None:
        super().__init__(nrows, ncols, time)

        #Define which manipulator to use
        self.time_currency = eval(f'Time_manipulator_usd.{time}')

        self.euro, euro_error = DF_Manipulator.usd_data('archive/EURUSD_D1.csv')
        self.gold, gold_error = DF_Manipulator.usd_data('archive/XAUUSD_D1.csv')
        self.usd_error = pd.concat([euro_error ,gold_error])

### Class containing crypto dataframes
class Plot_crypto(Plot):
    """
    Parameters:
    ------------
        nrows { int }: number of rows in figure containing axes   
        ncols { int }: number of colums in figure containing axes
        time { str }: day/week/month functions for manipulator class

    """
    def __init__(self, nrows, ncols, time) -> None:
        super().__init__(nrows, ncols, time)

        #Define which manipulator to use
        self.time_crypto = eval(f'Time_manipulator_crypto.{time}')
  
        ### Define Dataframes for each coin
        self.bitcoin, bitcoin_error = DF_Manipulator.crypto_data('archive/coin_Bitcoin.csv')
        self.binancecoin, binancecoin_error = DF_Manipulator.crypto_data('archive/coin_BinanceCoin.csv')
        self.cardano, cardano_error = DF_Manipulator.crypto_data('archive/coin_Cardano.csv')
        self.ethereum, ethereum_error = DF_Manipulator.crypto_data('archive/coin_Ethereum.csv')
        self.solana, solana_error = DF_Manipulator.crypto_data('archive/coin_Solana.csv')
        self.xrp, xrp_error = DF_Manipulator.crypto_data('archive/coin_XRP.csv')
        self.crypto_error = pd.concat([bitcoin_error, binancecoin_error, cardano_error, ethereum_error, solana_error, xrp_error])


### Class containing functions with one plot
class Single(Plot_crypto, Plot_currency):
    def __init__(self, time) -> None:
        """
        Parameters:
        ------------
            time { str }: day/week/month functions for manipulator class
        """
        super().__init__(1, 1, time)
        ## Define dataframes and manipulate datetime 
        self._bitcoin = self.time_crypto(self.bitcoin)
        self._binancecoin = self.time_crypto(self.binancecoin)
        self._cardano = self.time_crypto(self.cardano)
        self._ethereum = self.time_crypto(self.ethereum)
        self._solana = self.time_crypto(self.solana)
        self._xrp = self.time_crypto(self.xrp)
        self._euro = self.time_currency(self.euro)
        self._gold = self.time_currency(self.gold)

    ### Plot for High/Low/Open/Close for all crypto over time
    def all_coin(self, var1):
        """
        Parameters:
        ------------
            var1 { str }: column name to use on y axis in plot

        """
        ax = self.ax
        column = f'{var1.capitalize()}'
        ### Define plots
        ax.plot(self._bitcoin.index, self._bitcoin[column], label='Bitcoin')
        ax.plot(self._binancecoin.index, self._binancecoin[column], label='Binance Coin')
        ax.plot(self._cardano.index, self._cardano[column], label='Cardano')
        ax.plot(self._ethereum.index, self._ethereum[column], label='Ethereum')
        ax.plot(self._solana.index, self._solana[column], label='Solana')
        ax.plot(self._xrp.index, self._xrp[column], label='XRP')
        ax.set_yscale('log')
        ax.set_ylabel(f'{column} values')
        ax.set_title(f'{column} By {self.time_title.capitalize()}')    
        ax.tick_params(axis='x', labelrotation=90)
        self.plot_show()

    ### Plot to compare High/Low/Open/Close values in USD of bitcoin/gold/euro
    def bitcoin_euro_gold(self, var1):
        """
        Parameters:
        ------------
            var1 { str }: column name to use on y axis in plot
        """
        ax = self.ax
        column = f'{var1.capitalize()}'
        ax.plot(self._bitcoin.index, self._bitcoin[column], label='Bitcoin', color='yellow')
        ax.set_yscale('log')
        ax.set_title(f'{var1.capitalize()} Values by {self.time_title.capitalize()}')
        ax.set_ylabel('Value in USD')
        ax.legend(loc='upper left')
        ax1 = ax.twinx()
        ax1.plot(self._euro.index, self._euro[column], label='Euro')
        ax1.plot(self._gold.index, self._gold[column], label='Gold')
        ax1.set_ylabel('Value in USD')
        ax1.set_yscale('log')
       
        self.plot_show()



 ### Class containing functions with double plots
class Double(Plot_crypto, Plot_currency):
    def __init__(self, time) -> None:
        """
        Parameters:
        -----------
            time { str }: day/week/month functions from manipulator class
        """
        super().__init__(1, 2, time)

        ### Function to plot High/Low and Open/Close comparison
    def coin(self, var1):
        """
        Parameters:
        ------------
            var1 { str }: coin name to use on y axis in plot
        """
        ### Define variables
        df = self.time(eval(f'self.{var1}'))
        ax1 = self.ax[0]
        ax2 = self.ax[1]
        ax1.plot(df.index, df['High'], label='High')
        ax1.plot(df.index, df['Low'], label='Low')
        ax1.set_yscale('log')
        ax1.legend()
        ax1.set_ylabel(f'{var1.capitalize()} High/Low Value')
        ax1.set_title(f'{var1.capitalize()} value by {self.time_title}')
        ax1.tick_params(axis='x', labelrotation=90)
        ax2.plot(df.index, df['Open'], label='Open')
        ax2.plot(df.index, df['Close'], label='Close')
        ax2.set_yscale('log')
        ax2.set_ylabel(f'{var1.capitalize()} Value')
        ax2.set_title(f'{var1.capitalize()} Open/Close values by {self.time_title}')
        ax2.tick_params(axis='x', labelrotation=90)
        self.plot_show()

        ### Function for to plot difference between Open-Close and High-Low
    def diff_coin(self, var1):
        """
        Parameters:
        ------------
            var1 { str }: crypto DF to use in plot
        """
        ### Define variables
        df = self.time(eval(f'self.{var1}'))
        ax1 = self.ax[0]
        ax2 = self.ax[1]
        ax1.plot(df.index, df['High'] - df['Low'], label='Difference High vs Low')
        ax1.plot(df.index, df['Open'] - df['Close'], label='Difference Open vs Close')
        ax1.legend()
        ax1.set_yscale('log')
        ax1.set_ylabel(f'{var1.capitalize()} Difference Value')
        ax1.set_title(f'{var1.capitalize()} value by {self.time_title}')
        ax1.tick_params(axis='x', labelrotation=90)
        ax2.plot(df.index, df['Volume'], label='Volume')
        ax2.set_yscale('log')
        ax2.set_ylabel(f'{var1.capitalize()} Volume value')
        ax2.set_title(f'{var1.capitalize()} Volume values by {self.time_title}')
        ax2.tick_params(axis='x', labelrotation=90)
        self.plot_show()