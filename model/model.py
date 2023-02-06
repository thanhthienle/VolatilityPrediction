from scipy.stats import norm
import scipy.optimize as opt
from datetime import datetime
import time
from arch import arch_model
from numba import jit
from sklearn.metrics import mean_squared_error as mse
import pandas as pd
from pandas.tseries.offsets import BusinessDay
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from warnings import filterwarnings
from sklearn.svm import SVR
from scipy.stats import uniform as sp_rand
from sklearn.model_selection import RandomizedSearchCV
import random
from sklearn.neural_network import MLPRegressor
filterwarnings('ignore')

def convertToDate(x: str):
    if isinstance(x, str):
      return datetime.strptime(x, '%d/%m/%Y')
    return x

def toFloat(x: str):
    if isinstance(x, str):
      return float("".join(x.split(',')))
    return x

def toInt(x: str):
    if isinstance(x, str):
      return int("".join(x.split(',')))
    return x

def classic_forecast(df: pd.DataFrame, horizon: int, model, plotres=False):
    # Forecast
    forecast_arch = model.forecast(horizon=horizon)
    
    # Build forecast dataframe
    latest_date = df['date'].iloc[-1]
    forecast_date = [latest_date + i*BusinessDay() for i in range(1, horizon+1)] # Python list to store the next n_forecast trading dates
    forecast_vola = forecast_arch.variance.iloc[-1].values
    
    forecast_dict = {
        'date': forecast_date,
        'vola': forecast_vola,
    }
    forecast = pd.DataFrame(forecast_dict)
    
    # Draw
    if plotres:
        plt.figure(figsize=(20, 6))
        plt.plot(df['date'].iloc[-100:], df['realized_vol'][-100:] / 100, label='Realized Volatility')
        plt.plot(forecast['date'], forecast['vola'] / 100, label='Volatility Prediction-ARCH')
        plt.title('Volatility Forecasting with ARCH', fontsize=12)
        plt.legend()
        plt.show()
    
    return forecast

def normalize_data(code):
  df = pd.read_json('./data/{}.json'.format(code), convert_dates=False)
  df = df.drop_duplicates().reset_index(drop=True)
  df.date = df.date.apply(convertToDate)
  df = df.sort_values(by='date').reset_index(drop=True)
  for column in ['close', 'high', 'open', 'low']:
    df[column] = df[column].apply(toFloat)
  for column in ['value', 'volume']:
    df[column] = df[column].apply(toInt)
  df['return'] = df.close.pct_change().apply(lambda x: x*100)
  df['return'][0] = 0
  df['realized_vol'] = df['return'].rolling(5).std()
  return df

def ARCH_modelSelect(ret):
  bic_arch = []
  best_param = -1
  for p in range(1, 5):
      arch = arch_model(ret, mean='zero', vol='ARCH', p=p).fit(disp='off')
      bic_arch.append(arch.bic)
      if arch.bic == np.min(bic_arch):
          best_param = p
  return best_param, arch_model(ret, mean='zero', vol='ARCH', p=best_param).fit(disp='off')
# best_hyperparam, arch = ARCH_modelSelect(ret=df['return'])

def GARCH_modelSelect(ret):
  bic_garch = []
  best_params = -1, -1
  for p in range(1, 5):
    for q in range(1, 5):
      garch = arch_model(ret,
                          mean='zero',
                          vol='GARCH',
                          p=p, o=0, q=q).fit(disp='off')
      bic_garch.append(garch.bic)
      if garch.bic == np.min(bic_garch):
        best_params = p, q
  return best_params, arch_model(ret,
                                  mean='zero',
                                  vol='GARCH',
                                  p=best_params[0], o=0, q=best_params[1]).fit(disp='off')

