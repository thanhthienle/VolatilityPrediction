from influxdb import InfluxDBClient
from config import InfluxDBConfig

from datetime import datetime

def network(name):
  if "bsc" in name:
    return "bsc"
  elif "eth" in name:
    return "eth"
  elif "polygon" in name:
    return "polygon"
  elif "ftm" in name:
    return "ftm"
  else:
    return ""

class InfluxDB:
  def __init__(self):
    self.client =InfluxDBClient(host=InfluxDBConfig.HOST, port=InfluxDBConfig.PORT, username=InfluxDBConfig.USERNAME, password=InfluxDBConfig.PASSWORD)
    self.db = self.client.switch_database(InfluxDBConfig.DATABASE)

  def insert_data(self, doc, measurement):
    try:
      # time = list(doc['count'])[-1]
      insert_data = [{
        "measurement": measurement,
        # "time": timestampToDatetime(time),
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
          "volumn": doc['volumn']
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
