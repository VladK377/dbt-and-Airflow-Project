import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import snowflake.connector
import re
from thefuzz import fuzz



def creat_cursor():
    # Snowflake credentials
  SNOWFLAKE_ACCOUNT = "be66569.eu-central-1"
  SNOWFLAKE_USER = "VKUT"
  SNOWFLAKE_PASSWORD = "*****"
  SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
  SNOWFLAKE_DATABASE = "ADP_WORKSPACES"
  SNOWFLAKE_SCHEMA = "AE"
  # Step 1: Establish a connection to Snowflake
  connection = snowflake.connector.connect(
      account=SNOWFLAKE_ACCOUNT,
      user=SNOWFLAKE_USER,
      password=SNOWFLAKE_PASSWORD,
      warehouse=SNOWFLAKE_WAREHOUSE,
      database=SNOWFLAKE_DATABASE,
      schema=SNOWFLAKE_SCHEMA,
  )

  cursor = connection.cursor()
  return connection



def create_table_from_dataframe(conn, df, table_name):
    cursor = conn.cursor()
    # Properly quote column names to handle special characters and case sensitivity
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join([f'"{col}" STRING' for col in df.columns])}
    );
    """
    cursor.execute(create_table_query)
    print(f"Table {table_name} created successfully.")

def insert_data_from_dataframe(conn, df, table_name):
    cursor = conn.cursor()
    # Properly quote column names in the INSERT statement
    insert_query = f"""
    INSERT INTO {table_name} ({', '.join([f'"{col}"' if ' ' in col or '"' in col else col for col in df.columns])})
    VALUES ({', '.join(['%s'] * len(df.columns))});
    """

    # Convert DataFrame to tuple format for insertion
    data_to_insert = [tuple(row) for row in df.itertuples(index=False, name=None)]

    cursor.executemany(insert_query, data_to_insert)
    print(f"Inserted {len(data_to_insert)} rows into {table_name}.")



def snowflake_pipeline():

    connection = creat_cursor()
    cursor = connection.cursor()

    # Step 2: Fetch data from Snowflake
    cursor.execute("SELECT * FROM ADP_WORKSPACES.AE.pre_fuzzy_aggregated")
    results = cursor.fetchall()

    # Get column names from cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Create a Pandas DataFrame
    df = pd.DataFrame(results, columns=column_names)

    # Step 3: Convert column names to uppercase
    df.columns = df.columns.str.replace(" ", "_")

    # Step 3: Apply transformation to specific columns (Site Name and Parent Account Name)
    df['Site_Name'] = df['Site_Name'].apply(lambda x: re.sub(r"[^\w\s]", '', str(x)).upper())
    df['Parent_Name'] = df['Parent_Name'].apply(lambda x: re.sub(r"[^\w\s]", '', str(x)).upper())

    # Table name for insertion
    table_name = "pre_fuzzy_cleansed"

    # Create table in Snowflake
    create_table_from_dataframe(connection, df, table_name)

    # Insert data into Snowflake
    insert_data_from_dataframe(connection, df, table_name)

    # Step 2: Fetch data from Snowflake
    cursor.execute("SELECT * FROM ADP_WORKSPACES.AE.pre_fuzzy_cleansed")
    results = cursor.fetchall()

    # Get column names from cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Create a Pandas DataFrame
    df = pd.DataFrame(results, columns=column_names)

    # Generate sequential values for the 'RecordID' column starting from 1
    df['RecordID'] = range(1, len(df) + 1)

    # Combine 'Site Name Cleansed' and 'Country Name' into a new column 'Combined'
    df['Combined'] = df['Site Name Cleansed'] + " " + df['Country Name']

    # Function to compare rows
    def compare_rows(row1, row2):
        return fuzz.ratio(row1, row2)

    # Initialize a list to store results
    results = []

    # Iterate through all rows and compare them with each other
    for i in range(len(df)):
        for j in range(i + 1, len(df)):  # Compare each row only with the remaining rows
            if df.iloc[i]['Clearence Reason'] != df.iloc[j]['Clearence Reason']:  # Compare only rows from different sources
                combined_1 = df.iloc[i]['Combined']
                combined_2 = df.iloc[j]['Combined']

                # Compare the rows and calculate the similarity coefficient
                similarity = compare_rows(combined_1, combined_2)

                # If similarity is greater than or equal to 80, add to the list
                if similarity >= 80:
                    results.append({
                        'Account UUID1': df.iloc[i]['Account UUID'],
                        'RecordID1': df.iloc[i]['RecordID'],
                        'Account UUID2': df.iloc[j]['Account UUID'],
                        'RecordID2': df.iloc[j]['RecordID']
                    })

    # Convert the results to a DataFrame for convenience
    results_df = pd.DataFrame(results)

    # Group by 'Account UUID1' and concatenate all 'RecordID' values for each 'Account UUID1'
    grouped_result = results_df.groupby('Account UUID1')[['RecordID1', 'RecordID2']].apply(
        lambda x: ','.join(x['RecordID1'].astype(str) + '-' + x['RecordID2'].astype(str))
    ).reset_index(name='RecordID')

    # Rename the column 'Account UUID1' to 'Account UUID'
    grouped_result.rename(columns={'Account UUID1': 'Account UUID'}, inplace=True)


    table_name = "pre_fuzzy_result"

    # Create table in Snowflake
    create_table_from_dataframe(connection, df, table_name)

    # Insert data into Snowflake
    insert_data_from_dataframe(connection, df, table_name)

    cursor.close()
    connection.close()




