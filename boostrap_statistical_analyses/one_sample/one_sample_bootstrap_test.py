
import numpy as np


def bootstrap_replicate(data, func):
    return func(np.random.choice(data, size=len(data)))


def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""

    # Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate(data, func)

    return bs_replicates


def one_sample_bootstrap_test(series_1, expectedmean, n_replicates=10000, alpha=0.05):
    '''One sample test: 
        
    Description:
            test in which we are comparing a single mean value to be 
            the mean of a third party series data. In another words, checking the 
            probability of a given mean value to be the mean of a given
            data-series
            
    Example:
        you want to see if Frog B and Frog C have similar 
        impact forces in tongue projection for fly capture. 
        
        Unfortunately, you do not have Frog C's impact forces samples available, 
        but you know they have a mean of 0.55 N. 
                
        Because you don't have the original data, 
        you cannot do a permutation test, and you cannot assess the hypothesis
        that the forces from Frog B and Frog C come from the same distribution. 
        
        You will therefore test another, less restrictive hypothesis: 
            The mean strike force of Frog B is equal to that of Frog C.
    
    
    Parameters:
        series_1: the series from which we will test the hypothesis that meanY
        is actually its mean.
        
        expectedmean: a given value that is assumed to be a candidate for mean of the 
               given series_1
               
        n_replicates (int - optional): number of permutations to check the probability.
        
    Returns:
        p-value of Ho being True ->>>> Therefore, meanY being actually the mean
        of series_1.
        
    '''
    
    
    shifted = series_1 - np.mean(series_1) + expectedmean
    
    bs_replicates = draw_bs_reps(shifted, np.mean, n_replicates)
    
    p_value = np.sum(bs_replicates <= np.mean(series_1)) / n_replicates
    
    if p_value <= alpha:
        print('''The low p-value ({0:0.3%}) suggest that the null hypothesis, 
              that the given mean and the series-data have the same mean, is False.
                 
              '''.format(p_value))
    else:
        print('''The high p-value ({0:0.3%}) suggest that the null hypothesis, 
              that the given mean and the series-data have the same mean, is True.
                 
              '''.format(p_value))
     
    return p_value




if '__main__' == __name__:
    A = np.random.normal(size=100) + 5
    
    
    expectedmean = 1
    
    p_value = one_sample_bootstrap_test(A, expectedmean)
    