from model.model import normalize_data, ARCH_modelSelect, classic_forecast
from database.influxdb import InfluxDB
from model.SVR import SVRservice
import pickle

influx = InfluxDB()
codes = ["STB", "VIC", "SSI", "MSN", "FPT", "HAG"]

for code in codes:
  df=normalize_data(code)
# # best_hyperparam, arch = ARCH_modelSelect(ret=df['return'])

# # filename = 'finalized_model.sav'
# # pickle.dump(arch, open(filename, 'wb'))
# # loaded_model = pickle.load(open(filename, 'rb'))
# # n_forecast = 100
# # _ = classic_forecast(df=df, horizon=n_forecast, model=loaded_model, plotres=True)
# # print(_)
# # print(loaded_model)
# # print(arch)
  for i in range(4, len(df)):
    influx.insert_data(doc=df.loc[i], measurement=code)
