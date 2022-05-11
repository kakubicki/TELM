import sys
import time 
import sqlite3
import numpy
from sqlite3 import Error

import config
import dbcommands

#generowanie parametrow
def create_random_data():
    random_factor = numpy.random.normal(0, 0.15)
    temp = 36.6 + random_factor
    random_factor = numpy.random.normal(0, 0.15)
    pressure_systolic = round(120 + 20 * random_factor)
    random_factor = numpy.random.normal(0, 0.15)
    pressure_diastolic = round(80 + 10 * random_factor)
    random_factor = numpy.random.normal(0, 0.15)
    heart_rate = round(60 + 5 * random_factor)
    random_factor = numpy.random.normal(0, 0.15)
    SpO2 = min(100, round(90 + 5 * random_factor))
    return (str(temp), str(pressure_systolic), str(pressure_diastolic), str(heart_rate), str(SpO2))

#laczenie z baza danych sql
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

#wstawienie do bazy parametrow dla danego patientID
def insert_result(patientID, t):
    conn = create_connection(config.DB_PATH)
    res = create_random_data() + (patientID, t)
    print("inserting: " + str(res))
    cur = conn.cursor()
    cur.execute(dbcommands.sql_insert_result, res)
    conn.commit()
    return cur.lastrowid

def main():
    if len(sys.argv) < 3:
        print("You need to specify patient ID and samples count")
        input("Press Enter to continue...")
    patientID = int(sys.argv[1])
    count = int(sys.argv[2])
    t = round(time.time())
    for i in range (1, count):
        insert_result(patientID, t - i * 60) 
    input("Press Enter to continue...")

if __name__ == '__main__':
    main()