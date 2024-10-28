from typing import Dict, Literal, Optional, Union, Tuple, List
import random
import datetime as dt


from src.simulation_schemas import (AreaAppointmentTimeDistributions, 
                                    DeliveryPropensityByArea, 
                                    PopulationScenarios, 
                                    DidNotAttendRatesByArea, 
                                    ClinicalStaffFTEByArea, 
                                    StaffPropensityByArea,
                                    AcuteReferralRatesByArea,
                                    DailyForecastAppointmentsByArea)

from src.constants import (SARIMA_FORECAST_OUTPUT_FILENAME, 
                           APPOINTMENT_DURATION_OUTPUT_FILENAME, 
                           STAFF_TYPE_PROPENSITY_OUTPUT_FILENAME, 
                           APPOINTMENT_MODE_PROPENSITY_OUTPUT_FILENAME, 
                           POPULATION_PROJECTIONS_OUTPUT_FILENAME,
                           ACUTE_REFERRAL_RATES_OUTPUT_FILENAME,
                           WORKFORCE_CURRENT_STAFF_FTE)

HOURS_PER_DAY = 7.5
MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR
CONSTRAINED_APPOINTMENT_RANGE = (25,28)

STAFF_TYPE_MAPPING =  {"gp":"GP",
                       "nurses":"Other Practice staff",
                       "direct_patient_care": "Other Practice staff", 
                       "advanced_nurse_practictioners":"Other Practice staff"}


# Class representing an individual staff member
class StaffMembers:
    def __init__(self,
                 staff_type:Literal['GP','Other practice staff'], 
                 fte:float, 
                 appointment_limit:bool=False):
        """
        Initializes a staff member object, this is effectively a pool of staff resources for 1 working day.

        Parameters:
        - staff_type: The type of staff member (e.g., 'GP', 'Other practice staff').
        - fte: The full-time equivalent (FTE) value of the staff member.
        - appointment_limit: Whether the staff member practices safe appointment scheduling. Defaults to False.

        Attributes:
        - staff_type: The type of staff member.
        - initial_time: The available time per day in minutes, calculated based on the FTE value.
        - available_time: The initially available time per day in minutes.
        - safe_practice: Whether the staff member practices safe appointment scheduling.
        - initial_appointments: The initial number of appointments per day, calculated based on the FTE value and safe_practice.
        - available_appointments: The initially available number of appointments per day.

        """
        self.staff_type = staff_type  # Type of staff (e.g., GP)
        self.initial_time = fte* MINUTES_PER_DAY  # Available time per day in minutes
        self.available_time = self.initial_time  # Initially, all daily time is available
        self.appointment_limit = appointment_limit  # Whether the staff member practices safe appointment scheduling
        if appointment_limit: # give them a set number of appointments per day.
            appts = 0 
            for i in range(int(fte)):
                # make a set of appointments for each FTE
                appts += random.randint(*CONSTRAINED_APPOINTMENT_RANGE) # 25-28 appointments per day per fte if constrained 
            # find the remainder (FTE) and multiply by the random number of appointments
            remainder = int((fte - int(fte)) * random.randint(*CONSTRAINED_APPOINTMENT_RANGE))
            self.initial_appointments = appts + remainder
            self.available_appointments = self.initial_appointments
        else:
            # these aren't constrained, so just setting arbitary values
            self.initial_appointments = fte * 99
            self.available_appointments = fte * 99

    def patient_request_appointment(self, appointment_duration:float)->bool:
        """
        Checks if a patient can request an appointment based on the availability of appointments and time.

        Args:
            appointment_duration (float): The duration of the appointment in minutes.

        Returns:
            bool: True if the patient request is successful
        """
        # if safe_practice, then constrain appointments & appointment time
        if self.appointment_limit:
            if self.available_appointments > 0 and self.available_time >= appointment_duration:
                self.available_appointments -= 1
                self.available_time -= appointment_duration
                return True
            else:
                return False
        else:
            # only depends on time, safe practice is not observed
            if self.available_time >= appointment_duration:
                self.available_time -= appointment_duration
                return True
            else:
                return False


class SimulationData:
    """
    This class effectively holds all the data calculated from the notebooks in one big class.
    Might be approprate to break this into several classes in time.
    """


    def __init__(self):

       
        #population scenarios
        self.population_scenarios:PopulationScenarios = PopulationScenarios.read_yaml(POPULATION_PROJECTIONS_OUTPUT_FILENAME)
        # staffing levels
        self.staff_fte = ClinicalStaffFTEByArea.read_yaml(WORKFORCE_CURRENT_STAFF_FTE)
        # prpoensity to attend
        self.did_not_attend_rates = DidNotAttendRatesByArea.read_yaml("outputs/assumptions/dna_appointments.yaml")
        # DEMAND SCENARIOS
        self.appointment_forecasts = {'SARIMA' : DailyForecastAppointmentsByArea.read_yaml(SARIMA_FORECAST_OUTPUT_FILENAME),
                                    #   'Regression - Principal Projection': None,
                                    #   'Regression - High International Migration Variant':None,
                                    #   'Regression - Low International Migration Variant': None
        } # TODO: Complete these
        self.staff_type_propensity = StaffPropensityByArea.read_yaml(STAFF_TYPE_PROPENSITY_OUTPUT_FILENAME)
        self.appointment_mode_propensity = DeliveryPropensityByArea.read_yaml(APPOINTMENT_MODE_PROPENSITY_OUTPUT_FILENAME)
        self.appointment_durations = AreaAppointmentTimeDistributions.read_yaml(APPOINTMENT_DURATION_OUTPUT_FILENAME)
        self.acute_referral_rates = AcuteReferralRatesByArea.read_yaml(ACUTE_REFERRAL_RATES_OUTPUT_FILENAME)
    
        

