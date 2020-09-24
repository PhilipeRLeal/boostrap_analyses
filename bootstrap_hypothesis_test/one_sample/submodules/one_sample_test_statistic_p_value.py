# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:51:41 2020

@author: Philipe_Leal
"""

import numpy as np

from bootstrap_replicate import _draw_bs_reps


def one_sample_series_difference(data, 
                     expected_value=0, 
                     reducer=np.mean):
    
    return reducer(data) - expected_value



def compute_boostrap_pvalue(data, 
                            expected_value = 0,
                            n_reps=999,
                            reducer = np.mean,
                            **reducer_kwargs):
    
    partial_reducer = lambda x: reducer(x, **reducer_kwargs)
    
    partial_diff = lambda x: one_sample_series_difference(x, 
                                              expected_value, 
                                              partial_reducer)
    
    diff_observed = partial_diff(data)
    
    shifted_data = data - partial_reducer(data) + expected_value
    
    bs_replicates = _draw_bs_reps(shifted_data,
                                  reducer=partial_diff,
                                  n_reps=n_reps)
    
    if np.mean(data) < expected_value:
    
        p_value = np.sum(bs_replicates <= np.mean(diff_observed))/n_reps
        
    else:
        p_value = np.sum(bs_replicates >= np.mean(diff_observed))/n_reps
    
    return p_value



if '__main__' == __name__:
    
    ("""
    
     Description:
         Assume that we are measuring a given variable over time (series 1),
         and we assume that a given statistical moment of that series is == K
         (ex: its mean or its variance).
         
         In order to test that, we can do a one sample boostrap test statistics.
         
     Parameters
    ----------
    series1 : TYPE bool Array
        DESCRIPTION.
        
    expected_value : TYPE (float)
        DESCRIPTION: the value to check whether the selected statistical 
        moment of series1 is actually it.
        
        
    n_reps : TYPE (int), optional.
        DESCRIPTION. The default is 999. The number of replicates it will do
        

    Returns
    -------
    p : TYPE (float)
        DESCRIPTION: it represents the probability of observing 
        a test statistic equally or more extreme 
        than the one observed, 
        given that the null hypothesis is true.
        
        H0: the selected moment of series 1 is the same as the expected value.
        Ha: they are different. Therefore, their fractions of Trues and Falses
        are different.
    
     """)
    
    
    a = np.array([0.172, 0.142, 0.037, 0.453,
                  0.355, 0.022, 0.502, 0.2,
                  3, 0.72,  0.582, 0.198, 0.198,
                  0.597, 0.516, 0.815, 0.402, 0.605,
                  0.711, 0.614, 0.468])
    
    
    expected_value = 0.55
    
    p_value = compute_boostrap_pvalue(a, expected_value, 9999)
    
    print('pvalue: {2:.4f}'.format(np.mean(a), expected_value, p_value))

