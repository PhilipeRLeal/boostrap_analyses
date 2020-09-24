
import numpy as np
from permutation import draw_perm_reps

def diff_between_series(series1, series2, reducer=np.mean):
    
    return reducer(series1) - reducer(series2)

def frac_of_cases(series1):
    """
    Description:
        
        Compute fraction True cases from given data series
    
    Params:
        series1: an array of True and False cases:
            
        series2: it is not used. It is only there, 
                 so that the draw_perm_reps can work without major changes
                 
    """
    frac = series1[series1==True].size / (series1.size)
    return frac


def diff_frac(data_A, data_B):
    frac_A = frac_of_cases(data_A)
    frac_B = frac_of_cases(data_B)
    
    return frac_B - frac_A

def eval_permutation_pvalue(series_A, series_B,  
                            reducer=diff_frac,
                            n_samples=10000):
    
    
    diff_frac_obs = reducer(series_A, series_B)
    
    perm_replicates = np.empty(n_samples)
    
    for i in range(n_samples):
        perm_replicates[i] = draw_perm_reps(series_A,
                                            series_B, 
                                            reducer,
                                            size=1)
                                                   
    p_value = np.mean(perm_replicates >= diff_frac_obs)
    
    return {'p_value':p_value, 'perm_replicates':perm_replicates,'empirical_diff':diff_frac_obs}
    
    
    

if '__main__' == __name__:
    print(''' example case of AB test:
        
        You measure the number of people who click on an ad on your
        company's website before and after changing its color.
        
        prior: the series of clicks (True, False) prior to the change
        
        after: the series of clicks (True, False) after the change
        
        The sum of True represents the amount of clicks on the ad during the 
        time evaluated.
        
        A True represents someone that did click on your ad 
        A False represents someone that did not click on your ad 
        
    ''')
    
    
    prior = np.array([True] * 153 + [False] * 91)
    after = np.array([True] * 136 + [False] * 35)
    
    results = eval_permutation_pvalue(prior, after, reducer=diff_frac)
    
    print('p-value =', results['p_value'])
    
    ################
    
    
    
    
    
    
    
    n = '\n'*2 + '-'*40 + '\n'*2
    print(n, """Second case:
          
              Assume you measure the values of a given variable before and after a given
              update in your sistem.
              
              To measure the probability of that change having any effect over 
              the variable of interest, let's say: 
                  The amount of time a person lasts in your website
            
              We could do a permutation pvalue analyzes as follows:
                  
                  series 1: an array of entries, which each entry represents the amount of time a given
                  person spent in your website prior to a given change
                  
                  series 2: an array of entries, which each entry represents the amout of time
                  that a given person spent after the given change.
                  
              For this particular case, since it is no longer a True/False condition,
              the function to evaluate the potential difference between the two series
              would be something like: diff_between_series case, in which one
              could evaluate the difference of a given parameter of interest 
              between the series:
          

        
         """,n)
    
    series1 = np.random.normal(1,2,size=100)
    series2 = np.random.normal(3, 4, size=100)
    
    reducers = [np.mean, np.std, np.var, lambda x: np.percentile(x, 25)]
    
    for reducer in reducers:
        
    results = eval_permutation_pvalue(prior, after, reducer=diff_frac)
    
    print('p-value =', results['p_value'])
        results = eval_permutation_pvalue(series1, 
                                         series2, 
                                         reducer=lambda x, y: diff_between_series(x, 
                                                                               y, 
                                                                               reducer)
                                        )
        
        print(reducer.__name__, 'pvalue: {0:.3f}'.format( results['p_value']))
                           