import numpy as np
import pandas as pd
import datetime as dt
import pytz
import random
from collections import defaultdict
from typing import Dict, Literal, Optional, Union, Tuple
from tqdm import tqdm
import json
import multiprocessing as mp
from functools import partial
import logging
from datetime import datetime

from src.various_methods import is_working_day
from src.constants import (SARIMA_FORECAST_OUTPUT_FILENAME, 
                         APPOINTMENT_DURATION_OUTPUT_FILENAME, 
                         STAFF_TYPE_PROPENSITY_OUTPUT_FILENAME, 
                         APPOINTMENT_MODE_PROPENSITY_OUTPUT_FILENAME, 
                         POPULATION_PROJECTIONS_OUTPUT_FILENAME,
                         ACUTE_REFERRAL_RATES_OUTPUT_FILENAME,
                         WORKFORCE_CURRENT_STAFF_FTE)

from src.simulation import (SimulationData, 
                          DailyRegionalModel)

# Configure logging with process ID
def setup_logging():
    log_filename = f"outputs/simulation_log_{datetime.now(tz=pytz.timezone('UTC')).isoformat()}.txt"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - Process %(process)d - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

DEMAND_FORECASTS = [
    'SARIMA',
]

CAPACITY_POLICIES = ['Do Nothing']

def merge_daily_summaries(existing_summary: Dict, new_summary: Dict) -> Dict:
    """
    Merge two daily summaries without requiring DailyRegionalModel instance.
    This function should implement the same logic as DailyRegionalModel.update_summary()
    """
    merged = existing_summary.copy()
    # Add your merging logic here based on your summary structure
    # For example, if your summaries contain counts or averages:
    for key in new_summary:
        if key in merged:
            if isinstance(merged[key], (int, float)):
                merged[key] = (merged[key] + new_summary[key]) / 2  # or sum, depending on your needs
            elif isinstance(merged[key], list):
                merged[key].extend(new_summary[key])
            elif isinstance(merged[key], dict):
                merged[key] = merge_daily_summaries(merged[key], new_summary[key])
        else:
            merged[key] = new_summary[key]
    return merged

def process_single_run(run_params: tuple) -> Dict:
    """
    Process a single simulation run with the given parameters.
    """
    simulation_run, start_date, end_date, simulation_data = run_params
    setup_logging()  # Setup logging for this process
    
    date_range = pd.date_range(start=start_date, end=end_date).date
    run_output = {}
    
    logging.info(f"Starting simulation run {simulation_run}")
    
    for demand_forecast in DEMAND_FORECASTS:
        logging.info(f"Demand Forecast: {demand_forecast}")
        run_output[demand_forecast] = {}
        
        for capacity_policy in CAPACITY_POLICIES:
            logging.info(f"Capacity Policy: {capacity_policy}")
            run_output[demand_forecast][capacity_policy] = {}
            
            for region in ['06L', '07K', '06T']:
                logging.info(f"Region: {region}")
                run_output[demand_forecast][capacity_policy][region] = {}
                
                for day in date_range:
                    if is_working_day(day):
                        logging.info(f"Processing day {day}")
                        daily_model = DailyRegionalModel(
                            sim_data=simulation_data,
                            date=day,
                            run_number=simulation_run,
                            region=region,
                            forecast_model=demand_forecast,
                            capacity_policy=capacity_policy
                        )
                        daily_model.process_day()
                        day_isoformat = day.isoformat()
                        run_output[demand_forecast][capacity_policy][region][day_isoformat] = daily_model.create_initial_summary()
    
    return run_output

def merge_run_outputs(outputs_list: list) -> Dict:
    """
    Merge the outputs from multiple simulation runs into a single dictionary.
    """
    merged_outputs = {}
    
    for run_output in outputs_list:
        for demand_forecast in run_output:
            if demand_forecast not in merged_outputs:
                merged_outputs[demand_forecast] = {}
                
            for capacity_policy in run_output[demand_forecast]:
                if capacity_policy not in merged_outputs[demand_forecast]:
                    merged_outputs[demand_forecast][capacity_policy] = {}
                    
                for region in run_output[demand_forecast][capacity_policy]:
                    if region not in merged_outputs[demand_forecast][capacity_policy]:
                        merged_outputs[demand_forecast][capacity_policy][region] = {}
                        
                    for day, summary in run_output[demand_forecast][capacity_policy][region].items():
                        if day in merged_outputs[demand_forecast][capacity_policy][region]:
                            # Merge summaries directly without creating a new DailyRegionalModel
                            merged_outputs[demand_forecast][capacity_policy][region][day] = merge_daily_summaries(
                                merged_outputs[demand_forecast][capacity_policy][region][day],
                                summary
                            )
                        else:
                            merged_outputs[demand_forecast][capacity_policy][region][day] = summary
                            
    return merged_outputs

def run_simulation(start_date: dt.date, end_date: dt.date, n_runs: int) -> Dict:
    """
    Run the simulation in parallel using multiple processes.
    """
    setup_logging()
    logging.info("Starting parallel simulation")
    
    # Initialize simulation data (shared between processes)
    simulation_data = SimulationData()
    
    # Create a pool of workers
    num_processes = mp.cpu_count() #- 1  # Leave one CPU free for system tasks
    pool = mp.Pool(processes=num_processes)
    
    # Prepare parameters for each run
    run_params = [(i, start_date, end_date, simulation_data) for i in range(n_runs)]
    
    # Run simulations in parallel with progress bar
    outputs_list = list(tqdm(
        pool.imap(process_single_run, run_params),
        total=n_runs,
        desc="Processing simulation runs"
    ))
    
    # Clean up
    pool.close()
    pool.join()
    
    # Merge results from all runs
    merged_outputs = merge_run_outputs(outputs_list)
    
    logging.info("Parallel simulation completed")
    return merged_outputs

if __name__ == '__main__':
    
    import time
    
    # Start timing the simulation
    start_time = time.time()

    # Run the simulation
    simulation_outputs = run_simulation(
        start_date=dt.date(2024, 6, 1),
        end_date=dt.date(2024, 6, 30),
        n_runs=10
    )

    # End timing the simulation
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Log the elapsed time
    logging.info(f"Simulation completed in {elapsed_time:.2f} seconds")
    # Save the outputs
    with open('outputs/simulation_outputs.json', 'w') as f:
        json.dump(simulation_outputs, f)