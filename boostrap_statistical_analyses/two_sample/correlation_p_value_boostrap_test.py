# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:37:36 2020

@author: Philipe_Leal
"""

import numpy as np



def correlation_coefficient_pvalue(data1, data2, n_samples):
    
    corr_coeffs = np.empty(n_samples)
    obtained_corr = np.corrcoef(data1, data2)[0][1]
    
    for i in range(n_samples):
        
        data1_shuffled = np.random.permutation(data1)
        
        corr_coeffs[i] = np.corrcoef(data1_shuffled, data2)[0][1]
        
    p_value = np.mean( np.abs(corr_coeffs) >= np.abs(obtained_corr) )
    
    return {'Randomized_Pearson_Mean_Corr' : np.mean(corr_coeffs),
            'IC': np.percentile(corr_coeffs, [2.5, 97.5]),
            'pvalue': p_value}
    



if '__main__' == __name__:
        
    """Do a permutation test: Permute the series1 data values but leave the 
        series 2 untouched.
        
       Evaluate the correlation between the permutated and the original data
       for all iterations.
       
       Evaluate the amount of times (in %) 
       that the randomized pvalue got more extreme than the observed one.
       
       This percentage represents the probability of having a correlation 
       more extreme than the observed one given that 
       the two series are independent: therefore, have no correlation
       between themselves.
       
       The IC represents the thresholds that would be expected in case
       both series were independent assuming normal distribution.
       If the given returned correlation coefficient is out of that bound,
       we could assume that the data is not independent.
       
       
    
    """
    
    data1 = np.random.normal(-50,4, 100)
    
    data2 = np.random.normal(15, 1, 100)
    n_samples = 9999
    
    R = correlation_coefficient_pvalue(data1, data2, n_samples)
    
    print(R)
    
    