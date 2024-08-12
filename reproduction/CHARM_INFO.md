# CHARM Info

**Time unit:** Day

**Admissions:** three types of admissions
   
   **Emergency:** triangular distribution
   
   **Elective:** triangular distribution
   
   **Covid-19 positive:** CSV file 

**Zones:** Zones can be any of:

| Zone type   | Short | Code |
| --- | --- | --- |
| Emergency ICU | EM | 1 |
| Emergency Recovery | EMR | 2 |
| Elective ICU | EL | 3 |
| Elective Recovery | ELR | 4 |
| Covid-19 ICU | C | 5 |
| Covid-19 Recovery | CR | 6 |

Each zone can be defined as COVID, EMERGENCY, ELECTIVE and respective RECOVERY

IF COVID occupancy > UPPER_THRESHOLD, EMERGENCY/ELECTIVE BECOMES COVID 

IF COVID occupancy < LOWER_THRESHOLD, reverse EMERGENCY/ELECTIVE

**Run length:** As many days as the entries in DAILY_ARRIVALS.csv

## Input Parameters

#### file: ICU_INPUT_PARAMS.csv

**Replications:** *Number of simulation replications {integer}*

**Arrivals**

 - Emergency daily arrivals: *Three fields {min, max, mode}*

 - Elective daily arrivals: *Three fields {min, max, mode}*

**Length of Stay (in days):**

 - Emergency ICU LoS: *Three fields {min, max, mode}*

 - Elective ICU LoS: *Three fields {min, max, mode}*

 - Covid-19 ICU Los: *Three fields {min, max, mode}*

 - Emergency recovery LoS: *Three fields {min, max, mode}*

 - Elective recovery LoS: *Three fields {min, max, mode}*

 - Covid-19 recovery Los : *Three fields {min, max, mode}*

**Mortality (probability)**

 - Emergency ICU mortality: *One field {0-1}*

 - Elective ICU mortality: *One field {0-1}*

 - Covid-19 ICU mortality: *One field {0-1}*

 - Emergency recovery mortality: *One field {0-1}*

 - Elective recovery mortality: *One field {0-1}*

 - Covid-19 recovery mortality: *One field {0-1}*

**Covid ICU wards occupancy threshold (percentage)**

 - Upper threshold: *One field {0-100}*

 - Lower threshold: *One field {0-100}*

#### file: ZONES.csv

**ID:** *Integer in ascending order starting from 1*

**Type:** *Integer {1-6}*

**Capacity:** *Integer {number of beds in the zone}*

#### file: DAILY_ARRIVALS.csv

**Index:** *Integer in ascending order starting from 0*

**Day:** *Can be any e.g., Integer or Date*

**Covid-19 positive:** *Integer {number of Covid-19 positive patients}*
