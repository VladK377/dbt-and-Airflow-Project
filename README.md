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
    - Macros created in dbt 'listagg_grouped.sql'. Macros requres
    - Using SQL queries and dbt models to perform the aggregation.
    - Results are stored in a specified Snowflake table.

2. **Data Cleansing**:
    - Identifying and applying data cleansing operations to clean the data.
    - Implementing the cleansing process with Python and/or SQL.
    - Storing the cleansed data in a specified database table.

3. **Fuzzy Matching**:
    - Implementing fuzzy matching logic from the Alteryx workflows.
    - Using Python libraries like `fuzzywuzzy` to match records.
    - Storing matched data in Snowflake.

4. **dbt Models**:
    - dbt models are created to encapsulate SQL transformations and aggregations.
    - Ensuring that dbt models are well-structured and following best practices.

5. **Airflow DAGs**:
    - Orchestrating the workflow using Airflow DAGs that trigger dbt models and Python scripts.
    - DAGs are modular, reusable, and follow best practices to ensure smooth execution.

## Setup Instructions

### Prerequisites
- Python 3.x
- Apache Airflow
- dbt (Data Build Tool)
- Snowflake account for data storage (optional, depending on your project setup)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/VladK377/dbt-and-Airflow-Project.git
cd dbt-and-Airflow-Project

