import calendar
from typing import Union
import numpy as np
import datetime as dt
import pandas as pd
from dataclasses import dataclass
import math
from functools import lru_cache
import joblib

from . import constants

def get_numdays(df_:pd.DataFrame):
    month_values = df_.index.get_level_values('APPOINTMENT_MONTH')
    years, months =  month_values.year, month_values.month

    def _num_days_in_month(year:int, month:int):
        # to be used by np.vectorize
        return calendar.monthrange(year, month)[1]

    num_days_in_month_v_ = np.vectorize(_num_days_in_month)

    return num_days_in_month_v_(years,months)

def is_working_day(day: Union[dt.date, pd.Timestamp]):
    """
    Check if a given day is a working day.

    Parameters:
    day (datetime.date or pandas.Timestamp): The day to check.

    Returns:
    bool: True if the day is a working day, False otherwise.
    """
    if day.isoweekday() < 6 and day not in constants.ENGLAND_BANK_HOLIDAYS:
        return True
    else:
        return False


def get_workingdays(a_:np.array):
    years, months =  a_.year, a_.month

    def _num_workingdays_in_month(year,month):
        workingdays = 0
        day = 1
        while day <= calendar.monthrange(year,month)[1]:
            the_date =  dt.datetime(year,month,day)
            if is_working_day(the_date):
                workingdays +=1
            day += 1
        return workingdays

    vec_workingdays = np.vectorize(_num_workingdays_in_month)
    return vec_workingdays(years, months)



def calc_oadr_status(ons_age_group:str):

    ons_age_group = ons_age_group.replace(" and over", "")
    try:
        ons_age = int(ons_age_group)
    except ValueError:
        return None
    if ons_age < 65 and ons_age >=20:
        return 'Working'
    elif ons_age >=65:
        return 'Retired'
    else:
        return None
    
# Function to perform sin/cos transformation
def sin_cos_transformer(X):
    angle = 2 * np.pi * X / 12
    sin_component = np.sin(angle)
    cos_component = np.cos(angle)
    return np.column_stack((sin_component, cos_component))


@dataclass
class PlotCounter:
    """simple object to count plots in each notebook run
    and conveniently make names"""
    name: str
    count: int = 1

    @property
    def plot_name(self):
        """Generates a unique plot name based on the current count"""
        current_count = self.count
        self.count += 1 # increment count
        return f"{constants.NOTEBOOK_OUTPUT_FIGURES_PATH}{self.name}_{current_count}"
    

@lru_cache(maxsize=12)
def _month_to_angle(month:int)->float:
    """
    Converts a month (1-12) to its corresponding angle in radians.

    Parameters:
    month (int): The month to convert.

    Returns:
    float: The angle in radians.

    Raises:
    ValueError: If the month is not in the range 1-12.
    """
    if month not in range(1,13):
        raise ValueError('month must be in range 1-12')
    return month*2*math.pi/12

@lru_cache(maxsize=12)
def month_num_to_sin(month:int)->float:
    """
    Converts a month number to its corresponding sine value.

    Args:
        month (int): The month number (1-12).

    Returns:
        float: The sine value of the month number.

    Raises:
        ValueError: If the month number is not in the range 1-12.
    """
    if month not in range(1,13):
        raise ValueError('month must be in range 1-12')
    return math.sin(_month_to_angle(month))

@lru_cache(maxsize=12)
def month_num_to_cos(month:int)->float:
    """
    Convert the month number to its corresponding cosine value.

    Parameters:
    month (int): The month number (1-12).

    Returns:
    float: The cosine value of the month number.
    """
    if month not in range(1,13):
        raise ValueError('month must be in range 1-12')
    return math.cos(_month_to_angle(month))


@dataclass
class ModelWrapper:
    def __init__(self, model_path):
        """
        Initializes the ModelWrapper and caches the model after loading it with Joblib.

        Args:
            model_path (str): Path to the pickled (joblib) scikit-learn model file.
        """
        self.model_path = model_path
        self.model = None  # Initialize model as None
        self._load_model()  # Load the model and cache it

    def _load_model(self):
        """
        Loads the model from a joblib file and caches it.

        Returns:
            object: The loaded scikit-learn model.
        """
        if self.model is None:  # Only load if not already cached
            self.model = joblib.load(self.model_path)
        return self.model

    def predict(self, X):
        """
        Predicts the output using the cached model.

        Args:
            X (array-like): Input data to be used for prediction.

        Returns:
            array-like: The predicted values from the model.
        """
        return self.model.predict(X)