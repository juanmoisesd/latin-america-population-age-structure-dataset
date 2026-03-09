# Data Dictionary

This document describes the variables included in the demographic dataset used for the Latin America Population Age Structure project.

All variables follow a standardized naming convention compatible with Python, JavaScript, and statistical software.

---

## country
Type: string  
Description: Name of the country.

Example:
Mexico, Argentina, Chile.

---

## year
Type: integer  
Description: Reference year of the demographic observation.

Example:
1995, 2000, 2005, 2010, 2015, 2020.

---

## population_total_millions
Type: numeric (float)  
Unit: millions of people  

Description:  
Total population of the country in the specified year, expressed in millions.

Example:
126.7 = 126.7 million inhabitants.

---

## pct_0_14
Type: numeric (percentage)  
Unit: percent (%)

Description:  
Share of the population aged **0–14 years**.

---

## pct_15_24
Type: numeric (percentage)  
Unit: percent (%)

Description:  
Share of the population aged **15–24 years**.

---

## pct_25_54
Type: numeric (percentage)  
Unit: percent (%)

Description:  
Share of the population aged **25–54 years**.

---

## pct_55_64
Type: numeric (percentage)  
Unit: percent (%)

Description:  
Share of the population aged **55–64 years**.

---

## pct_65_plus
Type: numeric (percentage)  
Unit: percent (%)

Description:  
Share of the population aged **65 years or older**.

---

## pop_0_14_thousands
Type: numeric  
Unit: thousands of people

Description:  
Absolute population aged **0–14 years**, expressed in thousands.

---

## pop_15_24_thousands
Type: numeric  
Unit: thousands of people

Description:  
Absolute population aged **15–24 years**, expressed in thousands.

---

## pop_25_54_thousands
Type: numeric  
Unit: thousands of people

Description:  
Absolute population aged **25–54 years**, expressed in thousands.

---

## pop_55_64_thousands
Type: numeric  
Unit: thousands of people

Description:  
Absolute population aged **55–64 years**, expressed in thousands.

---

## pop_65_plus_thousands
Type: numeric  
Unit: thousands of people

Description:  
Absolute population aged **65 years or older**, expressed in thousands.

---

## source
Type: string  

Description:  
Primary data source used to compile the dataset.

Possible values include:

- CEPAL (Economic Commission for Latin America and the Caribbean)
- World Bank
- BBVA Research
- National statistical institutes

---

# Internal Consistency Rules

The dataset follows these structural constraints.

### Age structure consistency

The age distribution should sum approximately to 100%.


pct_0_14

pct_15_24

pct_25_54

pct_55_64

pct_65_plus
≈ 100


Minor rounding differences may occur.

---

### Population consistency

Absolute age-group populations should approximately match the total population.


(pop_0_14_thousands

pop_15_24_thousands

pop_25_54_thousands

pop_55_64_thousands

pop_65_plus_thousands)
/ 1000
≈ population_total_millions


Small discrepancies may appear due to rounding in source datasets.

---

# Dataset Structure

Each row represents:


country + year


Meaning that each observation corresponds to the demographic structure of a specific country in a specific year.

---

# Usage

This dataset is designed to support:

- demographic transition analysis
- population aging studies
- dependency ratio calculations
- demographic bonus analysis
- population pyramid visualization
- comparative country analysis

The dataset is used by the interactive **Demographic Atlas** included in this repository.
