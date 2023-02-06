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
from sklearn.neural_network import MLPRegressor\

# Function for model selection
def MLP_modelSelect(learning_rate=0.001):
    NN_vol = MLPRegressor(learning_rate_init=learning_rate, random_state=1)
    para_grid_NN = {
        'hidden_layer_sizes': [(100, 50), (50, 50), (10, 100)],
        'max_iter': [500, 1000],
        'alpha': [0.00005, 0.0005]}
    return RandomizedSearchCV(NN_vol, para_grid_NN)

class MLPservice:
    
    def __init__(self, data, learning_rate=0.001, pretrained_model=None):
        self.date = data['date']
        self.realized_vol = data['realized_vol']
        square_ret = self.realized_vol ** 2
        self.X = pd.concat([square_ret, self.realized_vol], axis=1, ignore_index=True).reset_index(drop=True)
        self.lr = learning_rate
        if pretrained_model:
            self.model = pretrained_model
        else:
            self.model = MLP_modelSelect(learning_rate)
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
        pred_mlp = self.model.predict(x_test)
        rmse_mlp = np.sqrt(mse(y_test / 100, pred_mlp / 100))
        
        if printres:
            print('The RMSE value of MLP is {:.4f}' .format(rmse_mlp))
            
        # Predicted DataFrame
        pred_date = self.date[test_start:]
        pred_dict = {
            'date': pred_date,
            'vola': pred_mlp
        }
        pred = pd.DataFrame(pred_dict)
        
        if plotres:
            plt.figure(figsize=(20, 6))
            plt.plot(self.date[-(prev+num_test):], self.realized_vol[-(prev+num_test):] / 100, label='Realized Volatility')
            plt.plot(pred['date'], pred['vola'] / 100, label='Volatility Prediction-MLP', alpha=0.75)
            plt.title(f'Volatility Prediction with MLP', fontsize=12)
            plt.legend()
            plt.show()
            
        return pred_mlp, rmse_mlp