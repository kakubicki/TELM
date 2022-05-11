sql_create_patients_table = """CREATE TABLE IF NOT EXISTS patients (
                                    id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text,
                                    date_of_birth text
                                );"""

sql_create_results_table = """CREATE TABLE IF NOT EXISTS results (
                                id integer PRIMARY KEY,
                                temperature text NOT NULL,
                                pressure_systolic text NOT NULL,
                                pressure_diastolic text NOT NULL,
                                SpO2 text NOT NULL,
                                heart_rate text NOT NULL,
                                patient_id integer NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (patient_id) REFERENCES patients (id)
                            );"""

sql_delete_results = "delete from results;"

sql_insert_patients = '''INSERT INTO patients VALUES(?,?,?,?);'''

sql_insert_result = '''INSERT INTO results(temperature, pressure_systolic, pressure_diastolic, SpO2, heart_rate, patient_id, timestamp)
                       VALUES(?,?,?,?,?,?,?);'''

sql_get_results = "select * from results where patient_id={} order by timestamp asc limit 30;" #desc zamiast asc wowczas malejaco

sql_get_patients = "select * from patients order by id;"