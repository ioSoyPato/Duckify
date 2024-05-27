# DataBase management is a key part of the project. The database_management.py file contains the functions that interact with the database.
# The functions are used to retrieve data from the database, update the number of times a song has been played, and recommend a song based on the genre of the current song. 
# The functions are called from the main.py file when a user interacts with the web application.

import pandas as pd
import libsql_experimental
import logging
from dotenv import load_dotenv
import os

'''
Create the Tables in Turso
Using libsql (experimental) to create and initialise the DB using the enviroment data
'''

'''
# Load the environment variables
load_dotenv()

# Set up the logging level
logging.basicConfig(level=logging.INFO)

# Set up the database connection using the env variables
auth_token = os.getenv('TURSO_API_KEY')
database_url = 'libsql://duckify-iosoypato.turso.io'

# Create a connection to the database and a cursor to execute queries
try:
    con = libsql_experimental.connect(database_url, sync_url=None, auth_token=auth_token)
    cur = con.cursor()
    logging.info("Conexión a la base de datos establecida con éxito.")
except Exception as e:
    logging.error(f"Error al conectar a la base de datos: {e}")
    raise


# Function to create a table in the Turso database
def create_table(cursor, table_name, df):
    try:
        df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]
        columns = ', '.join([f"{col} TEXT" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        cursor.execute(create_table_query)
        logging.info(f"Tabla {table_name} creada con éxito.")
    except Exception as e:
        logging.error(f"Error al crear la tabla {table_name}: {e}")
        raise

# Function to insert data into a table in the Turso database
def insert_data(cursor, table_name, df, batch_size=10):
    try:
        df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['?' for _ in df.columns])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Insert data in batches
        for start in range(0, len(df), batch_size):
            end = start + batch_size
            batch = df.iloc[start:end]
            data = [tuple(row) for row in batch.itertuples(index=False)]
            logging.debug(f"Insertando lote desde {start} hasta {end}")
            cursor.executemany(insert_query, data)
        logging.info(f"Datos insertados en la tabla {table_name} con éxito.")
    except Exception as e:
        logging.error(f"Error al insertar datos en la tabla {table_name}: {e}")
        raise

# Function to process a CSV file and load its data into a table in the Turso database
def process_csv(csv_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        if "Unnamed: 0" in df.columns:
            df = df.drop("Unnamed: 0", axis=1)
        create_table(cur, table_name, df)
        insert_data(cur, table_name, df)
        logging.info(f"Datos de {csv_file} cargados en la tabla {table_name} con éxito.")
    except Exception as e:
        logging.error(f"Error al procesar el archivo {csv_file}: {e}")
        raise


# All the CSV files and table names to be processed (You can do a for loop to process all the files at once)
csv_files = ['ELECTRONIC.csv', 'POP.csv','RAP.csv',"ROCK.csv","SONGS_DB.csv","User.csv"]  
table_names = ['RAP', 'ROCK', 'ELECTRONIC', 'POP', 'User', 'SONGS_DB']

'''

# Function to read a table from the Turso database and return it as a pandas DataFrame object
def read_table_as_dataframe(table_name):

    # load the environment variables
    load_dotenv()

    # Set up the logging level
    logging.basicConfig(level=logging.INFO)

    #  obtain the API key
    auth_token = os.getenv('TURSO_API_KEY')

    # Set up the database connection using the env variables
    database_url = os.getenv('LIBSQL_URL')

    # Create the Turso database connection
    try:
        con = libsql_experimental.connect(database_url, sync_url=None, auth_token=auth_token)
        cursor = con.cursor()
        logging.info("Conexión a la base de datos establecida con éxito.")
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        raise

    try:
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        rows = cursor.fetchall()
        # Obtener los nombres de las columnas
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]
        df = pd.DataFrame(rows, columns=columns)
        return df
    except Exception as e:
        logging.error(f"Error al leer la tabla {table_name}: {e}")
        raise