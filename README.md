# dbt and Airflow Project

This project involves automating data processing workflows using **dbt** (Data Build Tool) and **Apache Airflow**. The workflows include data aggregation, cleansing, fuzzy matching, and orchestration to ensure data pipelines run smoothly and efficiently.

## Project Overview

### Objective
- The goal of this project is to replicate ETL operations initially performed in Alteryx workflows.
- The core components include:
    - **Data Aggregation**: Using SQL and dbt models to aggregate data.
    - **Data Cleansing**: Implementing data cleansing operations with Python scripts.
    - **Fuzzy Matching**: Simple fuzzy matching logic implemented with Python.
    - **dbt Models**: Creating SQL transformations and aggregations using dbt.
    - **Airflow DAGs**: Orchestrating the execution of dbt models and Python scripts using Airflow.

### Components:
1. **Data Aggregation**:
    - The macro `listagg_grouped.sql` in dbt is used for data aggregation.
    - This macro requires the full table name and the column for grouping to be specified.
    - All other columns are automatically aggregated using the `LISTAGG` function.
    - In the file `pre_fuzzy_aggregated.sql`, the table is aggregated utilizing this macro.
    - The results are stored in the Snowflake table `ADP_WORKSPCES.AE.PRE_FUZZY_AGGREGATED`.

2. **Data Cleansing**:
    - Data cleansing is performed in the `adp_work.py` script.
    - The cleansed data is stored in the Snowflake table `ADP_WORKSPCES.AE.PRE_FUZZY_CLEANSED`.
    -  _Note_: In the Alteryx workflow, data cleansing is applied to the columns 'Site Name Cleansed' and 'Parent Account Name Cleansed'. 
      In the initial table and subsequent processing steps, these columns do not exist. 
      Data cleansing is applied to the 'Site Name' and 'Parent Account Name' columns, and after cleansing, the columns are named 'Site Name Cleansed' and 'Parent Account Name Cleansed'.
      
3. **Fuzzy Matching**:
    - Fuzzy matching is implemented using the `thefuzz` library.
    - The script for fuzzy matching is located in the `adp_work.py` file.
    - The results are stored in the Snowflake table `ADP_WORKSPCES.AE.PRE_FUZZY_RESULT`.
    - _Note_: In the Alteryx workflow, the column 'Source' is used to compare results from different sources. 
      In the initial table and subsequent processing steps, there was no field specifically named "Source". 
      A placeholder field, 'Clearence Reason', was used in its place for this purpose.


4. **dbt Models**:

   There are two dbt model files:
    - `pre_fuzzy_aggregated.sql`: This file contains the main SQL transformations for aggregating the data.
    - `listagg_grouped.sql`: This file defines a macro that performs aggregation by grouping based on a specified column and applying the `LISTAGG` function to the remaining columns.

6. **Airflow DAGs**:
    - Data cleansing and orchestration are managed in the `dbt_pipeline.py` file using Airflow.
 



####  Clone the Repository
```bash
git clone https://github.com/VladK377/dbt-and-Airflow-Project.git
cd dbt-and-Airflow-Project

