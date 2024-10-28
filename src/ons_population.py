
from typing import Final, Dict, Type, Literal
import pandas as pd

from schemas import DataCatalogEntry
import constants as const


DEFAULT_AGE_BINS = 5
DEFAULT_TIME_PERIOD = 'daily'

class ONSPopulationScenario:

    def __init__(self, ons_catalog_entry: Type[DataCatalogEntry]):
        self.ons_catalog_entry = ons_catalog_entry
        self.ons_raw_df:pd.DataFrame = self.ons_catalog_entry.load()
        self.interpolated_df:pd.DataFrame = pd.DataFrame()
        self.yearly_age_bins = '5'
        self.time_period = 'daily'
        self.name = self.ons_catalog_entry.name
    
    def interpolated_population(self, 
                                time_period: Literal['daily','monthly','yearly'] = DEFAULT_TIME_PERIOD, 
                                yearly_age_bins:Literal[None,'5','10','Total'] = DEFAULT_AGE_BINS)->pd.DataFrame:
        """
        Interpolates the population data based on the specified time period and age bins.

        Args:
            time_period (Literal['daily','monthly','yearly'], optional): The time period for interpolation. Defaults to DEFAULT_TIME_PERIOD.
            yearly_age_bins (Literal[None,'5','10','Total'], optional): The age bins for interpolation. Defaults to DEFAULT_AGE_BINS.

        Returns:
            pandas.DataFrame: The interpolated population data.
        """
        

        if not self.interpolated_df.empty and self.time_period == time_period and self.yearly_age_bins == yearly_age_bins:
            # return cached df
            return self.interpolated_df.copy()
        self.yearly_age_bins = yearly_age_bins
        self.time_period = time_period
        df = self.ons_raw_df.copy()
        # create sub-icb column and drop na, drop
        df = df.assign(sub_icb = lambda df: df['AREA_NAME'].map(const.CCG_SUB_ICB)).dropna()
        if yearly_age_bins == 'Total' or yearly_age_bins is None:
            # Drop 'All ages' in AGE_GROUP
            df = df.loc[df['AGE_GROUP'] == 'All ages']
        else:
            df = df.loc[df['AGE_GROUP'] != 'All ages']
        # Create bins and labels for age groups
        if yearly_age_bins == '5' or yearly_age_bins == '10':
            if yearly_age_bins == '5':
                bins = [i for i in range(0,91,5)] + [150]
                labels = [f'{i}-{i+4}' for i in range(0,90,5)] + ['90+']
            elif yearly_age_bins == '10':
                bins = [i for i in range(0,91,10)] + [150]
                labels = [f'{i}-{i+9}' for i in range(0,90,10)] + ['90+']
        # Replace '90 and over' with 90 and convert to int
            df['AGE_GROUP'] = df['AGE_GROUP'].replace("90 and over", 90).astype(int)
            # Create age groups
            df['AGE_GROUP'] = pd.cut(df['AGE_GROUP'], bins, labels = labels,include_lowest = True, right = False)
        # unpivot table
        df = df.drop(columns={'AREA_CODE','COMPONENT','SEX','AREA_NAME'}).melt(id_vars=['AGE_GROUP','sub_icb'], var_name='year', value_name='population')
        # convert year to datetime
        df['year'] = df['year'].astype(int) 
        df['Date'] = pd.to_datetime(df['year'].astype(str) + '-01-01')
        # drop year column
        df = df.drop(columns={'year'})
        # convert population to int
        df['population'] = df['population'].astype(int)
        # group by age group, date and sub_icb
        df= df.groupby(['AGE_GROUP','Date','sub_icb']).sum(observed=True).reset_index()
        # interpolate
        df = self._interpolate_subpopulations(df, 'sub_icb', 'AGE_GROUP', time_period=time_period)
        self.interpolated_df = df.copy()
        return df

    @staticmethod
    def _interpolate_subpopulations(df_:pd.DataFrame, 
                                    cat_col_1:str ='sub_icb',
                                      cat_col_2:str='AGE_GROUP', 
                                      time_period: Literal['daily','monthly','yearly'] = 'daily')->pd.DataFrame:
        """Interpolates the population for a given sub_icb, age_group and date.

        Args:
            df_ (pd.DataFrame): input dataframe
            cat_col_1 (str): 1st categorical column
            cat_col_2 (str): 2nd categorical column

        Returns:
            pd.DataFrame: interpolated dataframe
        """

        aggregations ={
            'daily': 'D',
            'monthly': 'MS'}
        if time_period == 'yearly':
            return df_
       
        agg_period = aggregations.get(time_period, 'D')
        cat_col_1_vals = df_[cat_col_1].unique()
        cat_col_2_vals = df_[cat_col_2].unique()
        sub_dfs = []
        for cat1 in cat_col_1_vals:
            for cat2 in cat_col_2_vals:
                sub_df = df_.loc[(df_[cat_col_1] == cat1) & (df_[cat_col_2] == cat2)].set_index(['Date']).drop(columns=[cat_col_1, cat_col_2])
                sub_df = sub_df.resample(agg_period).interpolate(method='linear', fill_value=0.0).round(0).astype(int).reset_index()
                sub_df[cat_col_1] = cat1
                sub_df[cat_col_2] = cat2
        
                sub_dfs.append(sub_df)
        agg_df = pd.concat(sub_dfs)
        return agg_df