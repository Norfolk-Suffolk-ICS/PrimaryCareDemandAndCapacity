Title: Referral Rate
Date: 2024-01-04
Modified: 2024-10-10
Category: Capacity Analysis
Authors: A.Jarman & I.Khan
Summary: Analysis on primary care rate of referrals in SNEE-ICB 

<br>

## Introduction & Background
The referral rate is calculated as the number of referrals divided by the total number of appointments per year, it is a critical metric in understanding healthcare dynamics. In this part of analysis, our focus is on comprehending the volume of referrals originating from each sub-ICB (Integrated Care Board) under SNEE (Suffolk and North East Essex) that remain within the area (ESNEFT and WSFT) and those extending beyond its borders.
<br><br>

## Data Sources
For this analysis, the primary data sources utilized were NHS England's referrals and appointments datasets.
- The referrals dataset is predominantly encompassing data points from April 2023 to March 2024.
- The appointments dataset is spanning from March 2022 to August 2024. While FY22 and FY23 were based on complete annual data, the assessment for FY24 is limited to the available data from April to August.
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
            <td>Referrals dataset</td>
            <td><a href="https://www.england.nhs.uk/statistics/statistical-work-areas/outpatient-referrals/">NHS England - Outpatient Referrals</a></td>
            <td><a href="https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2/2024/05/Annual-CSV-2023-24-Published-May-2024-59834-1.zip">Annual CSV 2023-24 Published May 2024</a></td>
        </tr>
        <tr>
            <td>Appointments dataset</td>
            <td><a href="https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice">NHS Digital - Appointments in General Practice</a></td>
            <td><a href="https://files.digital.nhs.uk/D5/4B437E/Appointments_GP_Regional_CSV_Aug_24.zip">Regional CSV SuffolkNEEssex (Mar22 - Aug24)</a></td>
        </tr>
    </tbody>
</table>
<br>

## Methodology
Before the analysis, the data was pre-processed.

- Appointments dataframe underwent a cleaning process where 'Unknown' entries under HCP-type were replaced with 'Other practice staff'.
- Extra columns were dropped from both the datasets
- Filtering the datsets to only keep records for SNEE-ICB
  
The initial step involved grouping the dataset to get the total number of referrals to each SUB-ICB areas between April 2023 and March 2024 namely, Ipswich & East Suffolk (06L), West Suffolk (07K), and North East Essex (06T).

Upon preparing both datasets, the referral rate for each SNEE-ICB area was computed by dividing the referrals dataset by the appointments dataset. The resulting table, included at the conclusion of this document, outlines the referral rates for each SNEE SUB-ICB area concerning GP and Other practice staff.
<br><br>

## Insights through Sankey Diagram
Interpretation of the data via a Sankey Diagram revealed noteworthy insights:

- Of the three Sub-ICB's, **Ipswich & East Suffolk** had the **highest volume of referrals**.
- Aside from SNEE-ICB, the highest number of referrals by both GPs and Other practice staff were directed towards **Cambridgeshire and Peterborough ICB**.

<hr>
<iframe src="Referral_rate_2_sankey.html" width="80%" height="1000px"></iframe>
<br><br>
<iframe src="Referral_rate_4_sankey.html" width="80%" height="1000px"></iframe>
<br>

## Results
The results were set of referrals rates which can be re-created during simulation runs. This is saved to a `yaml` file which is then easily read by the simulation application using a built in python package.

<table>
    <thead>
        <tr>
            <th>Code</th>
            <th>GP Referral Rate</th>
            <th>Others Referral Rate</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Ipswich & East Suffolk (06L)</td>
            <td>0.0983</td>
            <td>0.0491</td>
        </tr>
        <tr>
            <td>North East Essex (06T)</td>
            <td>0.0602</td>
            <td>0.0324</td>
        </tr>
        <tr>
            <td>West Suffolk (07K)</td>
            <td>0.0759</td>
            <td>0.0595</td>
        </tr>
    </tbody>
</table>

<br><hr><br>