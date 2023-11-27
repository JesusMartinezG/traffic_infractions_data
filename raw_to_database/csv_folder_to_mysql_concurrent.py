import os
import csv
import MySQLdb
import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import count

MYSQL_HOST = 'localhost'
MYSQL_USER = 'trafico'
MYSQL_PASSWORD = 'trafico.1234'
MYSQL_DATABASE = 'DATOS_ABIERTOS_2'

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger('Transactions')

db = MySQLdb.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    passwd=MYSQL_PASSWORD,
    db=MYSQL_DATABASE
)

logger.info(f"Connected to database")

csv_folder = '../raw_data/'

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Relative path to the "raw_data" directory
raw_data_directory = os.path.join(current_directory, csv_folder)

# List all files in the "raw_data" directory
all_files = os.listdir(raw_data_directory)

# Filter files that start with "inViales"
filtered_files = [file for file in all_files if file.startswith("inViales")]

# Initialize database table
with open(os.path.join(current_directory, 'schema.sql'), 'r') as file:
    sql_script = file.read()

cursor = db.cursor()
cursor.execute(sql_script)


def process_row(row):
    cursor.execute(
        '''
        INSERT INTO inViales
        (
            folio,
            creacion,
            dia_semana,
            cierre,
            tipo_incidente_c4,
            incidente_c4,
            alcaldia_inicio,
            latitud,
            longitud,
            codigo_cierre,
            clas_con_f_alarma,
            tipo_entrada,
            alcaldia_cierre,
            colonia
        ) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',
        (row[0], f'{row[1]} {row[2]}', row[3], f'{row[4]} {row[5]}', row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
    )
    return 1


def process_csv_file(filename):
    logger.info("Processing: %s", filename)
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        with ThreadPoolExecutor(max_workers=4) as executor:
            counter = sum(executor.map(process_row, csvreader))

        logger.info("Total no. of rows: %d" % counter)

    return counter


# Use ThreadPoolExecutor for concurrent processing of CSV files
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_csv_file, [os.path.join(raw_data_directory, file) for file in filtered_files]))

# Commit any remaining changes
db.commit()
logger.info("Final no. of rows inserted: %d" % (sum(results)))
cursor.close()
print("Done")