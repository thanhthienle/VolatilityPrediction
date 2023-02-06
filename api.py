from flask import Flask
from flask_cors import CORS, cross_origin
import pandas as pd
import datetime
from flask import jsonify
from database.influxdb import InfluxDB
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# on the terminal type: curl http://127.0.0.1:5000/



# auth_provider = PlainTextAuthProvider(username=CASSANDRA_USER, password=CASSANDRA_PASS)
# cluster = Cluster(contact_points=[CASSANDRA_HOST], port=CASSANDRA_PORT,auth_provider=auth_provider)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
influx = InfluxDB()
# Vẽ biểu đồ chứng khoán của mã code trong thời gian n ngày

@app.route('/OLHC/<code>', methods = ['GET'])
def getData(code):
    data = influx.query_data(code)
    raw_data = data.raw
    res = {
        "time": [],
        "close": [],
        "high": [],
        "low": [],
        "open": [],
        "volume": [],
        "vola": []
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['close'].append(row[1])
            res['high'].append(row[2])
            res['low'].append(row[3])
            res['open'].append(row[4])
            res['volume'].append(row[5])
            res['vola'].append(row[6])
    return jsonify(res)


@app.route('/arch/<code>', methods = ['GET'])
def getArch(code):
    data = influx.query_data("arch_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)

@app.route('/garch/<code>', methods = ['GET'])
def getGarch(code):
    data = influx.query_data("garch_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)

@app.route('/svr_lin/<code>', methods = ['GET'])
def getSVRlin(code):
    data = influx.query_data("svr_lin_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)

@app.route('/svr_poly/<code>', methods = ['GET'])
def getSVRpoly(code):
    data = influx.query_data("svr_poly_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)

@app.route('/svr_rbf/<code>', methods = ['GET'])
def getSVRrbf(code):
    data = influx.query_data("svr_rbf_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)

@app.route('/mlp/<code>', methods = ['GET'])
def getMLP(code):
    data = influx.query_data("mlp_{}".format(code))
    raw_data = data.raw
    res = {
        "time": [],
        "vola": [],
    }
    for value in raw_data['series']:
        for row in value['values']:
            res['time'].append(row[0])
            res['vola'].append(row[1])
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug = True)