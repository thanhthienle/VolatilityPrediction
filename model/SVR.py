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
import torch
import torch.nn as nn
from sklearn.neural_network import MLPRegressor

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