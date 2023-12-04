import os
import csv
import sqlite3
import logging
from itertools import count


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logger = logging.getLogger('Transactions')

def create_sqlite_instance():
    # open sqlite database file in folder 'instance' and create it if it doesn't exist
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # create table schema
    cursor.execute('''
        DROP TABLE IF EXISTS inViales
        '''
    )
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inViales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folio TEXT UNIQUE NOT NULL,
            creacion TEXT,
            dia_semana TEXT,
            cierre TEXT,
            tipo_incidente_c4 TEXT,
            incidente_c4 TEXT,
            alcaldia_inicio TEXT,
            latitud REAL,
            longitud REAL,
            codigo_cierre TEXT,
            clas_con_f_alarma TEXT,
            tipo_entrada TEXT,
            alcaldia_cierre TEXT,
            colonia TEXT
        )
    ''')

    csv_folder = '../raw_data/'

    # Get the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Relative path to the "raw_data" directory
    raw_data_directory = os.path.join(current_directory, csv_folder)

    # List all files in the "raw_data" directory
    all_files = os.listdir(raw_data_directory)

    # Filter files that start with "inViales"
    filtered_files = [file for file in all_files if file.startswith("inViales")]

    counter = (count())

    # fill table with data from csv files listed in filtered_files
    for file in filtered_files:
        filename = os.path.join(raw_data_directory, file)
        logger.info("Processing: %s", filename)
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
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
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''',
                    (row[0], f'{row[1]} {row[2]}' if row[1]!='NA' and row[2]!='NA' else None,row[3], f'{row[4]} {row[5]}' if row[4]!='NA' and row[5]!='NA' else None, row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
                )

                next(counter)

                if csvreader.line_num%10000==0:
                    conn.commit()
                    logger.info(f"Commited {csvreader.line_num} rows")

            # get total number of rows
            logger.info("Total no. of rows: %d"%(csvreader.line_num))

    conn.commit()
    logger.info("Final no. of rows inserted: %d"%(next(counter)-1))
    cursor.close()
    print("Done")
    conn.close()

# run create_sqlite_instance() if main file
if __name__ == '__main__':
    create_sqlite_instance()