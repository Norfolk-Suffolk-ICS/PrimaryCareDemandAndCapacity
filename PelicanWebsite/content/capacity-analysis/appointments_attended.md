Title: Appointments Attendance
Date: 2024-01-04
Modified: 2024-10-11
Category: Capacity Analysis
Authors: A.Jarman & I.Khan
Summary: Analysis on primary care appointments (Attended/DNA) in SNEE-ICB

<br>

## Introduction & Background
Understanding the frequency of missed appointments in SNEE footprints is crucial.  This analysis endeavors to construct a model that captures the instances of missed appointments, allowing patients to re-enter the system at a later date.
<br><br>

## Data Sources
The primary data for this analysis is derived from the extensive appointments dataset provided by NHS England, spanning from March 2022 to August 2024. While FY22 and FY23 were based on complete annual data, the assessment for FY24 is limited to the available data from April to August.
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
            <td>Appointments dataset</td>
            <td><a href="https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice">NHS Digital - Appointments in General Practice</a></td>
            <td><a href="https://files.digital.nhs.uk/D5/4B437E/Appointments_GP_Regional_CSV_Aug_24.zip">Regional CSV SuffolkNEEssex (Mar22 - Aug24)</a></td>
        </tr>
    </tbody>
</table>
<br>


## Methodology
Before the analysis, the data was pre-processed. 

- Appointment months were converted into FY-years.
- Calculated the national averages and proportional representation for each appointment type.

1- Comparison with SNEE Area:

- Conducted a comparative analysis between the national averages and proportions with the SNEE area for fiscal years 2022, 2023, and 2024.
- Visualized the results through detailed comparison plots.

2- Detailed Proportion Analysis:

- Extracted proportions of attended, did not attend (DNA), and unknown appointments based on SUB-ICB, healthcare professional type (hcp_type), and appointment mode.
- Plotted the changes in did not attend (DNA) appointments over the years.

3- Correlation Matrix:

- Conducted a correlation matrix analysis to identify factors affecting the likelihood of DNA appointments  in the SNEE area.

4- Identifying Appointment Trends:

- Explored if certain appointments are more likely to be missed.
- Conducted additional analysis on appointment types with higher likelihood of being missed.

This approach involves a comprehensive examination of various factors influencing appointment attendance, utilizing visualizations for better understanding. This structured analysis should provide valuable insights into missed appointments trends and potential influencing factors in the SNEE area.
<br><br>

## Results and Inferences 

### 1. Missed (DNA) appointments comparison of proportion and average (per month): SNEE-ICB and National average

<table>
  <thead>
    <tr>
      <th rowspan="2">Year</th>
      <th colspan="2">Attended (Average, %)</th>
      <th colspan="2">DNA (Average, %)</th>
      <th colspan="2">Unknown (Average, %)</th>
    </tr>
    <tr>
      <th>Nation wide</th>
      <th>SNEE</th>
      <th>Nation wide</th>
      <th>SNEE</th>
      <th>Nation wide</th>
      <th>SNEE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>FY-2022</td>
      <td>608,099 (91.21%)</td>
      <td>465,022 (93.22%)</td>
      <td>31,569 (4.63%)</td>
      <td>17,823 (3.51%)</td>
      <td>27,096 (4.17%)</td>
      <td>16,936 (3.27%)</td>
    </tr>
    <tr>
      <td>FY-2023</td>
      <td>628,297 (90.04%)</td>
      <td>481,801 (91.84%)</td>
      <td>31,723 (4.45%)</td>
      <td>16,480 (3.11%)</td>
      <td>38,692 (5.51%)</td>
      <td>27,284 (5.06%)</td>
    </tr>
    <tr>
      <td>FY-2024 (Apr-Aug)</td>
      <td>629,349 (90.06%)</td>
      <td>493,590 (92.03%)</td>
      <td>30,356 (4.22%)</td>
      <td>15,572 (2.88%)</td>
      <td>40,010 (5.72%)</td>
      <td>27,752 (5.09%)</td>
    </tr>
  </tbody>
</table>
<br>

Based on the above table:

- The average percentage of **DNA appointments** for SNEE-ICB is consistently **lower** than the National Average across all observed years
- Conversely, the average percentage of **Attended appointments** for SNEE-ICB is consistently **higher** than the National Average for each year, suggesting a more favorable attendance trend in SNEE.
Overall, these findings highlight the effectiveness of SNEE-ICB's initiatives in reducing missed appointments while promoting higher attendance rates compared to the national landscape.<br>

The plot below confirms that the average number of attended/DNA appointments in SNEE is lower compared to other ICBs.
<br>

![Average appointments]({attach}/img/Appointment_attendance_1.png)

<br>

### Breaking down appointment trends by SNEE Sub-ICB Areas
<table>
  <tr>
    <th>SUB_ICB_LOCATION_CODE</th>
    <th>FY_YEAR</th>
    <th>Attended (%)</th>
    <th>DNA (%)</th>
    <th>Unknown (%)</th>
  </tr>
  <tr>
    <td rowspan="3">Ipswich & East Suffolk (06L)</td>
    <td>FY2022</td>
    <td>93.62%</td>
    <td>2.79%</td>
    <td>3.59%</td>
  </tr>
  <tr>
    <td>FY2023</td>
    <td>91.44%</td>
    <td>2.79%</td>
    <td>5.77%</td>
  </tr>
  <tr>
    <td>FY2024</td>
    <td>92.04%</td>
    <td>2.50%</td>
    <td>5.46%</td>
  </tr>
  <tr>
    <td rowspan="3">North East Essex (06T)</td>
    <td>FY2022</td>
    <td>91.16%</td>
    <td>4.91%</td>
    <td>3.92%</td>
  </tr>
  <tr>
    <td>FY2023</td>
    <td>90.65%</td>
    <td>3.85%</td>
    <td>5.50%</td>
  </tr>
  <tr>
    <td>FY2024</td>
    <td>90.38%</td>
    <td>3.79%</td>
    <td>5.83%</td>
  </tr>
  <tr>
    <td rowspan="3">West Suffolk (07K)</td>
    <td>FY2022</td>
    <td>94.88%</td>
    <td>2.84%</td>
    <td>2.29%</td>
  </tr>
  <tr>
    <td>FY2023</td>
    <td>93.42%</td>
    <td>2.68%</td>
    <td>3.90%</td>
  </tr>
  <tr>
    <td>FY2024</td>
    <td>93.67%</td>
    <td>2.36%</td>
    <td>3.97%</td>
  </tr>
</table>

- The sub-ICB North East Essex (06T) demonstrates the highest proportion of DNA appointments, suggesting a significant challenge in managing appointment attendance within this region.
- Conversely, the sub-ICB West Suffolk (07K) exhibits the maximum proportion of Attended appointments, indicating a strong performance in appointment adherence.
<br><br>


### 2. Did not attend appointments trends over Time/Years

**Nation Wide**
<br>

![DNA-FY(21-22-23)]({attach}/img/Appointment_attendance_7.png)

We can infer that -

- Nationally the missed appointments are consistent over years when appointment mode is Face to Face, home visit or telephonic.
- Nationally inconsistencies is observed in appointments with unknown or video/online modes over the years.

- Below graph represents the same information for SNEE-ICB areas

**SNEE-ICB**
<br>

![DNA-FY(21-22-23)]({attach}/img/Appointment_attendance_8.png)

<br><br>


### 3. To understand if Across staff groups & Sub-ICB, are some appointments more likely to be missed/attended

**Below table shows the comaparison between proportion of appointments (Attended,DNA and Unknown) National vs SNEE, based on HCP type and Appointment mode**

