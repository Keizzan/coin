""""
##############################################################################
#######             PROJECT NAME : COIN VS USD                         #######
##############################################################################

                             Synopsis:
This file contains class DF_Manipulator which has different function to read specific csv files, 
and classes containing function to manipulate datetime format for desired results.
"""
import pandas as pd
from validator.validator import Validator


### Class containing functions for DateTime manipulation for crypto dataframes
class Time_manipulator_crypto:
    """
        Parameters:
        -----------
        dataframe { pandas dataframe object }

        returns:
        dataframe
    """    
    ### Grouby day
    def day(dataframe):

        dataframe.reset_index(drop=True, inplace=True)
        dataframe['Day'] = dataframe['Date'].dt.date
        dataframe.set_index('Day', inplace=True)
        return dataframe
    ### Groupby week
    def week(dataframe):
        dataframe.reset_index(drop=True, inplace=True)
        dataframe['Week'] = dataframe['Date'].dt.strftime('%Y-%U')
        dataframe = dataframe.groupby('Week').mean()
        return dataframe
    ### Groupby month
    def month(dataframe):
        dataframe.reset_index(drop=True, inplace=True)
        dataframe['Month'] = dataframe['Date'].dt.strftime('%Y-%m')
        dataframe = dataframe.groupby('Month').mean()
        return dataframe

### Class containing functions for DateTime manipulation for USD dataframes
class Time_manipulator_usd:
    """
        Parameters:
        -----------
        dataframe { pandas dataframe object }

        returns:
        dataframe
    """    
    ### Grouby day
    def day(dataframe):

        dataframe.reset_index(drop=False, inplace=True)
        dataframe['Day'] = dataframe['Time'].dt.date
        dataframe.set_index('Day', inplace=True)
        return dataframe
    ### Groupby week
    def week(dataframe):
        dataframe.reset_index(drop=False, inplace=True)
        dataframe['Week'] = dataframe['Time'].dt.strftime('%Y-%U')
        dataframe = dataframe.groupby('Week').mean()
        return dataframe
    ### Groupby month
    def month(dataframe):
        dataframe.reset_index(drop=False, inplace=True)
        dataframe['Month'] = dataframe['Time'].dt.strftime('%Y-%m')
        dataframe = dataframe.groupby('Month').mean()
        return dataframe


### Dataframe manipulator
class DF_Manipulator:
    ### Reads and outputs validated dataframe
    def crypto_data(dataframe):
        """
        Parameters:
        ------------
        dataframe { pandas dataframe object }

        return:
        --------
        validater_var, var_error
        pandas dataframe objects 
        """
        ### Read, isolate required columns and parse dates
        var = pd.read_csv(dataframe, parse_dates=['Date'],usecols=['Name', 'Date','High','Low', 'Open', 'Close', 'Volume'], index_col='Name')

        ### Run read dataframe through validator
        validated_var , var_error = Validator.Schema_1(var)

        ### Validated_var = Validated dataframe ready for plot
        ### Var_error = Dataframe containing invalid data rows
        return validated_var, var_error

    def usd_data(dataframe):
        """
        Parameters:
        ------------
        dataframe { pandas dataframe object }

        return:
        --------
        validater_var, var_error
        pandas dataframe objects 
        """
        ### Read, isolate required columns and parse dates
        var = pd.read_csv(dataframe, delimiter='\t', usecols=['High','Low', 'Open', 'Close', 'Volume', 'Time'], index_col='Time', parse_dates=['Time'])

        ### Run read dataframe through validator
        validated_var , var_error = Validator.Schema_2(var)

        ### Validated_var = Validated dataframe ready for plot
        ### Var_error = Dataframe containing invalid data rows
        return validated_var, var_error