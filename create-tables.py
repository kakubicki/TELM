import sqlite3 
from sqlite3 import Error
import dbcommands
import config

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_patient(conn, patient):
    print("inserting: " + str(patient))
    cur = conn.cursor()
    cur.execute(dbcommands.sql_insert_patients, patient)
    conn.commit()
    return cur.lastrowid

def main():
    conn = create_connection(config.DB_PATH)
    if conn is not None:
        create_table(conn, dbcommands.sql_create_patients_table)
        create_table(conn, dbcommands.sql_create_results_table)
        print("Finished creating tables.")
        insert_patient(conn, (1, "Corey", "Trevor", "04/10/2010"))
        insert_patient(conn, (2, "Jim", "Lahey", "11/11/1980"))
        insert_patient(conn, (3, "Phil", "Collins", "01/12/1975"))
    else:
        print("Error! cannot create the database connection.")
    pass

if __name__ == '__main__':
    main()