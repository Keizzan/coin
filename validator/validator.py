""""
##############################################################################
#######             PROJECT NAME : COIN VS USD                         #######
##############################################################################

                             Synopsis:
This file contains class Validator which has different dataframe validation rules
"""


### imports
import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import DateFormatValidation, CustomElementValidation


class Validator:

    def Schema_1(dataframe):
        """
    Parameters
    -----------
    dataframe {pandas dataframe object } : designated dataframe for validation
    
    Returns
    -----------
    dataframe, error:
    pandas dataframe objects
        """    

        ### Custom function for validation float
        def float_check(num):
            """
                Parameters
                -----------
                num : any
                
                Returns
                -----------
                Boolean
            """
            try:
                float(num)
            except ValueError:
                return False
            return True

        ### Define custom validators
        float_validation = [CustomElementValidation(lambda i: float_check(i),'is not a float number')]
        null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]


        ### Define schema template for validation columns
        schema = Schema([
            Column('High', null_validation+float_validation),
            Column('Low', null_validation+float_validation),
            Column('Date', null_validation + [DateFormatValidation('%Y-%m-%d %H:%M:%S')]),
            Column('Open', null_validation+float_validation),
            Column('Close', null_validation+float_validation),
            Column('Volume', null_validation+float_validation)
        ])
    
        ### Validation
        error_row = schema.validate(dataframe)
        ### Isolate and seperate errors
        errors_index_rows = [e.row for e in error_row]
        dataframe = dataframe.drop(index=errors_index_rows)
        error = pd.DataFrame({'Errors':error_row})
        
        ### Return two dataframes,
        ### validated dataframe and errors dataframe
        return dataframe, error

    def Schema_2(dataframe):
        """        
        Parameters
        -----------
        dataframe {pandas dataframe object } : designated dataframe for validation
        
        Returns
        -----------
        validated dataframe, error dataframe
        pandas dataframe objects
        """   
        ### Custom function for validation
        def float_check(num):
            """
            Parameters
            -----------
            num : any
            
            Returns
            -----------
            Boolean
            """
            try:
                float(num)
            except ValueError:
                return False
            return True

        ### Define custom validators
        float_validation = [CustomElementValidation(lambda i: float_check(i),'is not a float number')]
        null_validation = [CustomElementValidation(lambda a: a is not np.nan, 'cannot be empty')]


        ### Define schema template for validation columns
        schema = Schema([
            Column('High', null_validation+float_validation),
            Column('Low', null_validation+float_validation),
            # Column('Time', null_validation),
            Column('Open', null_validation+float_validation),
            Column('Close', null_validation+float_validation),
            Column('Volume', null_validation+float_validation)
        ])
    
        ### Validation
        error_row = schema.validate(dataframe)
        ### Isolate and seperate errors
        errors_index_rows = [e.row for e in error_row]
        dataframe = dataframe.drop(index=errors_index_rows)
        error = pd.DataFrame({'Errors':error_row})
        
        ### Return two dataframes,
        ### validated dataframe and errors dataframe
        return dataframe, error