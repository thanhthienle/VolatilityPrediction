import pickle
from model.model import normalize_data, classic_forecast
from database.influxdb import InfluxDB
from pandas.tseries.offsets import BusinessDay
import pandas as pd


codes = ["STB", "VIC", "SSI", "MSN", "FPT", "HAG"]
influx = InfluxDB()

def forecast(df: pd.DataFrame, model):
    latest_date = df['date'].iloc[-1]
    forecast_date = [latest_date + 1*BusinessDay()] # Python list to store the next n_forecast trading dates
    # Forecast
    res = {
       "date": forecast_date[0],
       "vola": model.predict([[df['return'].iloc[-1]**2, df['realized_vol'].iloc[-1]]])[0]
    }
    return res

for code in codes:
  df=normalize_data(code)

  filename = './saved_models/ARCH/{}.sav'.format(code)
  loaded_model_arch = pickle.load(open(filename, 'rb'))
  n_forecast = 100
  data = classic_forecast(df=df, horizon=n_forecast, model=loaded_model_arch, plotres=False)
  for i in range(len(data)):
    influx.insert_data_pred(doc=data.loc[i], measurement='arch_{}'.format(code))
  print('ARCH {}'.format(code))

  filename = './saved_models/GARCH/{}.sav'.format(code)
  loaded_model_garch = pickle.load(open(filename, 'rb'))
  n_forecast = 100
  data = classic_forecast(df=df, horizon=n_forecast, model=loaded_model_garch, plotres=False)
  for i in range(len(data)):
    influx.insert_data_pred(doc=data.loc[i], measurement='garch_{}'.format(code))
  print('GARCH {}'.format(code))

  filename = './saved_models/SVR_lin/{}.sav'.format(code)
  loaded_model_svr_lin = pickle.load(open(filename, 'rb'))
  res = forecast(df, loaded_model_svr_lin)
  print(res)
  influx.insert_data_pred(doc=res, measurement='svr_lin_{}'.format(code))
  print('Saved SVR_lin_{}'.format(code))

  filename = './saved_models/SVR_poly/{}.sav'.format(code)
  loaded_model_svr_poly = pickle.load(open(filename, 'rb'))
  res = forecast(df, loaded_model_svr_poly)
  influx.insert_data_pred(doc=res, measurement='svr_poly_{}'.format(code))
  print('Saved SVR_poly_{}'.format(code))

  filename = './saved_models/SVR_rbf/{}.sav'.format(code)
  loaded_model_svr_rbf = pickle.load(open(filename, 'rb'))
  res = forecast(df, loaded_model_svr_rbf)
  influx.insert_data_pred(doc=res, measurement='svr_rbf_{}'.format(code))
  print('Saved SVR_rbf_{}'.format(code))

  filename = './saved_models/MLP/{}.sav'.format(code)
  loaded_model_mlp = pickle.load(open(filename, 'rb'))
  res = forecast(df, loaded_model_mlp)
  influx.insert_data_pred(doc=res, measurement='mlp_{}'.format(code))
  print('Saved MLP_{}'.format(code))