from flask import Flask, jsonify
from flask_restful import Api
import sqlite3
from sqlite3 import Error
import time
from datetime import datetime
import plotly.graph_objects as go
import dbcommands
import config

app = Flask(__name__)
api = Api(app)

@app.route('/get-patients', methods=['GET'])
def get_patients():
    patients = read_db(dbcommands.sql_get_patients)
    patients = [{"id": p[0], "first_name": p[1], "last_name": p[2], "DOB": p[3]} for p in patients]
    print(patients)
    response = jsonify(patients)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get-results/<id>', methods=['GET'])
def get_results(id):
    db_result = read_db(dbcommands.sql_get_results.format(id))
    results = [{"id": r[0], "temperature": float(r[1]), "pressure_systolic": int(r[2]), "pressure_diastolic": int(r[3]), "SpO2": int(r[4]), "heart_rate": int(r[5]), "time": "{:02d}".format(datetime.fromtimestamp(float(r[7])).hour, "") + ":" + "{:02d}".format(datetime.fromtimestamp(float(r[7])).minute)} for r in db_result]

    yTemperature = [(r['time'], r['temperature']) for r in results]
    yPressureSys = [(r['time'], r['pressure_systolic']) for r in results]
    yPressureDias = [(r['time'], r['pressure_diastolic']) for r in results]
    ySpO2 = [(r['time'], r['SpO2']) for r in results]
    yHeartRate = [(r['time'], r['heart_rate']) for r in results]
    
    #uworzenie zmiennej dla nazw plikow(wykresow)
    filename = config.FILES_PATH + "/" + str(id) + "-{}.png"

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[t[0] for t in yTemperature], y=[t[1] for t in yTemperature], name="Temperature"))
    fig.update_yaxes(title="Temperature")
    fig.write_image(filename.format("temp"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[t[0] for t in yPressureSys], y=[t[1] for t in yPressureSys], name="Pressure Systolic"))
    fig.add_trace(go.Scatter(x=[t[0] for t in yPressureDias], y=[t[1] for t in yPressureDias], name="Pressure Diastolic"))
    fig.update_yaxes(title="Pressure")
    fig.write_image(filename.format("press"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[t[0] for t in ySpO2], y=[t[1] for t in ySpO2], name="SpO2"))
    fig.update_yaxes(title="SPo2")
    fig.write_image(filename.format("spo2"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[t[0] for t in yHeartRate], y=[t[1] for t in yHeartRate], name="Heartrate"))
    fig.update_yaxes(title="Heartrate")
    fig.write_image(filename.format("hr"))
    
    response = jsonify("")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def read_db(sqlCommand):
    conn = create_connection(config.DB_PATH)
    cur = conn.cursor()
    rows = [r for r in cur.execute(sqlCommand)]
    return rows

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()