<table>
  <tr>
    <th colspan="2">TYPE</th>
    <th colspan="2">Attended</th>
    <th colspan="2">DNA</th>
    <th colspan="2">Unknown</th>
  </tr>
  <tr>
    <th>HCP_TYPE</th>
    <th>APPT_MODE</th>
    <th>Nation wide</th>
    <th>SNEE</th>
    <th>Nation wide</th>
    <th>SNEE</th>
    <th>Nation wide</th>
    <th>SNEE</th>
  </tr>
  <tr>
    <td rowspan="5">GP</td>
    <td>Face-to-Face</td>
    <td>93.02%</td>
    <td>94.93%</td>
    <td>3.61%</td>
    <td>2.21%</td>
    <td>3.37%</td>
    <td>2.86%</td>
  </tr>
  <tr>
    <td>Home Visit</td>
    <td>84.79%</td>
    <td>94.10%</td>
    <td>2.02%</td>
    <td>1.48%</td>
    <td>13.20%</td>
    <td>4.42%</td>
  </tr>
  <tr>
    <td>Telephone</td>
    <td>95.14%</td>
    <td>97.31%</td>
    <td>1.64%</td>
    <td>0.65%</td>
    <td>3.22%</td>
    <td>2.04%</td>
  </tr>
  <tr>
    <td>Unknown</td>
    <td>50.21%</td>
    <td>54.27%</td>
    <td>2.15%</td>
    <td>2.32%</td>
    <td>47.63%</td>
    <td>43.41%</td>
  </tr>
  <tr>
    <td>Video/Online</td>
    <td>89.91%</td>
    <td>93.06%</td>
    <td>0.80%</td>
    <td>0.88%</td>
    <td>9.30%</td>
    <td>6.06%</td>
  </tr>
  <tr>
    <td rowspan="5">Other Practice Staff</td>
    <td>Face-to-Face</td>
    <td>87.68%</td>
    <td>89.53%</td>
    <td>6.99%</td>
    <td>4.95%</td>
    <td>5.33%</td>
    <td>5.52%</td>
  </tr>
  <tr>
    <td>Home Visit</td>
    <td>82.84%</td>
    <td>89.38%</td>
    <td>3.16%</td>
    <td>3.22%</td>
    <td>14.01%</td>
    <td>7.40%</td>
  </tr>
  <tr>
    <td>Telephone</td>
    <td>92.03%</td>
    <td>95.14%</td>
    <td>3.38%</td>
    <td>1.20%</td>
    <td>4.59%</td>
    <td>3.66%</td>
  </tr>
  <tr>
    <td>Unknown</td>
    <td>41.40%</td>
    <td>47.27%</td>
    <td>2.94%</td>
    <td>3.10%</td>
    <td>55.67%</td>
    <td>49.63%</td>
  </tr>
  <tr>
    <td>Video/Online</td>
    <td>89.44%</td>
    <td>93.37%</td>
    <td>1.39%</td>
    <td>2.87%</td>
    <td>9.17%</td>
    <td>3.76%</td>
  </tr>
  <tr>
    <td rowspan="5">Unknown</td>
    <td>Face-to-Face</td>
    <td>75.70%</td>
    <td>41.70%</td>
    <td>2.29%</td>
    <td>49.28%</td>
    <td>24.33%</td>
    <td>9.02%</td>
  </tr>
  <tr>
    <td>Home Visit</td>
    <td>67.79%</td>
    <td>89.15%</td>
    <td>3.80%</td>
    <td>0.92%</td>
    <td>30.63%</td>
    <td>9.93%</td>
  </tr>
  <tr>
    <td>Telephone</td>
    <td>90.15%</td>
    <td>93.40%</td>
    <td>2.35%</td>
    <td>3.82%</td>
    <td>10.79%</td>
    <td>2.77%</td>
  </tr>
  <tr>
    <td>Unknown</td>
    <td>74.19%</td>
    <td>90.67%</td>
    <td>2.27%</td>
    <td>2.26%</td>
    <td>31.84%</td>
    <td>7.06%</td>
  </tr>
  <tr>
    <td>Video/Online</td>
    <td>79.00%</td>
    <td>100.00%</td>
    <td>2.73%</td>
    <td>2.76%</td>
    <td>21.19%</td>
    <td>18.84%</td>
  </tr>
</table>

**Major Highlights**

- SNEE consistently outperforms national averages across most appointment modes and HCP types, especially in home visits and telephone appointments.
- Face-to-Face Appointments: High attendance rates with low DNA rates, but a small percentage of unknown outcomes.
- Home Visits: Moderate attendance rates with low DNA rates, but a notable percentage of unknown outcomes.
- Telephone Appointments: Very high attendance rates with minimal DNA rates and low unknown outcomes.
- Unknown Mode: Low attendance rates with a high percentage of unknown outcomes, indicating a need for better tracking.
- Video/Online Appointments: High attendance rates with very low DNA rates and a moderate percentage of unknown outcomes

<br>


### 4. Likelihood of Missing Appointments: from a combination of Sub-ICB, Staff type, Appointment type.

- To understand this in detail, we have generated a Correlation matrix between all the indicators under SNEE-ICB areas.
- Correlation between variables signifies the degree and direction of the relationship between them. It measures how changes in one variable correspond to changes in another.
Correlation is measured on a scale from -1 to 1:
- Close to 1 shows a strong positive relationship: both variables move in the same direction or increase together.
- Close to -1 indicates a strong negative relationship: the variables move in opposite directions, means as one variable goes up, the other tends to go down.
- Around 0 suggests a weak or no clear relationship between the variables.

<table> <tr> <th>Feature</th> <th>Coefficient</th> </tr> <tr> <td>Appointment Mode: Face-to-Face</td> <td>0.133321</td> </tr> <tr> <td>Appointment Mode: Unknown</td> <td>0.112205</td> </tr> <tr> <td>HCP Type: Other Practice Staff</td> <td>0.099106</td> </tr> <tr> <td>HCP Type: Unknown</td> <td>0.096461</td> </tr> <tr> <td>SUB ICB Location Code: 06L</td> <td>0.050065</td> </tr> <tr> <td>SUB ICB Location Code: 06T</td> <td>0.039058</td> </tr> <tr> <td>Appointment Mode: Video/Online</td> <td>-0.047138</td> </tr> <tr> <td>Appointment Mode: Home Visit</td> <td>-0.082667</td> </tr> <tr> <td>SUB ICB Location Code: 07K</td> <td>-0.090500</td> </tr> <tr> <td>Appointment Mode: Telephone</td> <td>-0.117008</td> </tr> <tr> <td>HCP Type: GP</td> <td>-0.175618</td> </tr> </table>

- In summary, **Appointment mode:Face-to-Face/Unknown**, **HCP Type: Unkown/Other practice staff**, and specific location codes **like '06L'** have **positive correlations** with **DNA** appointments, indicating that these factors increase the chances of appointment being missed. 
- While **HCP Type:GPs**, **Appointment mode: home visits/telephone**, and specific location codes **like '07K'** have weak negative correlations, therefore these factors will decrease the chances of appointment being missed
<br><br>


### 5. Creating YAML for results

