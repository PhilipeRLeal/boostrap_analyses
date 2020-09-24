
import numpy as np
from pvalue_for_AB_test import draw_perm_reps, frac_of_cases


def get_pvalue_for_AB_test(series1, 
                           series2, 
                           func=frac_of_cases,
                           n_reps=999):
    '''
    Description:
        This functin 
    
    

    Parameters
    ----------
    series1 : TYPE bool Array
        DESCRIPTION.
        
    series2 : TYPE bool Array
        DESCRIPTION.
        
    n_reps : TYPE (int), optional.
        DESCRIPTION. The default is 999. The number of replicates it will do
        

    Returns
    -------
    p : TYPE (float)
        DESCRIPTION: it represents the probability of observing 
        a test statistic equally or more extreme 
        than the one observed, 
        given that the null hypothesis is true.
        
        H0: both series (series 1 and series 2) are the same.
        Ha: they are different. Therefore, their fractions of Trues and Falses
        are different.

    '''
    
    # Acquire permutation samples: perm_replicates
    perm_replicates = draw_perm_reps(series1, series2, 
                                     func, n_reps)
    
    n = series1.size
    conditional_cases = series1[series1==True].size
    # Compute and print p-value: p
    p = np.mean(perm_replicates <= conditional_cases/n)
    
    
    
    return p

def diff_between_series(series1, series2, reducer=np.mean):
    
    return reducer(series1) - reducer(series2)


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
    
    pvalue = get_pvalue_for_AB_test(prior, after, func=frac_of_cases)
    
    print('p-value =', pvalue)
    
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
        
        p_value = get_pvalue_for_AB_test(series1, 
                                         series2, 
                                         func=lambda x, y: diff_between_series(x, 
                                                                               y, 
                                                                               reducer)
                                        )
        
        print(reducer.__name__, 'pvalue: {0:.3f}'.format( p_value))
                           

    