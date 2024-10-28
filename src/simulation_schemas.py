import datetime as dt
from typing import Dict, List, Literal, Union, Type, Any
from abc import ABC
import yaml
import random
import pandas as pd
import scipy.stats as stats

from pydantic import (
    BaseModel,
    Field,
    RootModel,
    model_validator
    )


# this is used to define the arguments for the pydantic Field class
# so that probability of non attendance is between 0 and 1
PROPENSITY_FIELD_ARGS = {
    "default": 0.0,
    "ge": 0.0,
    "le": 1.0,
}

# this is used to confirm that the weights of a propensity sum to 1.0
PROPENSITY_ACCURACY_THRESHOLD = 0.002


class YamlLoader(ABC):
    """Base class to define the methods that the yaml loader must implement"""

    @classmethod
    def read_yaml(cls, file_path: str):
        """
        Reads a YAML file and returns an instance of the class.

        Args:
            cls (type): The class to instantiate.
            file_path (str): The path to the YAML file.

        Returns:
            object: An instance of the class with attributes populated from the YAML file.
        """
        with open(file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            class_instance = cls(**yaml_data)
            return class_instance

    
class BaseChoice(BaseModel, ABC):
    """
    Base class for propensity choices, not to be used directly.
    The fields are the choices and the values are the probabilities.
    """

    def pick(self, n_choices: int = 1) -> Union[Any, List[Any]]:
        """
        Randomly selects one of the fields based on their probabilities (values must be float).

        Returns:
            str: The selected staff field name.
        """
        # get the probabilities as a dictionary
        probabilities_dict: Dict[str, float] = self.model_dump(by_alias=True)
        # randomly select a staff type based on the probabilities using the random module
        field_choices = random.choices(
            list(probabilities_dict.keys()),
            weights=list(probabilities_dict.values()),
            k=n_choices,
        )
        if n_choices == 1:
            return field_choices[0]
        else:
            return
        
    class Config:
        case_sensitive = False


# Define a custom exception class for better error handling
class PropensityError(Exception):
    pass


class SumTo1Choice(BaseChoice, ABC):
    """
    Base class for propensity choices, not to be used directly.
    The fields are the choices and the values are the probabilities.
    The sum of the field values must be 1.0.
    """
        
    @model_validator(mode='after')
    def validate_sum_to_one(self):
        """Ensure the sum of all propensities for staff types is approximately 1."""
        # Sum the values for the keys present in your YAML data
        

        propensity_sum =sum(self.model_dump().values())
        # Use the custom exception for raising errors
        lower_threshold = 1 - PROPENSITY_ACCURACY_THRESHOLD
        upper_threshold = 1 + PROPENSITY_ACCURACY_THRESHOLD
        if not (lower_threshold <= propensity_sum <= upper_threshold):
            raise PropensityError(f"The sum of delivery propensities must be close to 1 (within tolerance\
                {PROPENSITY_ACCURACY_THRESHOLD}). Got {propensity_sum:.6f} instead.")
        
        return self



class AreaModel(ABC):
    @property
    def areas(self) -> List[str]:
        """returns the list of areas"""
        return list(self.model_dump().keys())

    def get_area(self, area: str) -> Type[BaseModel]:
        """
        Get the propensity for a given area.

        Args:
            area (str): The area to get the details for.

        Returns:
            Dict[str, float]: The propensity for the given area.
        """
        return self.root.get(area)


class PopulationBaseline(BaseModel):
    """Class to represent the population baseline"""
    pass


class PopulationByYear(RootModel[Dict[int, int]]):
    @property
    def years(self) -> List[int]:
        """returns the list of years"""
        return list(self.model_dump.keys())

    def get_year(self, year: int):
        return self.root.get(year)


class PopulationByAgeGroup(RootModel[Dict[str, PopulationByYear]]):
    @property
    def age_groups(self) -> List[str]:
        """returns the list of age_groups"""
        return list(self.model_dump().keys())

    def get_age_group(self, age_group: str) -> PopulationByYear:
        return self.root.get(age_group)


class PopulationByArea(RootModel[Dict[str, PopulationByAgeGroup]], AreaModel):
    """Class to load and validate the population estimates by area"""

    def as_dataframe(
        self, proportions: bool = False, monthly: bool = False
    ) -> pd.DataFrame:
        """returns the population by area as a pandas dataframe"""
        # convert to dict
        df_ = pd.DataFrame.from_dict(self.model_dump(by_alias=True)).T

        # mangle the dataframe, empty list to hold rows
        mangled_rows = []
        # iterate over the rows
        for i, row in df_.iterrows():
            # iterate over the columns (age bands)
            for col in df_.columns:
                # each entry is a dictionary with the year as key and the population as value
                for k, v in row[col].items():
                    # append the row to the list
                    mangled_rows.append([col, i, k, v])
        pivot_df = pd.DataFrame(
            mangled_rows, columns=["age_band", "area", "year", "population"]
        ).pivot(index=["year", "area"], columns="age_band", values="population")

        if monthly:
            # add a month column to index
            expanded_index_df: pd.DataFrame = pd.DataFrame(
                index=pd.date_range(
                    dt.date(
                        pivot_df.index.get_level_values("year").min(), month=1, day=1
                    ),  # jan 1st of the first year
                    dt.date(
                        pivot_df.index.get_level_values("year").max(), month=12, day=1
                    ),  # dec 1st of the last year
                    freq="M",
                )  # month frequency
            ).assign(
                month=lambda df: df.index.month, year=lambda df: df.index.year
            )  # add month and year columns

            # add areas
            monthly_areas_df: pd.DataFrame = pd.concat(
                [
                    expanded_index_df.assign(area=area)
                    for area in df_.index.get_level_values("area").unique()
                ]
            ).set_index(["area", "year", "month"])
            del expanded_index_df  # free up memory
            # merge the two dataframes and interpolate the missing values
            monthly_population_df = monthly_areas_df.join(
                df_, how="outer"
            ).interpolate()

            if not proportions:
                return monthly_population_df
            else:
                return monthly_population_df.div(
                    monthly_population_df.sum(axis=1), axis=0
                )

        else:
            if not proportions:
                return pivot_df
            else:
                return pivot_df.div(pivot_df.sum(axis=1), axis=0)


class PopulationScenarios(RootModel[Dict[str, PopulationByArea]], YamlLoader):
    """Class to load and validate the population scenarios yaml file for a yaml file of areas"""

    @property
    def scenarios(self) -> List[str]:
        """returns the list of scenarios"""
        return list(self.model_dump().keys())

    def get_scenario(self, scenario: str) -> PopulationByArea:
        """returns the population by area for a given scenario"""
        return self.root.get(scenario)


class PopulationBaseLinesByArea(RootModel[Dict[str, PopulationBaseline]], AreaModel, YamlLoader):
    """Class to load and validate the population estimates yaml file for a yaml file of areas"""

    pass


class PopulationGrowthFactors(BaseModel):
    """Class to represent the population growth factors"""

    pass


class PopulationGrowthFactorsByArea(RootModel[Dict[str, PopulationGrowthFactors]]):
    """Class to represent the population growth factors by area"""

    pass


class PopulationGrowthFactorScenarios(RootModel[Dict[str, PopulationGrowthFactorsByArea]], YamlLoader):
    """Class to load and validate the population growth factor scenarios yaml file for a yaml file of areas"""

    pass


class AppointmentTimeDistributions(BaseModel):
    """Class to represent the appointment time distributions"""
    lognorm: List[float] = Field(..., max_length=3, min_length=3)
    expon: List[float] = Field(..., max_length=2, min_length=2)

    def get_time(self, distribution:Literal['lognorm','expon']='lognorm') -> float:
        """samples the chosen distribution"""
        if distribution =='lognorm':
            return stats.lognorm.rvs(*self.lognorm, size=1)[0]
        elif distribution =='expon':
            return stats.expon.rvs(*self.expon, size=1)[0]
        else:
            raise ValueError(f"Unknown distribution {distribution}, must be one of 'lognorm' or 'expon'")   
    

class AreaAppointmentTimeDistributions(RootModel[Dict[str, AppointmentTimeDistributions]], YamlLoader, AreaModel):
    """Class to load and validate the appointment time distributions yaml file,
    fields can have any name"""


class StaffDidNotAttendRatesByDelivery(BaseChoice):
    """
    Class to represent the did not attend rates for a given staff type
    """

    face_to_face: float = Field(alias="Face-to-Face", **PROPENSITY_FIELD_ARGS)
    home_visit: float = Field(alias="Home Visit", **PROPENSITY_FIELD_ARGS)
    telephone: float = Field(alias="Telephone", **PROPENSITY_FIELD_ARGS)
    unknown: float = Field(alias="Unknown", **PROPENSITY_FIELD_ARGS)
    video_online: float = Field(alias="Video/Online", **PROPENSITY_FIELD_ARGS)
    
    def did_patient_attend(self, appointment_mode:str)->bool:
        # randomly choose a number between 0 and 1
        random_num = random.random()
        # get the propensity for the given appointment mode
        propensity = getattr(self, appointment_mode.lower().replace(" ", "_").replace("/","_").replace("-","_"))
        # return True if the random number is greater than the propensity to NOT attend
        return random_num > propensity


class DidNotAttendRates(BaseModel):
    """
    Class to represent the did not attend rates for a given area.
    The fields are the staff types and the values
    """

    gp: StaffDidNotAttendRatesByDelivery = Field(..., alias="GP", default_factory=dict)
    other_practice_staff: StaffDidNotAttendRatesByDelivery = Field(
        ..., alias="Other Practice staff", default_factory=dict
    )
    unknown: StaffDidNotAttendRatesByDelivery = Field(
        ..., alias="Unknown", default_factory=dict
    )
    def _get_staff_type(self, staff_type:str)->StaffDidNotAttendRatesByDelivery:
        return getattr(self, staff_type.lower().replace(" ", "_"))
    


class DidNotAttendRatesByArea(RootModel[Dict[str, DidNotAttendRates]], YamlLoader, AreaModel):
    """Class to load and validate the did not attend rates yaml file for a yaml file of areas"""   
    def did_patient_attend(self, area:str, staff_type:str, appointment_mode:str)->bool:
        
        #
        area_rates:DidNotAttendRates = self.get_area(area)
        
        # get the nested class
        staff_rates:StaffDidNotAttendRatesByDelivery = area_rates._get_staff_type(staff_type)
        
        # run the did_patient_attend method of the StaffDidNotAttendRatesByDelivery class
        return staff_rates.did_patient_attend(appointment_mode)

class AppointmentStaffChoice(SumTo1Choice):
    """
    Class to represent the propensity of a given staff type for appointments
    """

    gp: float = Field(alias="GP", **PROPENSITY_FIELD_ARGS)
    other_practice_staff: float = Field(alias="Other Practice staff", **PROPENSITY_FIELD_ARGS)
    unknown: float = Field(alias="Unknown", **PROPENSITY_FIELD_ARGS)
    
    def pick(self)->str:
        """Selects an item using the superclass's pick method. If the selected item is 'Unknown',
        it recursively calls itself until a valid item is selected. 
        This will automatically balance the probabilities of the other items, over enough iterations.

      

        Returns
        -------
        str
            The selected item, guaranteed not to be 'Unknown'.
        """
        # make an original choice
        choice_ = super().pick()
        # if the choice is unknown, recursively call the pick method
        if choice_ == 'Unknown':
            return self.pick()
        else:
            # if the choice is not unknown, return it
            return choice_
    

class StaffPropensityByArea(RootModel[Dict[str, AppointmentStaffChoice]], YamlLoader, AreaModel):
    """Class to load and validate the staff type propensity yaml file for a yaml file of areas"""

    def pick_staff_type(self, area: str) -> str:
        # randomly choose a staff type depending on the area
        area_model:AppointmentStaffChoice = self.get_area(area)

        return area_model.pick()


class AppointmentDeliveryChoice(SumTo1Choice):
    """
    Class to represent the propensity of a given delivery type for appointments.
    """
    face_to_face: float = Field(alias="Face-to-Face", **PROPENSITY_FIELD_ARGS)
    home_visit: float = Field(alias="Home Visit", **PROPENSITY_FIELD_ARGS)
    telephone: float = Field(alias="Telephone", **PROPENSITY_FIELD_ARGS)
    unknown: float = Field(alias="Unknown", **PROPENSITY_FIELD_ARGS)
    video_online: float = Field(alias="Video/Online", **PROPENSITY_FIELD_ARGS)

class DeliveryPropensityByStaff(BaseModel):
    gp: AppointmentDeliveryChoice = Field(alias="GP")
    other_practice_staff: AppointmentDeliveryChoice = Field(alias="Other Practice staff")
    unknown: AppointmentDeliveryChoice = Field(alias="Unknown",)

    def get_staff_type(self, staff_type:str)->AppointmentDeliveryChoice:
        return getattr(self, str(staff_type).lower().replace(" ","_"))


class DeliveryPropensityByArea(RootModel[Dict[str, DeliveryPropensityByStaff]], YamlLoader, AreaModel):
    """Class to load and validate the did not attend rates yaml file for a yaml file of areas"""


    def get_appointment_mode(self, area, staff_type:str)->str:
        # randomly choose a staff type depending on the area
        return self.get_area(area).get_staff_type(staff_type).pick()


class MonthlyAppointmentForecast(RootModel[Dict[str,Dict[dt.date, int]]], YamlLoader, AreaModel):
    """Class to load and validate monthly appointments, this is in appointments per day"""

    def get_forecast(self, area:str, date:dt.date)->int:
        area_forecast = self.get_area(area)
        for forecast_month, forecast in area_forecast.items():
            if date.month == forecast_month.month and date.year == forecast_month.year:
                return forecast


class ClinicalStaffFTE(BaseModel):
    gp: float = Field(..., alias="GP")
    direct_patient_care:float = Field(...,alias="Direct Patient Care")
    nurses:float =  Field(..., alias="Nurses")
    advanced_nurse_practictioners:float = Field(..., alias="Advanced Nurse Practitioners")
    

class ClinicalStaffFTEByArea(RootModel[Dict[str, ClinicalStaffFTE]], YamlLoader, AreaModel):
    """Class to load and validate the clinical staff FTE yaml file for a yaml file of areas"""
    
    
class NonGPStaffMix(BaseModel):
    advanced_nurse_practictioners:float = Field(..., alias="Advanced Nurse Practitioners", gte=0.0, lte=1.0)
    direct_patient_care:float = Field(..., alias="Direct Patient Care", gte=0.0, lte=1.0)
    nurses:float = Field(..., alias="Nurses", gte=0.0, lte=1.0)
    

class NonGPStaffMixByArea(RootModel[Dict[str, NonGPStaffMix]], YamlLoader, AreaModel):
    """Class to load and validate the clinical staff FTE yaml file for a yaml file of areas"""
    
    def calc_fte_by_staff(self, fte:float, area:str):
        """returns the non-GP FTE for each clinical staff type, based on the baseline mix"""
        area_mix = self.get_area(area)
        return {k:v*fte for k,v in area_mix.model_dump(by_alias=True).items()}
    

class AdminStaffFTERequirementByArea(RootModel[Dict[str, float]], YamlLoader, AreaModel):
    """Class to load and validate the admin staff FTE requirement yaml file for a yaml file of areas"""
    
    
class DailyForecastAppointments(RootModel[Dict[dt.date, int]]):
    """class to load in forecasts of appointments per day"""
    def get_forecast_for_day(self, date:dt.date):
        return self.root.get(date)

class DailyForecastAppointmentsByArea(RootModel[Dict[str, DailyForecastAppointments]], YamlLoader, AreaModel):
    """Class to load and validate the daily forecast appointments yaml file for a yaml file of areas"""

class AcuteReferralRates(BaseModel):
    gp: float= Field(alias="GP_Ref_rate")
    other: float = Field(alias="Others_Ref_rate")
    
    def did_refer(self, staff_type:str)->bool:
        """returns True if the patient was referred"""
        random_num = random.random()
        # get the propensity for the given staff type
        propensity = getattr(self, staff_type.lower().replace(" ","_"))
        # if the random number is less than the propensity (0-1), the patient was referred
        return random_num < propensity

class AcuteReferralRatesByArea(RootModel[Dict[str, AcuteReferralRates]], YamlLoader, AreaModel):
    """Class to load and validate the acute referral rates yaml file for a yaml file of areas"""
    
    def did_refer(self, area:str, staff_type:str)->bool:
        """returns True if the patient was referred"""
        area_rates:AcuteReferralRates = self.get_area(area)
        return area_rates.did_refer(staff_type)
    
    