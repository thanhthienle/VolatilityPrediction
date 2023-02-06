from model.model import normalize_data, ARCH_modelSelect, GARCH_modelSelect
from model.SVR import SVRservice
from model.NN import MLPservice
import pickle

codes = ["STB", "VIC", "SSI", "MSN", "FPT", "HAG"]
# codes = ["STB", "VIC", "SSI", "MSN", "FPT", "HAG", "KDC", "EIB", "DPM", "VNM", "REE", "OGC", "IJC", "VCB", "PNJ", "BVH", "ITA", "HPG", "CTG", "SJS", "QCG", "PVF", 'PVD', "CII", "SBT", "VSH", "KDH", "DIG", "HVG", 'GMD']

for code in codes:
  df=normalize_data(code)
  best_hyperparam_ARCH, arch = ARCH_modelSelect(ret=df['return'])
  filename = './saved_models/ARCH/{}.sav'.format(code)
  pickle.dump(arch, open(filename, 'wb'))
  print('Saved ARCH_{}'.format(code))

  best_hyperparam_GARCH, garch = GARCH_modelSelect(ret=df['return'])
  filename = './saved_models/GARCH/{}.sav'.format(code)
  pickle.dump(garch, open(filename, 'wb'))
  print('Saved GARCH_{}'.format(code))

  # SVR_service_lin = SVRservice(df, 'lin')
  # SVR_service_poly = SVRservice(df, 'poly')
  # SVR_service_rbf = SVRservice(df, 'rbf')

  # SVR_service_lin.train(0)
  # svr_lin = SVR_service_lin.model
  # filename = './saved_models/SVR_lin/{}.sav'.format(code)
  # pickle.dump(svr_lin, open(filename, 'wb'))
  # print('Saved SVR_lin_{}'.format(code))

  # SVR_service_poly.train(0)
  # svr_poly = SVR_service_poly.model
  # filename = './saved_models/SVR_poly/{}.sav'.format(code)
  # pickle.dump(svr_poly, open(filename, 'wb'))
  # print('Saved SVR_poly_{}'.format(code))

  # SVR_service_rbf.train(0)
  # svr_rbf = SVR_service_rbf.model
  # filename = './saved_models/SVR_rbf/{}.sav'.format(code)
  # pickle.dump(svr_rbf, open(filename, 'wb'))
  # print('Saved SVR_rbf_{}'.format(code))

  # MLP_service = MLPservice(df)
  # MLP_service.train(0)
  # mlp = MLP_service.model
  # filename = './saved_models/MLP/{}.sav'.format(code)
  # pickle.dump(mlp, open(filename, 'wb'))
  # print('Saved MLP_{}'.format(code))