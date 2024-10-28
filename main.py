import numpy as np
import pandas as pd
import datetime as dt
import pytz
import random
from collections import defaultdict
from typing import Dict, Literal, Optional, Union, Tuple
from tqdm import tqdm
from icecream import ic
import json

from src.various_methods import is_working_day
import logging
from datetime import datetime

from src.constants import (SARIMA_FORECAST_OUTPUT_FILENAME, 
                           APPOINTMENT_DURATION_OUTPUT_FILENAME, 
                           STAFF_TYPE_PROPENSITY_OUTPUT_FILENAME, 
                           APPOINTMENT_MODE_PROPENSITY_OUTPUT_FILENAME, 
                           POPULATION_PROJECTIONS_OUTPUT_FILENAME,
                           ACUTE_REFERRAL_RATES_OUTPUT_FILENAME,
                           WORKFORCE_CURRENT_STAFF_FTE)

from src.simulation import (SimulationData, 
                            DailyRegionalModel)
from src.simulation_schemas import SimulationOutputs

# Configure logging
log_filename = f"outputs/simulation_log_{datetime.now(tz=pytz.timezone('UTC')).isoformat()}.txt"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
# Example log entry
logging.info("Simulation log started.")

DEMAND_FORECASTS = [
    'SARIMA',
    # 'Regression - Principle Projection'
    # 'Regression - High International Migration Variant'
    # 'Regression - Low International Migration Variant'
    ]

CAPACITY_POLICIES = ['Do Nothing']

def run_simulation(start_date:dt.date,end_date:dt.date, n_runs:int):
    simulation_data = SimulationData()
    date_range = pd.date_range(start=start_date,end=end_date).date

    run_outputs = {}
    # iterate through the runs
    print("\n*****\n")
    for simulation_run in tqdm(range(n_runs)):
        # set empty outputs
        logging.info(f"Starting simulation run {simulation_run}")
        # iterate through the forecast methods
        for demand_forecast in DEMAND_FORECASTS: 
            logging.info(f"Demand Forecast: {demand_forecast}")
            # set empty outputs
            if not run_outputs.get(demand_forecast):
                run_outputs[demand_forecast] = {}
            # iterate through the capacity policies
            for capacity_policy in CAPACITY_POLICIES:
                logging.info(f"Capacity Policy: {demand_forecast}")
                if not run_outputs[demand_forecast].get(capacity_policy):
                    run_outputs[demand_forecast][capacity_policy] = {}
                # iterate through the regions
                for region in ['06L','07K','06T']:
                    logging.info(f"Region: {region}")

                    if not run_outputs[demand_forecast][capacity_policy].get(region):
                        run_outputs[demand_forecast][capacity_policy][region] = {}
                    # iterate through the dates
                    for day in date_range:
                        if is_working_day(day):
                            logging.info(f"Processing day {day}")
                            # run the simulation
                            daily_model = DailyRegionalModel(
                                sim_data=simulation_data, 
                                date=day, 
                                run_number=simulation_run, 
                                region=region,
                                forecast_model=demand_forecast,
                                capacity_policy=capacity_policy)
                            daily_model.process_day() # run the sim
                            day_isoformat = day.isoformat()
                            if run_outputs[demand_forecast][capacity_policy][region].get(day_isoformat):
                                daily_model.update_summary(run_outputs[demand_forecast][capacity_policy][region][day_isoformat])
                            else: 
                                run_outputs[demand_forecast][capacity_policy][region][day_isoformat] = daily_model.create_initial_summary()
                        # no need for else statement as the run_outputs are not created for non-working days
                        
    return run_outputs # end of loop



if __name__ == '__main__':
        
    simulation_outputs = run_simulation(
        start_date = dt.date(2024,6,1),
        end_date = dt.date(2025,5,31),
        n_runs=2)
    # save the outputs
    with open('outputs/simulation_outputs.json', 'w') as f:
        json.dump(simulation_outputs, f)
