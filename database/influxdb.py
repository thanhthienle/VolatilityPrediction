from influxdb import InfluxDBClient
from config import InfluxDBConfig

from datetime import datetime
class InfluxDB:
  def __init__(self):
    self.client =InfluxDBClient(host=InfluxDBConfig.HOST, port=InfluxDBConfig.PORT, username=InfluxDBConfig.USERNAME, password=InfluxDBConfig.PASSWORD)
    self.db = self.client.switch_database(InfluxDBConfig.DATABASE)

  def insert_data(self, doc, measurement):
    try:
      insert_data = [{
        "measurement": measurement,
        "time": doc['date'],
        "tags":
        {
        },
        "fields": {
          "open": doc['open'],
          "close": doc['close'],
          "high": doc['high'],
          "low": doc['low'],
          "value": doc['value'],
          "volume": doc['volume'],
          "vola": doc['realized_vol']
        }
      }]
      self.client.write_points(insert_data)
    except Exception as ex:
      print(ex)
    return None
  
  def insert_data_pred(self, doc, measurement):
    try:
      insert_data = [{
        "measurement": measurement,
        "time": doc['date'],
        "tags":
        {
        },
        "fields": {
          "vola": doc['vola']
        }
      }]
      self.client.write_points(insert_data)
    except Exception as ex:
      print(ex)
    return None
    

  def query_data(self, measurement):
    try:
      # query = f'SELECT * FROM "{measurement}" WHERE time >= {query_time}'.format(measurement, query_time)
      query = f'SELECT * FROM "{measurement}"'.format(measurement)
      result = self.client.query(query)
      return result
    except Exception as ex:
      print(ex)
    return None
  