class DailyRegionalModel:
    def __init__(self, sim_data:SimulationData, date:dt.date, run_number:int, region:str, forecast_model:str, capacity_policy:str, n_appointments:Optional[int]=None):
        
        self.sim_data = sim_data
        self.date = date
        self.run_number = run_number
        self.region = region
        self.forecast_model = forecast_model
        self.capacity_policy = capacity_policy

        if n_appointments is None:
            self.n_patients = self.sim_data.appointment_forecasts[self.forecast_model].get_area(self.region).get_forecast_for_day(date)
        else:
            self.n_patients = n_appointments


        loaded_staff_data = sim_data.staff_fte.get_area(region).model_dump()

        # staff parameters, this holds a dictionary of staff types, and the 
        self.staff = self.map_staff_fte_to_appointment_type(loaded_staff_data)
        staff_types = self.staff.keys()
        
        # appointments output
        self.fufilled_appointments = {staff_type:0 for staff_type in staff_types}
        self.unmet_demand_appointments = {staff_type:0 for staff_type in staff_types}
        self.no_show_appointments = {staff_type:0 for staff_type in staff_types}

        # minutes output
        self.fufilled_minutes = {staff_type:0 for staff_type in staff_types}
        self.unmet_demand_minutes = {staff_type:0 for staff_type in staff_types}
        self.no_show_minutes = {staff_type:0 for staff_type in staff_types}
        
        
    def map_staff_fte_to_appointment_type(self, staff_data:dict)->str:
        # define the staff type map
        output_fte = {k:0.0 for k in set(STAFF_TYPE_MAPPING.values())}
        for k,v in staff_data.items():
            output_fte[STAFF_TYPE_MAPPING[k]] += v
            # TODO: add in the appointment limit from capacity policy
        return {k:StaffMembers(staff_type=k,fte=v, appointment_limit=False) for k,v in output_fte.items()}
        
                
            
        
        
    
    def process_day(self):
        """
        - Each patient is processed in turn. 
        - The patient is assigned to a staff member based on the population propensity to see each staff member.
        The patient is then assigned an appointment mode based on the staff member's propensity to use that mode. 
        The patient is then assigned an appointment duration based on the staff member's propensity to use that duration. 
        The patient is then assigned an appointment time based on the staff member's availability. 
        If the staff member is available, the patient is assigned to that staff member. If the staff member is not available, the patient is assigned to the unmet demand.
        """
        for patient in range(self.n_patients):
            # Choose a staff type
            staff_type:str = self.sim_data.staff_type_propensity.pick_staff_type(self.region)
            # Choose an appointment mode
            appointment_mode:str = self.sim_data.appointment_mode_propensity.get_appointment_mode(area=self.region,staff_type=staff_type)
            # Choose an appointment duration
            duration:int = self.sim_data.appointment_durations.get_area(self.region).get_time()
            # Check if the staff member is available
            if self.staff[staff_type].patient_request_appointment(duration):
                # determine if they show up
                # they can only no show if they actually get an appointment!!
                # returns True if they attended
                if not self.sim_data.did_not_attend_rates.did_patient_attend(area=self.region, staff_type=staff_type, appointment_mode=appointment_mode):
                    # patient did not attend
                    self.no_show_appointments[staff_type] += 1
                    self.no_show_minutes[staff_type] += duration
                else:
                    # patient attended
                    self.fufilled_appointments[staff_type] += 1
                    self.fufilled_minutes[staff_type] += duration 
            else:
                self.unmet_demand_appointments[staff_type] += 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                self.unmet_demand_minutes[staff_type] += duration                                                                
                
        return
        
    def create_initial_summary(self)->Dict[str,Dict[str,List[Union[float,int]]]]:
        # only used on the first run.

            return {
                'fufilled_appointments':{k:[v] for k,v in self.fufilled_appointments.items()},
                'no_show_appointments': {k:[v] for k,v in self.no_show_appointments.items()},
                'unmet_demand_appointments': {k:[v] for k,v in self.unmet_demand_appointments.items()},
                'fufilled_minutes': {k:[v] for k,v in self.fufilled_minutes.items()},
                'no_show_minutes': {k:[v] for k,v in self.no_show_minutes.items()},
                'unmet_demand_minutes': {k:[v] for k,v in self.unmet_demand_minutes.items()}
                }
    
    def update_summary(self, summary:Dict[str,Dict[str,List[Union[float,int]]]])->None:
        
        # iterate through each of the keys and find the matching instance variable
        # iterate though those and append the values to the list
        for key, appointment_dict in summary.items():
            for staff_type, appt_data  in appointment_dict.items():
                summary[key][staff_type].append(getattr(self,key)[staff_type])
            





