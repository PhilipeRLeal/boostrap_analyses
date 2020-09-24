# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:47:43 2020

@author: Philipe_Leal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker


a = np.random.normal(size=10)
b = np.random.normal(size=10)

c = np.random.normal(size=10)

def diff_multi(*args):

    Multi = pd.MultiIndex.from_product([*args])
    
    Expected = abs(np.mean([np.mean(np.diff(x)) for x in Multi.to_numpy()]))
    
    print('Expected return: {0}'.format(Expected))
    
    return Expected


def diff_2S(a, b):

    Expected = abs(np.mean(a) - np.mean(b))
    
    print('Expected return: {0}'.format(Expected))
    
    return Expected

diff_multi(a,b)

diff_2S(a, b)