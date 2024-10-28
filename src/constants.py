from typing import Final, Dict, NamedTuple, Type, List
import datetime as dt
import holidays


# NHS ENGLAND APPOINTMENTS
REGIONAL_DATA_ZIP: Final[str] = "https://files.digital.nhs.uk/3D/ED1EDE/Appointments_GP_Regional_CSV_Aug_23.zip"
# CSV OF INTEREST
SNEE_CSV: Final[str] = "/content/Regional_CSV_SuffolkNEEssex.csv"

ONS_POPULATION_SCENARIOS_NAME = "ONS Population projections by single year of age mid-2018 to mid-2043"
# ONS DATA
SUBNATIONAL_ONS_ZIP: Final[str] = "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/localauthoritiesinenglandz1/2018based/2018snpppopulation.zip"
# Dictionary of ONS CSVs
ONS_CSVS: Final[Dict[str, str]] = {
    k: f"/content/2018 SNPP Population {k}.csv" for k in ['males', 'females', 'persons']}

# BANK HOLIDAYS
ENGLAND_BANK_HOLIDAYS: Final[Type[Dict[dt.date, str]]] = holidays.UnitedKingdom(
    years=[i for i in range(2021, 2035)])

# SUB ICB AREAS
IPS_EAST_SUFF = "Ipswich & East Suffolk"
WEST_SUFF = "West Suffolk"
NE_ESSEX = "North East Essex"

# SUB ICB CODES
SUB_ICB_CODES:Final[Dict[str,str]] = {"06L": IPS_EAST_SUFF,
                 "07K": WEST_SUFF,
                 "06T": NE_ESSEX}

# ONS CODE
ONS_CODES:Final[Dict[str,str]] = {"E38000086": IPS_EAST_SUFF,
                 "E38000204": WEST_SUFF,
                 "E38000117": NE_ESSEX}

# CCG to sub-ICB
CCG_SUB_ICB:Final[Dict[str,str]] = {"NHS Ipswich and East Suffolk CCG": IPS_EAST_SUFF,
               "NHS West Suffolk CCG": WEST_SUFF,
               "NHS North East Essex CCG": NE_ESSEX}

# ONS TO SUB-ICB
ICB_ONS_AREAS:Final[Dict[str,str]] = {"Tendring": NE_ESSEX,
                 "Colchester": NE_ESSEX,
                 "Forest Heath": WEST_SUFF,
                 "St Edmundsbury": WEST_SUFF,
                 "Babergh": IPS_EAST_SUFF,
                 "Mid Suffolk": IPS_EAST_SUFF,
                 "Suffolk Coastal": IPS_EAST_SUFF,
                 "Ipswich": IPS_EAST_SUFF}

#ORG Code
ORG_CODE:Final[Dict[str,str]] = {'QJG': 'NHS SUFFOLK AND NORTH EAST ESSEX INTEGRATED CARE BOARD'}

# Location for outputs
# these are all relative to the repo root directory ! 
NOTEBOOK_OUTPUT_BASE_PATH:Final[str] = "outputs/"
NOTEBOOK_OUTPUT_TABLES_PATH:Final[str] = NOTEBOOK_OUTPUT_BASE_PATH + "tables/"
NOTEBOOK_OUTPUT_FIGURES_PATH:Final[str] = NOTEBOOK_OUTPUT_BASE_PATH + "plots/"
SIMULATION_RESULTS_PATH:Final[str] = NOTEBOOK_OUTPUT_BASE_PATH + "simulation_results/"

GP_LIST_AGE_BANDS:Final[List[int]] = [i for i in range(0, 95, 5)] + [200]
GP_LIST_AGE_LABELS:Final[List[str]] = [f"{i}-{i+4}" for i in GP_LIST_AGE_BANDS[:-2]] + ["90+"]


#notebook 1a
APPOINTMENT_DURATION_OUTPUT_FILENAME = "outputs/appointment_durations.yaml"

#notebook 1b
APPOINTMENTS_DNA_OUTPUT_FILENAME = "outputs/appointment_dna.yaml"
APPOINTMENT_MODE_PROPENSITY_OUTPUT_FILENAME = "outputs/appointment_modes.yaml"
STAFF_TYPE_PROPENSITY_OUTPUT_FILENAME = "outputs/staff_propensity.yaml"

#notebook 1c
POPULATION_PROJECTIONS_OUTPUT_FILENAME = "outputs/population_projections.yaml"
SAME_DAY_APPOINTMENT_OUTPUT_FILENAME = "outputs/same_day_appointment.yaml"

#notebook 1d
ACUTE_REFERRAL_RATES_OUTPUT_FILENAME = "outputs/acute_referral_rates.yaml"

#notebook 2a
APPOINTMENTS_REGRESSION_MODEL_FILENAME= "outputs/demographic-month-sklearn.pkl"

#notebook 2b
SARIMA_FORECAST_OUTPUT_FILENAME = "outputs/forecasts-SARIMA.yaml"

# notebook 2c
WORKFORCE_ADMIN_REQUIREMENTS_FILENAME  ="outputs/workforce_admin_fte_requirements.yaml"
WORKFORCE_NON_GP_CLINICAL_STAFF_SPLIT_FILENAME = "outputs/workforce_non_gp_clinical_staff_mix.yaml"
WORKFORCE_CURRENT_STAFF_FTE = "outputs/workforce_current_staff_fte.yaml"
