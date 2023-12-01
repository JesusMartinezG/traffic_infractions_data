import os
import csv
import MySQLdb
import logging
from itertools import count

MYSQL_HOST = 'localhost'
MYSQL_USER = 'trafico'
MYSQL_PASSWORD = 'trafico.1234'
MYSQL_DATABASE = 'DATOS_ABIERTOS'

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)
logger = logging.getLogger('Transactions')

db = MySQLdb.connect(host=MYSQL_HOST,
             user=MYSQL_USER,
             passwd=MYSQL_PASSWORD,
             db=MYSQL_DATABASE
             )

cursor = db.cursor()

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

cursor.execute(sql_script)

counter = (count())

# Iterate over the filtered files
for file in filtered_files:
    filename = os.path.join(raw_data_directory, file)
    # Your processing logic for each file goes here
    logger.info("Processing: %s", filename)
    
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            # SAVE TO DATABASE
            # print('INSERT INTO inViales(folio,creacion,dia_semana,cierre,tipo_incidente_c4,incidente_c4,alcaldia_inicio,latitud,longitud,codigo_cierre,clas_con_f_alarma,tipo_entrada,alcaldia_cierre,colonia) VALUES(%s,%s %s,%s,%s %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'%row)
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
                (row[0], f'{row[1]} {row[2]}',row[3], f'{row[4]} {row[5]}', row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
            )
            
            next(counter)
            
            if csvreader.line_num%10000==0:
                db.commit()
                logger.info(f"Commited {csvreader.line_num} rows")
    
        # get total number of rows
        logger.info("Total no. of rows: %d"%(csvreader.line_num))
    
    # close the connection to the database.
db.commit()
logger.info("Final no. of rows inserted: %d"%(next(counter)-1))
cursor.close()
print("Done")