Finally, the results were processed into a YAML file for the simulation application, providing proportions of DNA appointments by sub-ICB areas, HCP types, and appointment modes.
- code "06L": Ipswich & East Suffolk, "07K": West Suffolk, "06T": North East Essex, corresponds to sub-areas under SNEE-ICB.
```yaml
00L:
  GP:
    Face-to-Face: 0.0232
    Home Visit: 0.0153
    Telephone: 0.0096
    Unknown: 0.0418
    Video/Online: 0.0129
  Other Practice staff:
    Face-to-Face: 0.0587
    Home Visit: 0.0177
    Telephone: 0.0254
    Unknown: 0.0393
    Video/Online: 0.023
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.008
    Telephone: 0.0291
    Unknown: 0.02
00N:
  GP:
    Face-to-Face: 0.032
    Home Visit: 0.0231
    Telephone: 0.0247
    Unknown: 0.0034
    Video/Online: 0.0323
  Other Practice staff:
    Face-to-Face: 0.0605
    Home Visit: 0.0354
    Telephone: 0.0456
    Unknown: 0.0291
    Video/Online: 0.0029
  Unknown:
    Face-to-Face: 0.0012
    Home Visit: 0.0713
    Telephone: 0.03
    Video/Online: 0.0291
00P:
  GP:
    Face-to-Face: 0.0447
    Home Visit: 0.0172
    Telephone: 0.0201
    Unknown: 0.013
    Video/Online: 0.0005
  Other Practice staff:
    Face-to-Face: 0.0734
    Home Visit: 0.018
    Telephone: 0.0512
    Unknown: 0.0023
    Video/Online: 0.005
  Unknown:
    Face-to-Face: 0.0026
    Home Visit: 0.0082
    Telephone: 0.0738
    Unknown: 0.0291
    Video/Online: 0.0291
00Q:
  GP:
    Face-to-Face: 0.0432
    Home Visit: 0.0072
    Telephone: 0.0256
    Unknown: 0.0291
    Video/Online: 0.0034
  Other Practice staff:
    Face-to-Face: 0.0831
    Home Visit: 0.0348
    Telephone: 0.0608
    Unknown: 0.0139
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0052
    Home Visit: 0.0076
    Telephone: 0.0291
00R:
  GP:
    Face-to-Face: 0.0526
    Home Visit: 0.0089
    Telephone: 0.0317
    Unknown: 0.0065
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0905
    Home Visit: 0.0405
    Telephone: 0.0473
    Unknown: 0.0006
    Video/Online: 0.0071
  Unknown:
    Face-to-Face: 0.0046
    Home Visit: 0.0261
    Telephone: 0.0416
    Unknown: 0.0291
00T:
  GP:
    Face-to-Face: 0.0515
    Home Visit: 0.0138
    Telephone: 0.0401
    Unknown: 0.0419
    Video/Online: 0.0025
  Other Practice staff:
    Face-to-Face: 0.0943
    Home Visit: 0.042
    Telephone: 0.0594
    Unknown: 0.0499
    Video/Online: 0.0456
  Unknown:
    Face-to-Face: 0.0021
    Home Visit: 0.1316
    Telephone: 0.0221
    Unknown: 0.019
    Video/Online: 0.0291
00V:
  GP:
    Face-to-Face: 0.049
    Home Visit: 0.0113
    Telephone: 0.0263
    Unknown: 0.022
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0778
    Home Visit: 0.0151
    Telephone: 0.0289
    Unknown: 0.0042
    Video/Online: 0.0075
  Unknown:
    Face-to-Face: 0.0173
    Home Visit: 0.0095
    Telephone: 0.0013
    Unknown: 0.0291
00X:
  GP:
    Face-to-Face: 0.0348
    Home Visit: 0.0102
    Telephone: 0.0256
    Unknown: 0.0291
    Video/Online: 0.1181
  Other Practice staff:
    Face-to-Face: 0.0635
    Home Visit: 0.0199
    Telephone: 0.0556
    Unknown: 0.1377
    Video/Online: 0.0009
  Unknown:
    Face-to-Face: 0.0555
    Home Visit: 0.0092
    Telephone: 0.0091
    Unknown: 0.0291
    Video/Online: 0.0291
00Y:
  GP:
    Face-to-Face: 0.0508
    Home Visit: 0.0088
    Telephone: 0.0226
    Unknown: 0.0026
    Video/Online: 0.0002
  Other Practice staff:
    Face-to-Face: 0.0889
    Home Visit: 0.0414
    Telephone: 0.0543
    Unknown: 0.0063
    Video/Online: 0.0007
  Unknown:
    Face-to-Face: 0.0008
    Home Visit: 0.0165
    Telephone: 0.0291
    Unknown: 0.0291
    Video/Online: 0.0291
01A:
  GP:
    Face-to-Face: 0.0416
    Home Visit: 0.0209
    Telephone: 0.0313
    Unknown: 0.0033
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.078
    Home Visit: 0.0483
    Telephone: 0.0595
    Unknown: 0.0036
    Video/Online: 0.0022
  Unknown:
    Face-to-Face: 0.0034
    Home Visit: 0.0093
    Telephone: 0.0098
    Unknown: 0.0291
    Video/Online: 0.0291
01D:
  GP:
    Face-to-Face: 0.0473
    Home Visit: 0.0105
    Telephone: 0.0287
    Unknown: 0.0291
    Video/Online: 0.0036
  Other Practice staff:
    Face-to-Face: 0.0937
    Home Visit: 0.0287
    Telephone: 0.0926
    Unknown: 0.1128
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0012
    Home Visit: 0.0139
    Telephone: 0.0386
    Unknown: 0.0291
    Video/Online: 0.0291
01E:
  GP:
    Face-to-Face: 0.0386
    Home Visit: 0.0054
    Telephone: 0.0194
    Unknown: 0.0291
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0716
    Home Visit: 0.0154
    Telephone: 0.0622
    Unknown: 0.0032
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0769
    Video/Online: 0.0291
01F:
  GP:
    Face-to-Face: 0.0357
    Home Visit: 0.0141
    Telephone: 0.0403
    Unknown: 0.0077
    Video/Online: 0.0012
  Other Practice staff:
    Face-to-Face: 0.0782
    Home Visit: 0.0255
    Telephone: 0.0874
    Unknown: 0.0584
    Video/Online: 0.0071
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0091
    Telephone: 0.0497
    Unknown: 0.0291
    Video/Online: 0.0291
01G:
  GP:
    Face-to-Face: 0.0603
    Home Visit: 0.0092
    Telephone: 0.0278
    Unknown: 0.0039
    Video/Online: 0.0014
  Other Practice staff:
    Face-to-Face: 0.0968
    Home Visit: 0.0583
    Telephone: 0.0608
    Unknown: 0.0116
    Video/Online: 0.0016
  Unknown:
    Face-to-Face: 0.0009
    Home Visit: 0.0161
    Telephone: 0.0046
    Unknown: 0.0291
    Video/Online: 0.0291
01H:
  GP:
    Face-to-Face: 0.0289
    Home Visit: 0.0087
    Telephone: 0.0249
    Unknown: 0.0064
    Video/Online: 0.0004
  Other Practice staff:
    Face-to-Face: 0.0568
    Home Visit: 0.0176
    Telephone: 0.0444
    Unknown: 0.0039
    Video/Online: 0.001
  Unknown:
    Face-to-Face: 0.0048
    Home Visit: 0.0096
    Telephone: 0.0139
    Unknown: 0.0291
    Video/Online: 0.0291
01J:
  GP:
    Face-to-Face: 0.0404
    Home Visit: 0.0173
    Telephone: 0.0265
    Unknown: 0.0053
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0959
    Home Visit: 0.0271
    Telephone: 0.0614
    Unknown: 0.0014
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.9435
    Home Visit: 0.0104
    Telephone: 0.0044
    Unknown: 0.0291
01K:
  GP:
    Face-to-Face: 0.0359
    Home Visit: 0.009
    Telephone: 0.0303
    Unknown: 0.0159
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0655
    Home Visit: 0.0183
    Telephone: 0.0562
    Unknown: 0.0052
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0019
    Home Visit: 0.0182
    Telephone: 0.032
    Unknown: 0.0291
    Video/Online: 0.0291
01T:
  GP:
    Face-to-Face: 0.0329
    Home Visit: 0.0091
    Telephone: 0.0197
    Unknown: 0.024
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0804
    Home Visit: 0.0191
    Telephone: 0.052
    Unknown: 0.034
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0455
    Home Visit: 0.0333
    Telephone: 0.0954
    Unknown: 0.0291
    Video/Online: 0.0291
01V:
  GP:
    Face-to-Face: 0.0274
    Home Visit: 0.0114
    Telephone: 0.0167
    Unknown: 0.259
    Video/Online: 0.0003
  Other Practice staff:
    Face-to-Face: 0.0607
    Home Visit: 0.0152
    Telephone: 0.0458
    Unknown: 0.25
    Video/Online: 0.001
  Unknown:
    Face-to-Face: 0.0007
    Home Visit: 0.0071
    Telephone: 0.0057
    Unknown: 0.0291
    Video/Online: 0.0291
01W:
  GP:
    Face-to-Face: 0.0403
    Home Visit: 0.0097
    Telephone: 0.024
    Unknown: 0.0085
    Video/Online: 0.0006
  Other Practice staff:
    Face-to-Face: 0.0726
    Home Visit: 0.0555
    Telephone: 0.0588
    Unknown: 0.0291
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0202
    Home Visit: 0.0138
    Telephone: 0.0138
    Unknown: 0.0291
    Video/Online: 0.0291
01X:
  GP:
    Face-to-Face: 0.0373
    Home Visit: 0.0115
    Telephone: 0.0267
    Unknown: 0.009
    Video/Online: 0.0003
  Other Practice staff:
    Face-to-Face: 0.0726
    Home Visit: 0.0181
    Telephone: 0.0619
    Unknown: 0.0052
    Video/Online: 0.0004
  Unknown:
    Face-to-Face: 0.0104
    Home Visit: 0.0201
    Telephone: 0.1131
    Unknown: 0.0291
    Video/Online: 0.0291
01Y:
  GP:
    Face-to-Face: 0.0576
    Home Visit: 0.0121
    Telephone: 0.0331
    Unknown: 0.0285
    Video/Online: 0.0045
  Other Practice staff:
    Face-to-Face: 0.0881
    Home Visit: 0.0527
    Telephone: 0.0645
    Unknown: 0.0335
    Video/Online: 0.0007
  Unknown:
    Face-to-Face: 0.0169
    Home Visit: 0.0102
    Telephone: 0.0291
    Unknown: 0.0262
02A:
  GP:
    Face-to-Face: 0.0477
    Home Visit: 0.0114
    Telephone: 0.0299
    Unknown: 0.007
    Video/Online: 0.02
  Other Practice staff:
    Face-to-Face: 0.0878
    Home Visit: 0.0365
    Telephone: 0.0575
    Unknown: 0.0068
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.2615
    Home Visit: 0.0049
    Telephone: 0.0363
    Video/Online: 0.0291
02E:
  GP:
    Face-to-Face: 0.0206
    Home Visit: 0.0329
    Telephone: 0.0113
    Unknown: 0.0275
    Video/Online: 0.0191
  Other Practice staff:
    Face-to-Face: 0.0554
    Home Visit: 0.047
    Telephone: 0.0257
    Unknown: 0.0207
    Video/Online: 0.0181
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0667
    Telephone: 0.0291
    Unknown: 0.0201
02G:
  GP:
    Face-to-Face: 0.0232
    Home Visit: 0.0171
    Telephone: 0.0271
    Unknown: 0.0291
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0509
    Home Visit: 0.0369
    Telephone: 0.0504
    Unknown: 0.0291
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0199
    Telephone: 0.0291
    Unknown: 0.0291
02H:
  GP:
    Face-to-Face: 0.0465
    Home Visit: 0.0134
    Telephone: 0.022
    Unknown: 0.0105
    Video/Online: 0.0111
  Other Practice staff:
    Face-to-Face: 0.0782
    Home Visit: 0.0201
    Telephone: 0.0405
    Unknown: 0.0189
    Video/Online: 0.0067
  Unknown:
    Face-to-Face: 0.0254
    Home Visit: 0.016
    Telephone: 0.0291
    Unknown: 0.0301
02M:
  GP:
    Face-to-Face: 0.0321
    Home Visit: 0.0096
    Telephone: 0.0131
    Unknown: 0.0291
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0523
    Home Visit: 0.0212
    Telephone: 0.093
    Unknown: 0.0064
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0006
    Home Visit: 0.0207
    Telephone: 0.0022
    Unknown: 0.0291
    Video/Online: 0.0291
02P:
  GP:
    Face-to-Face: 0.0253
    Home Visit: 0.0446
    Telephone: 0.0162
    Unknown: 0.0601
    Video/Online: 0.0397
  Other Practice staff:
    Face-to-Face: 0.056
    Home Visit: 0.0199
    Telephone: 0.025
    Unknown: 0.0564
    Video/Online: 0.0051
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0291
    Telephone: 0.011
    Unknown: 0.0273
02Q:
  GP:
    Face-to-Face: 0.0272
    Home Visit: 0.0156
    Telephone: 0.0114
    Unknown: 0.0283
    Video/Online: 0.0064
  Other Practice staff:
    Face-to-Face: 0.0543
    Home Visit: 0.0249
    Telephone: 0.0154
    Unknown: 0.0463
    Video/Online: 0.0046
  Unknown:
    Unknown: 0.0129
02T:
  GP:
    Face-to-Face: 0.0258
    Home Visit: 0.0085
    Telephone: 0.0105
    Unknown: 0.0336
    Video/Online: 0.0202
  Other Practice staff:
    Face-to-Face: 0.057
    Home Visit: 0.0408
    Telephone: 0.0208
    Unknown: 0.0246
    Video/Online: 0.0071
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0291
    Unknown: 0.0201
    Video/Online: 0.0291
02X:
  GP:
    Face-to-Face: 0.0446
    Home Visit: 0.0128
    Telephone: 0.0202
    Unknown: 0.0207
    Video/Online: 0.0204
  Other Practice staff:
    Face-to-Face: 0.0635
    Home Visit: 0.0365
    Telephone: 0.0247
    Unknown: 0.0237
    Video/Online: 0.005
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0328
    Telephone: 0.0311
    Unknown: 0.0285
    Video/Online: 0.0291
02Y:
  GP:
    Face-to-Face: 0.0251
    Home Visit: 0.0223
    Telephone: 0.0076
    Unknown: 0.0138
    Video/Online: 0.0072
  Other Practice staff:
    Face-to-Face: 0.0496
    Home Visit: 0.026
    Telephone: 0.0198
    Unknown: 0.0134
    Video/Online: 0.0023
  Unknown:
    Face-to-Face: 0.0005
    Home Visit: 0.0291
    Telephone: 0.0016
    Unknown: 0.0159
    Video/Online: 0.0291
03F:
  GP:
    Face-to-Face: 0.0364
    Home Visit: 0.0848
    Telephone: 0.0085
    Unknown: 0.0684
    Video/Online: 0.0058
  Other Practice staff:
    Face-to-Face: 0.0844
    Home Visit: 0.0329
    Telephone: 0.0231
    Unknown: 0.045
    Video/Online: 0.0225
  Unknown:
    Face-to-Face: 0.0006
    Home Visit: 0.0263
    Telephone: 0.0327
    Unknown: 0.0235
    Video/Online: 0.0008
03H:
  GP:
    Face-to-Face: 0.0178
    Home Visit: 0.0205
    Telephone: 0.0098
    Unknown: 0.0227
    Video/Online: 0.0108
  Other Practice staff:
    Face-to-Face: 0.0454
    Home Visit: 0.0133
    Telephone: 0.0074
    Unknown: 0.0165
    Video/Online: 0.0013
  Unknown:
    Face-to-Face: 0.0015
    Telephone: 0.0094
    Unknown: 0.0181
03K:
  GP:
    Face-to-Face: 0.0242
    Home Visit: 0.0192
    Telephone: 0.0115
    Unknown: 0.0196
    Video/Online: 0.0008
  Other Practice staff:
    Face-to-Face: 0.0419
    Home Visit: 0.0192
    Telephone: 0.0147
    Unknown: 0.0213
    Video/Online: 0.0041
  Unknown:
    Unknown: 0.016
03L:
  GP:
    Face-to-Face: 0.0285
    Home Visit: 0.0162
    Telephone: 0.0102
    Unknown: 0.0212
    Video/Online: 0.0037
  Other Practice staff:
    Face-to-Face: 0.0617
    Home Visit: 0.041
    Telephone: 0.0211
    Unknown: 0.0344
    Video/Online: 0.0251
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0136
    Telephone: 0.0291
    Unknown: 0.0178
03N:
  GP:
    Face-to-Face: 0.0334
    Home Visit: 0.0151
    Telephone: 0.0108
    Unknown: 0.034
    Video/Online: 0.0289
  Other Practice staff:
    Face-to-Face: 0.0692
    Home Visit: 0.033
    Telephone: 0.0128
    Unknown: 0.055
    Video/Online: 0.0075
  Unknown:
    Face-to-Face: 0.0219
    Home Visit: 0.0324
    Telephone: 0.0249
    Unknown: 0.0209
    Video/Online: 0.0291
03Q:
  GP:
    Face-to-Face: 0.0403
    Home Visit: 0.0119
    Telephone: 0.0103
    Unknown: 0.0211
    Video/Online: 0.0152
  Other Practice staff:
    Face-to-Face: 0.0438
    Home Visit: 0.0258
    Telephone: 0.0202
    Unknown: 0.0279
    Video/Online: 0.0238
  Unknown:
    Face-to-Face: 0.0196
    Telephone: 0.0291
    Unknown: 0.0073
03R:
  GP:
    Face-to-Face: 0.0235
    Home Visit: 0.0144
    Telephone: 0.0088
    Unknown: 0.0484
    Video/Online: 0.0071
  Other Practice staff:
    Face-to-Face: 0.0551
    Home Visit: 0.0244
    Telephone: 0.0077
    Unknown: 0.0359
    Video/Online: 0.0098
  Unknown:
    Unknown: 0.0187
03W:
  GP:
    Face-to-Face: 0.0301
    Home Visit: 0.03
    Telephone: 0.0067
    Unknown: 0.0651
    Video/Online: 0.0089
  Other Practice staff:
    Face-to-Face: 0.0491
    Home Visit: 0.0273
    Telephone: 0.0067
    Unknown: 0.0364
    Video/Online: 0.0117
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.2557
    Telephone: 0.0291
    Unknown: 0.0164
04C:
  GP:
    Face-to-Face: 0.0324
    Home Visit: 0.0398
    Telephone: 0.0099
    Unknown: 0.0204
    Video/Online: 0.0309
  Other Practice staff:
    Face-to-Face: 0.0782
    Home Visit: 0.0678
    Telephone: 0.011
    Unknown: 0.0299
    Video/Online: 0.0122
  Unknown:
    Unknown: 0.0368
04V:
  GP:
    Face-to-Face: 0.0261
    Home Visit: 0.0311
    Telephone: 0.0096
    Unknown: 0.0345
    Video/Online: 0.0089
  Other Practice staff:
    Face-to-Face: 0.0508
    Home Visit: 0.0226
    Telephone: 0.0224
    Unknown: 0.0197
    Video/Online: 0.0186
  Unknown:
    Unknown: 0.0168
04Y:
  GP:
    Face-to-Face: 0.0344
    Home Visit: 0.0038
    Telephone: 0.0149
    Unknown: 0.0014
    Video/Online: 0.0163
  Other Practice staff:
    Face-to-Face: 0.0571
    Home Visit: 0.0155
    Telephone: 0.0743
    Unknown: 0.0057
    Video/Online: 0.046
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0174
    Telephone: 0.0907
    Video/Online: 0.0029
05D:
  GP:
    Face-to-Face: 0.0285
    Home Visit: 0.0051
    Telephone: 0.0226
    Unknown: 0.0013
    Video/Online: 0.0025
  Other Practice staff:
    Face-to-Face: 0.0585
    Home Visit: 0.0484
    Telephone: 0.0733
    Unknown: 0.0073
    Video/Online: 0.0006
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0423
    Telephone: 0.0007
    Unknown: 0.0159
05G:
  GP:
    Face-to-Face: 0.0259
    Home Visit: 0.0114
    Telephone: 0.0175
    Unknown: 0.0153
    Video/Online: 0.0007
  Other Practice staff:
    Face-to-Face: 0.0566
    Home Visit: 0.015
    Telephone: 0.0474
    Unknown: 0.0083
    Video/Online: 0.0029
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0198
    Telephone: 0.1292
    Unknown: 0.0131
    Video/Online: 0.0291
05Q:
  GP:
    Face-to-Face: 0.0437
    Home Visit: 0.0119
    Telephone: 0.022
    Unknown: 0.0291
    Video/Online: 0.0012
  Other Practice staff:
    Face-to-Face: 0.0562
    Home Visit: 0.0158
    Telephone: 0.0548
    Unknown: 0.0085
    Video/Online: 0.0004
  Unknown:
    Face-to-Face: 0.0052
    Home Visit: 0.2673
    Telephone: 0.1429
    Unknown: 0.0291
    Video/Online: 0.0291
05V:
  GP:
    Face-to-Face: 0.0449
    Home Visit: 0.0114
    Telephone: 0.0255
    Unknown: 0.0291
    Video/Online: 0.0291
  Other Practice staff:
    Face-to-Face: 0.0626
    Home Visit: 0.0306
    Telephone: 0.046
    Unknown: 0.0291
    Video/Online: 0.0291
  Unknown:
    Face-to-Face: 0.0021
    Home Visit: 0.0104
    Telephone: 0.0291
    Unknown: 0.0291
    Video/Online: 0.0291
05W:
  GP:
    Face-to-Face: 0.0458
    Home Visit: 0.0075
    Telephone: 0.0231
    Unknown: 0.0543
    Video/Online: 0.002
  Other Practice staff:
    Face-to-Face: 0.0859
    Home Visit: 0.0151
    Telephone: 0.0636
    Unknown: 0.0038
    Video/Online: 0.002
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0134
    Telephone: 0.0062
    Unknown: 0.0129
    Video/Online: 0.0291
06H:
  GP:
    Face-to-Face: 0.0306
    Home Visit: 0.0206
    Telephone: 0.0054
    Unknown: 0.03
    Video/Online: 0.0106
  Other Practice staff:
    Face-to-Face: 0.0564
    Home Visit: 0.0183
    Telephone: 0.0151
    Unknown: 0.0379
    Video/Online: 0.0123
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0241
    Telephone: 0.0342
    Unknown: 0.0151
    Video/Online: 0.0291
06K:
  GP:
    Face-to-Face: 0.0266
    Home Visit: 0.015
    Telephone: 0.0061
    Unknown: 0.0133
    Video/Online: 0.0096
  Other Practice staff:
    Face-to-Face: 0.0585
    Home Visit: 0.0517
    Telephone: 0.0096
    Unknown: 0.041
    Video/Online: 0.0124
  Unknown:
    Home Visit: 0.0168
    Telephone: 0.0291
    Unknown: 0.0135
06L:
  GP:
    Face-to-Face: 0.0164
    Home Visit: 0.0073
    Telephone: 0.0019
    Unknown: 0.0221
    Video/Online: 0.0146
  Other Practice staff:
    Face-to-Face: 0.0457
    Home Visit: 0.0307
    Telephone: 0.0051
    Unknown: 0.0383
    Video/Online: 0.0295
  Unknown:
    Unknown: 0.0205
06N:
  GP:
    Face-to-Face: 0.0376
    Home Visit: 0.0109
    Telephone: 0.0218
    Unknown: 0.0073
    Video/Online: 0.0008
  Other Practice staff:
    Face-to-Face: 0.0714
    Home Visit: 0.0144
    Telephone: 0.0551
    Unknown: 0.0043
    Video/Online: 0.002
  Unknown:
    Face-to-Face: 0.0021
    Home Visit: 0.027
    Telephone: 0.0052
    Unknown: 0.0065
    Video/Online: 0.0291
06Q:
  GP:
    Face-to-Face: 0.0227
    Home Visit: 0.0118
    Telephone: 0.0081
    Unknown: 0.0269
    Video/Online: 0.0221
  Other Practice staff:
    Face-to-Face: 0.0469
    Home Visit: 0.0179
    Telephone: 0.0151
    Unknown: 0.0292
    Video/Online: 0.0423
  Unknown:
    Unknown: 0.0207
06T:
  GP:
    Face-to-Face: 0.0276
    Home Visit: 0.0219
    Telephone: 0.0124
    Unknown: 0.0352
    Video/Online: 0.007
  Other Practice staff:
    Face-to-Face: 0.051
    Home Visit: 0.0248
    Telephone: 0.0246
    Unknown: 0.0254
    Video/Online: 0.0221
  Unknown:
    Face-to-Face: 0.1155
    Home Visit: 0.0098
    Telephone: 0.0408
    Unknown: 0.025
    Video/Online: 0.0291
07G:
  GP:
    Face-to-Face: 0.0248
    Home Visit: 0.1574
    Telephone: 0.0066
    Unknown: 0.0309
    Video/Online: 0.0091
  Other Practice staff:
    Face-to-Face: 0.0457
    Home Visit: 0.0291
    Telephone: 0.0061
    Unknown: 0.0139
    Video/Online: 0.0019
  Unknown:
    Unknown: 0.0229
07H:
  GP:
    Face-to-Face: 0.0297
    Home Visit: 0.0336
    Telephone: 0.0091
    Unknown: 0.0186
    Video/Online: 0.1359
  Other Practice staff:
    Face-to-Face: 0.0643
    Home Visit: 0.0173
    Telephone: 0.0075
    Unknown: 0.0125
    Video/Online: 0.1429
  Unknown:
    Face-to-Face: 0.0291
    Unknown: 0.0147
07K:
  GP:
    Face-to-Face: 0.0221
    Home Visit: 0.0166
    Telephone: 0.0079
    Unknown: 0.0182
    Video/Online: 0.0019
  Other Practice staff:
    Face-to-Face: 0.0422
    Home Visit: 0.0365
    Telephone: 0.0131
    Unknown: 0.0256
    Video/Online: 0.0027
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0224
    Telephone: 0.0291
    Unknown: 0.0148
09D:
  GP:
    Face-to-Face: 0.036
    Home Visit: 0.0698
    Telephone: 0.0139
    Unknown: 0.0196
    Video/Online: 0.0208
  Other Practice staff:
    Face-to-Face: 0.0747
    Home Visit: 0.0915
    Telephone: 0.0145
    Unknown: 0.0335
    Video/Online: 0.0075
  Unknown:
    Face-to-Face: 0.0689
    Home Visit: 0.0042
    Telephone: 0.0866
    Unknown: 0.0245
10Q:
  GP:
    Face-to-Face: 0.0385
    Home Visit: 0.0235
    Telephone: 0.0211
    Unknown: 0.0004
    Video/Online: 0.0008
  Other Practice staff:
    Face-to-Face: 0.0679
    Home Visit: 0.036
    Telephone: 0.0396
    Unknown: 0.0037
    Video/Online: 0.0007
  Unknown:
    Face-to-Face: 0.2035
    Home Visit: 0.0313
    Telephone: 0.0057
    Unknown: 0.0291
    Video/Online: 0.002
10R:
  GP:
    Face-to-Face: 0.0344
    Home Visit: 0.0291
    Telephone: 0.0019
    Unknown: 0.0486
    Video/Online: 0.011
  Other Practice staff:
    Face-to-Face: 0.0737
    Home Visit: 0.0228
    Telephone: 0.0093
    Unknown: 0.0452
    Video/Online: 0.0037
  Unknown:
    Unknown: 0.0137
11J:
  GP:
    Face-to-Face: 0.0275
    Home Visit: 0.0242
    Telephone: 0.0046
    Unknown: 0.0246
    Video/Online: 0.0088
  Other Practice staff:
    Face-to-Face: 0.0499
    Home Visit: 0.033
    Telephone: 0.0077
    Unknown: 0.0461
    Video/Online: 0.0242
  Unknown:
    Unknown: 0.0137
11M:
  GP:
    Face-to-Face: 0.032
    Home Visit: 0.0313
    Telephone: 0.0063
    Unknown: 0.0131
    Video/Online: 0.0261
  Other Practice staff:
    Face-to-Face: 0.0492
    Home Visit: 0.0299
    Telephone: 0.0077
    Unknown: 0.0181
    Video/Online: 0.0229
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0694
    Telephone: 0.0326
    Unknown: 0.0132
    Video/Online: 0.0291
11N:
  GP:
    Face-to-Face: 0.0348
    Home Visit: 0.0347
    Telephone: 0.0106
    Unknown: 0.0537
    Video/Online: 0.0026
  Other Practice staff:
    Face-to-Face: 0.0567
    Home Visit: 0.03
    Telephone: 0.0375
    Unknown: 0.0336
    Video/Online: 0.0052
  Unknown:
    Face-to-Face: 0.0099
    Home Visit: 0.0145
    Telephone: 0.0399
    Unknown: 0.0104
    Video/Online: 0.0291
11X:
  GP:
    Face-to-Face: 0.0379
    Home Visit: 0.0217
    Telephone: 0.0273
    Unknown: 0.0177
    Video/Online: 0.0007
  Other Practice staff:
    Face-to-Face: 0.0607
    Home Visit: 0.021
    Telephone: 0.0556
    Unknown: 0.0296
    Video/Online: 0.0008
  Unknown:
    Face-to-Face: 0.0265
    Home Visit: 0.0141
    Telephone: 0.0102
    Unknown: 0.0291
    Video/Online: 0.0291
12F:
  GP:
    Face-to-Face: 0.044
    Home Visit: 0.0063
    Telephone: 0.0285
    Unknown: 0.0032
    Video/Online: 0.0005
  Other Practice staff:
    Face-to-Face: 0.0843
    Home Visit: 0.0254
    Telephone: 0.0853
    Unknown: 0.0009
    Video/Online: 0.0002
  Unknown:
    Face-to-Face: 0.0004
    Home Visit: 0.0126
    Telephone: 0.0205
    Unknown: 0.0291
    Video/Online: 0.0291
13T:
  GP:
    Face-to-Face: 0.0392
    Home Visit: 0.0514
    Telephone: 0.0142
    Unknown: 0.0131
    Video/Online: 0.0064
  Other Practice staff:
    Face-to-Face: 0.0733
    Home Visit: 0.0843
    Telephone: 0.0632
    Unknown: 0.0272
    Video/Online: 0.0081
  Unknown:
    Face-to-Face: 0.0017
    Home Visit: 0.0128
    Telephone: 0.0258
    Unknown: 0.0132
    Video/Online: 0.0291
14L:
  GP:
    Face-to-Face: 0.0638
    Home Visit: 0.0284
    Telephone: 0.0343
    Unknown: 0.0064
    Video/Online: 0.0004
  Other Practice staff:
    Face-to-Face: 0.1139
    Home Visit: 0.0585
    Telephone: 0.0669
    Unknown: 0.0138
    Video/Online: 0.0004
  Unknown:
    Face-to-Face: 0.0182
    Home Visit: 0.0129
    Telephone: 0.0157
    Unknown: 0.0291
    Video/Online: 0.0291
14Y:
  GP:
    Face-to-Face: 0.0308
    Home Visit: 0.0954
    Telephone: 0.0241
    Unknown: 0.0006
    Video/Online: 0.0039
  Other Practice staff:
    Face-to-Face: 0.0642
    Home Visit: 0.0188
    Telephone: 0.0373
    Unknown: 0.0131
    Video/Online: 0.0083
  Unknown:
    Face-to-Face: 0.0018
    Home Visit: 0.0144
    Telephone: 0.0037
    Unknown: 0.0287
15A:
  GP:
    Face-to-Face: 0.0387
    Home Visit: 0.0071
    Telephone: 0.0183
    Unknown: 0.0377
    Video/Online: 0.0004
  Other Practice staff:
    Face-to-Face: 0.0563
    Home Visit: 0.0158
    Telephone: 0.0482
    Unknown: 0.0537
    Video/Online: 0.0019
  Unknown:
    Face-to-Face: 0.0078
    Home Visit: 0.0161
    Telephone: 0.0109
    Unknown: 0.017
    Video/Online: 0.122
15C:
  GP:
    Face-to-Face: 0.0466
    Home Visit: 0.0281
    Telephone: 0.0218
    Unknown: 0.019
    Video/Online: 0.0005
  Other Practice staff:
    Face-to-Face: 0.0722
    Home Visit: 0.0161
    Telephone: 0.053
    Unknown: 0.0144
    Video/Online: 0.0022
  Unknown:
    Face-to-Face: 0.0009
    Home Visit: 0.0119
    Telephone: 0.0315
    Unknown: 0.0291
    Video/Online: 0.0291
15E:
  GP:
    Face-to-Face: 0.047
    Home Visit: 0.0325
    Telephone: 0.021
    Unknown: 0.0256
    Video/Online: 0.013
  Other Practice staff:
    Face-to-Face: 0.1022
    Home Visit: 0.0541
    Telephone: 0.0459
    Unknown: 0.053
    Video/Online: 0.0138
  Unknown:
    Face-to-Face: 0.0019
    Home Visit: 0.4797
    Telephone: 0.0116
    Unknown: 0.0312
    Video/Online: 0.0291
15F:
  GP:
    Face-to-Face: 0.0371
    Home Visit: 0.0128
    Telephone: 0.0131
    Unknown: 0.0295
    Video/Online: 0.0053
  Other Practice staff:
    Face-to-Face: 0.071
    Home Visit: 0.0319
    Telephone: 0.0206
    Unknown: 0.0434
    Video/Online: 0.014
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0204
    Telephone: 0.0183
    Unknown: 0.0321
15M:
  GP:
    Face-to-Face: 0.0281
    Home Visit: 0.0283
    Telephone: 0.01
    Unknown: 0.0119
    Video/Online: 0.0042
  Other Practice staff:
    Face-to-Face: 0.0523
    Home Visit: 0.0235
    Telephone: 0.0152
    Unknown: 0.0281
    Video/Online: 0.0082
  Unknown:
    Face-to-Face: 0.0298
    Home Visit: 0.0181
    Unknown: 0.0187
    Video/Online: 0.0291
15N:
  GP:
    Face-to-Face: 0.0316
    Home Visit: 0.018
    Telephone: 0.0125
    Unknown: 0.0137
    Video/Online: 0.0063
  Other Practice staff:
    Face-to-Face: 0.0521
    Home Visit: 0.03
    Telephone: 0.0179
    Unknown: 0.0298
    Video/Online: 0.0131
  Unknown:
    Face-to-Face: 0.0035
    Home Visit: 0.006
    Telephone: 0.0435
    Unknown: 0.012
16C:
  GP:
    Face-to-Face: 0.0328
    Home Visit: 0.0274
    Telephone: 0.0096
    Unknown: 0.0308
    Video/Online: 0.0058
  Other Practice staff:
    Face-to-Face: 0.0654
    Home Visit: 0.0337
    Telephone: 0.0138
    Unknown: 0.0463
    Video/Online: 0.0118
  Unknown:
    Face-to-Face: 0.001
    Home Visit: 0.008
    Telephone: 0.0154
    Unknown: 0.0252
    Video/Online: 0.0291
18C:
  GP:
    Face-to-Face: 0.0338
    Home Visit: 0.012
    Telephone: 0.0187
    Unknown: 0.0119
    Video/Online: 0.0013
  Other Practice staff:
    Face-to-Face: 0.0582
    Home Visit: 0.0113
    Telephone: 0.0566
    Unknown: 0.0057
    Video/Online: 0.0009
  Unknown:
    Face-to-Face: 0.0016
    Home Visit: 0.003
    Telephone: 0.0504
    Unknown: 0.0291
    Video/Online: 0.0291
26A:
  GP:
    Face-to-Face: 0.0288
    Home Visit: 0.0159
    Telephone: 0.0058
    Unknown: 0.0253
    Video/Online: 0.0245
  Other Practice staff:
    Face-to-Face: 0.0494
    Home Visit: 0.029
    Telephone: 0.0186
    Unknown: 0.0369
    Video/Online: 0.021
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0062
    Telephone: 0.0291
    Unknown: 0.0134
27D:
  GP:
    Face-to-Face: 0.0381
    Home Visit: 0.0589
    Telephone: 0.0297
    Unknown: 0.0194
    Video/Online: 0.0022
  Other Practice staff:
    Face-to-Face: 0.0705
    Home Visit: 0.0194
    Telephone: 0.0648
    Unknown: 0.023
    Video/Online: 0.0002
  Unknown:
    Face-to-Face: 0.0035
    Home Visit: 0.0133
    Telephone: 0.0204
    Unknown: 0.0291
    Video/Online: 0.0291
36J:
  GP:
    Face-to-Face: 0.0236
    Home Visit: 0.0161
    Telephone: 0.0079
    Unknown: 0.0197
    Video/Online: 0.0047
  Other Practice staff:
    Face-to-Face: 0.0545
    Home Visit: 0.0093
    Telephone: 0.0078
    Unknown: 0.0151
    Video/Online: 0.0052
  Unknown:
    Unknown: 0.0233
36L:
  GP:
    Face-to-Face: 0.0519
    Home Visit: 0.0155
    Telephone: 0.0241
    Unknown: 0.0229
    Video/Online: 0.0017
  Other Practice staff:
    Face-to-Face: 0.0933
    Home Visit: 0.0321
    Telephone: 0.063
    Unknown: 0.0244
    Video/Online: 0.0002
  Unknown:
    Face-to-Face: 0.0038
    Home Visit: 0.039
    Telephone: 0.0462
    Unknown: 0.0291
    Video/Online: 0.0291
42D:
  GP:
    Face-to-Face: 0.0279
    Home Visit: 0.0182
    Telephone: 0.0064
    Unknown: 0.016
    Video/Online: 0.0058
  Other Practice staff:
    Face-to-Face: 0.0463
    Home Visit: 0.0533
    Telephone: 0.0099
    Unknown: 0.0385
    Video/Online: 0.0059
  Unknown:
    Face-to-Face: 0.0044
    Home Visit: 0.0065
    Telephone: 0.0291
    Unknown: 0.0132
52R:
  GP:
    Face-to-Face: 0.0358
    Home Visit: 0.0217
    Telephone: 0.009
    Unknown: 0.066
    Video/Online: 0.0263
  Other Practice staff:
    Face-to-Face: 0.0653
    Home Visit: 0.0673
    Telephone: 0.0176
    Unknown: 0.0586
    Video/Online: 0.0254
  Unknown:
    Unknown: 0.0215
70F:
  GP:
    Face-to-Face: 0.0252
    Home Visit: 0.007
    Telephone: 0.0059
    Unknown: 0.0167
    Video/Online: 0.008
  Other Practice staff:
    Face-to-Face: 0.0498
    Home Visit: 0.0224
    Telephone: 0.016
    Unknown: 0.0219
    Video/Online: 0.0332
  Unknown:
    Face-to-Face: 0.0181
    Home Visit: 0.0241
    Telephone: 0.0291
    Unknown: 0.0116
    Video/Online: 0.0024
71E:
  GP:
    Face-to-Face: 0.0225
    Home Visit: 0.0217
    Telephone: 0.0072
    Unknown: 0.0191
    Video/Online: 0.0056
  Other Practice staff:
    Face-to-Face: 0.051
    Home Visit: 0.0264
    Telephone: 0.0148
    Unknown: 0.0438
    Video/Online: 0.0089
  Unknown:
    Face-to-Face: 0.0291
    Unknown: 0.0168
72Q:
  GP:
    Face-to-Face: 0.057
    Home Visit: 0.0168
    Telephone: 0.0312
    Unknown: 0.0145
    Video/Online: 0.0004
  Other Practice staff:
    Face-to-Face: 0.1107
    Home Visit: 0.0309
    Telephone: 0.0524
    Unknown: 0.0212
    Video/Online: 0.0021
  Unknown:
    Face-to-Face: 0.0003
    Home Visit: 0.0175
    Telephone: 0.0242
    Unknown: 0.0291
    Video/Online: 0.0291
78H:
  GP:
    Face-to-Face: 0.0279
    Home Visit: 0.0123
    Telephone: 0.0078
    Unknown: 0.0282
    Video/Online: 0.0077
  Other Practice staff:
    Face-to-Face: 0.0533
    Home Visit: 0.0294
    Telephone: 0.0139
    Unknown: 0.0298
    Video/Online: 0.0123
  Unknown:
    Face-to-Face: 0.0151
    Home Visit: 0.0152
    Telephone: 0.0155
    Unknown: 0.0137
    Video/Online: 0.0291
84H:
  GP:
    Face-to-Face: 0.0271
    Home Visit: 0.0339
    Telephone: 0.0102
    Unknown: 0.0237
    Video/Online: 0.0047
  Other Practice staff:
    Face-to-Face: 0.0511
    Home Visit: 0.029
    Telephone: 0.0124
    Unknown: 0.0389
    Video/Online: 0.0132
  Unknown:
    Telephone: 0.0291
    Unknown: 0.0163
91Q:
  GP:
    Face-to-Face: 0.0411
    Home Visit: 0.0198
    Telephone: 0.0162
    Unknown: 0.0066
    Video/Online: 0.0009
  Other Practice staff:
    Face-to-Face: 0.0661
    Home Visit: 0.0191
    Telephone: 0.051
    Unknown: 0.0139
    Video/Online: 0.0012
  Unknown:
    Face-to-Face: 0.0081
    Home Visit: 0.046
    Telephone: 0.0078
    Unknown: 0.0291
    Video/Online: 0.0291
92A:
  GP:
    Face-to-Face: 0.034
    Home Visit: 0.0178
    Telephone: 0.027
    Unknown: 0.0087
    Video/Online: 0.0001
  Other Practice staff:
    Face-to-Face: 0.0585
    Home Visit: 0.0254
    Telephone: 0.0417
    Unknown: 0.0106
    Video/Online: 0.0002
  Unknown:
    Face-to-Face: 0.0231
    Home Visit: 0.0269
    Telephone: 0.0324
    Unknown: 0.0145
    Video/Online: 0.0291
92G:
  GP:
    Face-to-Face: 0.0266
    Home Visit: 0.0117
    Telephone: 0.0036
    Unknown: 0.0259
    Video/Online: 0.01
  Other Practice staff:
    Face-to-Face: 0.0491
    Home Visit: 0.0183
    Telephone: 0.0082
    Unknown: 0.037
    Video/Online: 0.0142
  Unknown:
    Face-to-Face: 0.0291
    Telephone: 0.005
    Unknown: 0.0143
93C:
  GP:
    Face-to-Face: 0.0545
    Home Visit: 0.014
    Telephone: 0.0246
    Unknown: 0.0031
    Video/Online: 0.0015
  Other Practice staff:
    Face-to-Face: 0.1037
    Home Visit: 0.076
    Telephone: 0.0487
    Unknown: 0.0013
    Video/Online: 0.0011
  Unknown:
    Face-to-Face: 0.0088
    Home Visit: 0.0252
    Telephone: 0.0078
    Unknown: 0.0291
    Video/Online: 0.0291
97R:
  GP:
    Face-to-Face: 0.0308
    Home Visit: 0.0173
    Telephone: 0.0226
    Unknown: 0.0146
    Video/Online: 0.0024
  Other Practice staff:
    Face-to-Face: 0.0585
    Home Visit: 0.0252
    Telephone: 0.0519
    Unknown: 0.0043
    Video/Online: 0.0092
  Unknown:
    Face-to-Face: 0.037
    Home Visit: 0.0683
    Telephone: 0.0203
    Unknown: 0.0216
99A:
  GP:
    Face-to-Face: 0.0434
    Home Visit: 0.0132
    Telephone: 0.0333
    Unknown: 0.0245
    Video/Online: 0.0022
  Other Practice staff:
    Face-to-Face: 0.1079
    Home Visit: 0.0514
    Telephone: 0.0951
    Unknown: 0.0079
    Video/Online: 0.0022
  Unknown:
    Face-to-Face: 0.0056
    Home Visit: 0.01
    Telephone: 0.0488
    Unknown: 0.0291
    Video/Online: 0.0291
99C:
  GP:
    Face-to-Face: 0.0302
    Home Visit: 0.0207
    Telephone: 0.021
    Unknown: 0.0215
    Video/Online: 0.0041
  Other Practice staff:
    Face-to-Face: 0.0621
    Home Visit: 0.0385
    Telephone: 0.0386
    Unknown: 0.0136
    Video/Online: 0.0216
  Unknown:
    Face-to-Face: 0.0015
    Home Visit: 0.0145
    Telephone: 0.0532
    Unknown: 0.0202
    Video/Online: 0.0291
99E:
  GP:
    Face-to-Face: 0.0179
    Home Visit: 0.0132
    Telephone: 0.004
    Unknown: 0.0136
    Video/Online: 0.0104
  Other Practice staff:
    Face-to-Face: 0.0396
    Home Visit: 0.0054
    Telephone: 0.0043
    Unknown: 0.0201
    Video/Online: 0.0189
  Unknown:
    Unknown: 0.0163
99F:
  GP:
    Face-to-Face: 0.0246
    Home Visit: 0.0738
    Telephone: 0.0101
    Unknown: 0.0221
    Video/Online: 0.0057
  Other Practice staff:
    Face-to-Face: 0.0436
    Home Visit: 0.0485
    Telephone: 0.0064
    Unknown: 0.0247
    Video/Online: 0.0036
  Unknown:
    Unknown: 0.0264
99G:
  GP:
    Face-to-Face: 0.0279
    Home Visit: 0.0125
    Telephone: 0.0121
    Unknown: 0.0338
    Video/Online: 0.0182
  Other Practice staff:
    Face-to-Face: 0.0733
    Home Visit: 0.0088
    Telephone: 0.0087
    Unknown: 0.0293
    Video/Online: 0.0189
  Unknown:
    Unknown: 0.0323
A3A8R:
  GP:
    Face-to-Face: 0.0551
    Home Visit: 0.023
    Telephone: 0.0273
    Unknown: 0.0043
    Video/Online: 0.0041
  Other Practice staff:
    Face-to-Face: 0.1167
    Home Visit: 0.0356
    Telephone: 0.0568
    Unknown: 0.0023
    Video/Online: 0.0027
  Unknown:
    Face-to-Face: 0.0043
    Home Visit: 0.1114
    Telephone: 0.0269
    Unknown: 0.0217
    Video/Online: 0.0291
B2M3M:
  GP:
    Face-to-Face: 0.0405
    Home Visit: 0.0178
    Telephone: 0.0215
    Unknown: 0.0011
    Video/Online: 0.0005
  Other Practice staff:
    Face-to-Face: 0.0775
    Home Visit: 0.0133
    Telephone: 0.052
    Unknown: 0.0011
    Video/Online: 0.0181
  Unknown:
    Face-to-Face: 0.0029
    Home Visit: 0.0076
    Telephone: 0.0079
    Unknown: 0.0291
    Video/Online: 0.0291
D2P2L:
  GP:
    Face-to-Face: 0.0463
    Home Visit: 0.0188
    Telephone: 0.0234
    Unknown: 0.0189
    Video/Online: 0.0023
  Other Practice staff:
    Face-to-Face: 0.0885
    Home Visit: 0.0239
    Telephone: 0.0569
    Unknown: 0.0204
    Video/Online: 0.0048
  Unknown:
    Face-to-Face: 0.0006
    Home Visit: 0.0132
    Telephone: 0.0026
    Unknown: 0.0245
    Video/Online: 0.0291
D4U1Y:
  GP:
    Face-to-Face: 0.0615
    Home Visit: 0.0133
    Telephone: 0.0244
    Unknown: 0.0023
    Video/Online: 0.0012
  Other Practice staff:
    Face-to-Face: 0.0774
    Home Visit: 0.0194
    Telephone: 0.0595
    Unknown: 0.024
    Video/Online: 0.0046
  Unknown:
    Face-to-Face: 0.0291
    Home Visit: 0.0372
    Telephone: 0.0291
    Unknown: 0.0291
    Video/Online: 0.0291
D9Y0V:
  GP:
    Face-to-Face: 0.0353
    Home Visit: 0.0167
    Telephone: 0.0362
    Unknown: 0.0149
    Video/Online: 0.0046
  Other Practice staff:
    Face-to-Face: 0.0624
    Home Visit: 0.0227
    Telephone: 0.0361
    Unknown: 0.0234
    Video/Online: 0.0122
  Unknown:
    Face-to-Face: 0.0019
    Home Visit: 0.0145
    Telephone: 0.09
    Unknown: 0.0149
    Video/Online: 0.0291
M1J4Y:
  GP:
    Face-to-Face: 0.0336
    Home Visit: 0.0191
    Telephone: 0.0073
    Unknown: 0.0409
    Video/Online: 0.0138
  Other Practice staff:
    Face-to-Face: 0.0667
    Home Visit: 0.0337
    Telephone: 0.0129
    Unknown: 0.0499
    Video/Online: 0.0091
  Unknown:
    Unknown: 0.0243
M2L0M:
  GP:
    Face-to-Face: 0.0314
    Home Visit: 0.0205
    Telephone: 0.0157
    Unknown: 0.0516
    Video/Online: 0.0012
  Other Practice staff:
    Face-to-Face: 0.0587
    Home Visit: 0.0463
    Telephone: 0.0449
    Unknown: 0.0514
    Video/Online: 0.0007
  Unknown:
    Face-to-Face: 0.0024
    Home Visit: 0.0618
    Telephone: 0.0068
    Unknown: 0.0291
    Video/Online: 0.0291
W2U3Z:
  GP:
    Face-to-Face: 0.0422
    Home Visit: 0.0242
    Telephone: 0.0174
    Unknown: 0.011
    Video/Online: 0.0244
  Other Practice staff:
    Face-to-Face: 0.0854
    Home Visit: 0.0697
    Telephone: 0.0403
    Unknown: 0.0234
    Video/Online: 0.0616
  Unknown:
    Face-to-Face: 0.0065
    Home Visit: 0.051
    Telephone: 0.0129
    Unknown: 0.0283
    Video/Online: 0.1221
X2C4Y:
  GP:
    Face-to-Face: 0.0262
    Home Visit: 0.0216
    Telephone: 0.0087
    Unknown: 0.0317
    Video/Online: 0.0044
  Other Practice staff:
    Face-to-Face: 0.0468
    Home Visit: 0.0104
    Telephone: 0.0087
    Unknown: 0.043
    Video/Online: 0.0041
  Unknown:
    Face-to-Face: 0.0291
    Unknown: 0.0238
```

<br><hr><br>