Title: Population Projection
Date: 2024-01-03
Modified: 2024-01-03
Category: Demand Analysis
Authors: A.Jarman & I.Khan
Summary: Analysis on primary care population projection and demographics in SNEE-ICB

<br>

## Introduction & Background
In order to estimate future staffing requirements and demand for primary care services in the SNEE footprint, it is essential to understand the likely changes in population and demographics over the 10 year horizon that the D&C model investigates.
<br><br>

## Data Sources
ONS Population projections were used for the forward-looking population estimates used in the model. These are unfortunately 2018-based, so are not in line with the 2021 census, however they were revised in 2020. These are provided at the Clinical Commissioning Group (CCG) level (now sub-ICBs).
<table>
    <thead>
        <tr>
            <th>Dataset used</th>
            <th>Website URL</th>
            <th>Download zip</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Registred patients dataset</td>
            <td><a href="https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice", target=blank>Patients Registered at a GP practice, September 2024</a></td>
            <td><a href="https://files.digital.nhs.uk/31/AA1C9E/gp-reg-pat-prac-quin-age.zip">gp-reg-pat-prac-quin-age.csv</a></td>
        </tr>
        <tr>
            <td>Population Projections for CCGs by ONS</td>
            <td><a href="https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/clinicalcommissioninggroupsinenglandz2", target=blank>ONS Population Projections</a></td>
            <td>N/A</td>
        </tr>
    </tbody>
</table>
<br>


## Methodology
- Before the analysis, the data was pre-processed and cleaned.
- A 'baseline' population was established using the GP patient lists for each sub-ICB area for the year 2024.
- Population change factor for each year (2025-44) and each 5 year age band was then calculated from the ONS population scenarios, again using 2024 as a baseline.
- The baseline population was then multiplied by these coefficients to produce a population projection for each scenario.

After examining the data, it was decided that FY2024 is probably the most 'normal' year representing more typical demand after COVID-19 disrupted the previous years, both in terms of appointment times and also formats.
<br><br>

# Caveats & Problems
The geographical mapping between Ipswich and East Suffolk / West Suffolk sub ICBs are not identical to the Primary care network (PCN) boundaries; in this case those patients in the Ixworth (IP31) area would be considered to be in the Ipswich & east Suffolk ICB, however they are located in the West suffolk PCN. Therefore the population estimates for the two sub-ICB locations/ PCN locations are slightly misaligned and the expectation is that the projections would be expected to be marginally less accurate.
<br><br>

## Results and Inferences
The results were a fitted set of distribution parameters which can be re-created during simulation runs. This is saved to a `yaml` file which is then easily read by the simulation application using a built in python package. These are positional arguments to scipy functions which recreate the distributions.

### Population growth scenarios: Based on Principal Projection
![Population Projections]({attach}/img/Demographic_pop_growth_1.png)  
<br>

### Over 65's Scenarios: Based on Principal Projection
![Population Projections]({attach}/img/Demographic_pop_growth_2.png) 
<br>

**The population projections for '10 year migration variant', 'High international migration variant', 'Low international migration variant', 'Alternative internal migration variant', have been stored in the yaml file**.<br>
Link to download--> [Download Projected Population Data](/extras/population_projections.yaml) 


<br><hr><br>


