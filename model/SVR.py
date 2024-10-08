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

svr_poly = SVR(kernel='poly', degree=2)
svr_lin = SVR(kernel='linear')
svr_rbf = SVR(kernel='rbf')

svr = {
    'poly': svr_poly,
    'lin': svr_lin,
    'rbf': svr_rbf
}

svr_namelookup = {
    'poly': 'Polynomial',
    'lin': 'Linear',
    'rbf': 'RBF'
}

def SVR_modelSelect(kernel: str):
    para_grid = {'gamma': sp_rand(),
                 'C': sp_rand(),
                 'epsilon': sp_rand()}
    return RandomizedSearchCV(svr[kernel], para_grid)

class SVRservice:
    
    def __init__(self, data: pd.DataFrame, kernel: str, pretrained_model=None):
        
        self.date = data['date']
        self.realized_vol = data['realized_vol']
        square_ret = self.realized_vol ** 2
        self.X = pd.concat([square_ret, self.realized_vol], axis=1, ignore_index=True).reset_index(drop=True)
        self.kernel = kernel
        if pretrained_model:
            self.model = pretrained_model
        else:
            self.model = SVR_modelSelect(kernel=kernel)
        self.num_test = None
        
    def train(self, num_test):
        
        # Change service num_test for testing later
        self.num_test = num_test
        test_start = len(self.date) - num_test
        
        # Training data
        x_train = self.X[4:test_start-1]
        y_train = self.realized_vol[5:test_start]
        
        # Select and train model
        self.model.fit(x_train, y_train)
        
    def test(self, num_test, printres=False, plotres=False, prev=0):
        
        # Data
        test_start = len(self.date) - num_test
        x_test = self.X[test_start-1:-1]
        y_test = self.realized_vol[test_start:]
        
        # Predict on test set and calculate RMSE
        pred_svr = self.model.predict(x_test)
        rmse_svr = np.sqrt(mse(y_test / 100, pred_svr / 100))
        
        if printres:
            print('The RMSE value of SVR with {} Kernel is {:.4f}' .format(svr_namelookup[self.kernel], rmse_svr))
            
        # Predicted DataFrame
        pred_date = self.date[test_start:]
        pred_dict = {
            'date': pred_date,
            'vola': pred_svr
        }
        pred = pd.DataFrame(pred_dict)
        
        if plotres:
            plt.figure(figsize=(20, 6))
            plt.plot(self.date[-(prev+num_test):], self.realized_vol[-(prev+num_test):] / 100, label='Realized Volatility')
            plt.plot(pred['date'], pred['vola'] / 100, label='Volatility Prediction-SVR-GARCH', alpha=0.75)
            plt.title(f'Volatility Prediction with SVR-GARCH ({svr_namelookup[self.kernel]})', fontsize=12)
            plt.legend()
            plt.show()
            
        return pred_svr, rmse_svr
        
    

# SVR_service_lin = SVRservice(df, 'lin')
# SVR_service_poly = SVRservice(df, 'poly')
# SVR_service_rbf = SVRservice(df, 'rbf')