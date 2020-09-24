
import numpy as np




def bootstrap_replicate_1d(data, func):
    return func(np.random.choice(data, size=len(data)))


def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""

    # Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data, func)

    return bs_replicates

def two_sample_bootstrap(series_1, series_2, n_samples=10000, alpha=0.05):
    
    '''Two sample test: 
        
    Description:
            test in which we are comparing the means of two different data-series,
            though not necessarily the given series have the same distribution
            (PDF distribution - family or parameters).
            
    How the test is done:
        To do the two-sample bootstrap test, 
        we shift both arrays to have the same mean, 
        since we are simulating the hypothesis that their means are, in fact, equal. 
        We then draw bootstrap samples out of the shifted arrays and 
        compute the difference in means. 
        
        This constitutes a bootstrap replicate, and we generate many of them.
        The p-value is the fraction of replicates with a difference 
        in means greater than or equal to what was observed.
        
            
    Example:
        you want to see if Frog B and Frog C have similar 
        impact forces (mean) in tongue projection for fly capture. 
        
        In here, you have Frog C's impact forces samples available.
        
    
    
    Parameters:
        series_1 (Array 1D): the series_1 from which we will test the hypothesis that mean(series_1) == mean(series_2)
                  is actually its mean.
        
        series_2 (Array 1D): the series_2 from which we will test the hypothesis that mean(series_1) == mean(series_2)
                  is actually its mean.
       
       
               
        n_samples (int - optional): number of permutations to check the probability.
        
        alpha (float == 0.05): confidence coefficient for rejecting the null hypothesis
        
    Returns:
        p-value of Ho being True ->>>> series_1 and series_2 have same mean
        
    '''
    
    # Compute the empirical_diff_means:
    
    empirical_diff_means = np.mean(series_1) - np.mean(series_2)
    
    # Compute mean of all forces: concat_mean
    
    concat = np.concatenate([series_1, series_2])
    
    concat_mean = np.mean(concat)
    
    # Generate shifted arrays
    series_1_shifted = series_1 - np.mean(series_1) + concat_mean
    series_2_shifted = series_2 - np.mean(series_2) + concat_mean
    
    # Compute 10,000 bootstrap replicates from shifted arrays
    bs_replicates_a = draw_bs_reps(series_1_shifted, np.mean, size=10000)
    bs_replicates_b = draw_bs_reps(series_2_shifted, np.mean, size=10000)
    
    # Get replicates of difference of means: bs_replicates
    bs_replicates = bs_replicates_a - bs_replicates_b
    
    # Compute and print the probability of getting a boostrap more extreme than the observed:
        # the p-value:
    p_value = np.sum(bs_replicates >= empirical_diff_means) / len(bs_replicates)
 

    if p_value <= alpha:
        print('''The low p-value ({0:0.3%}) suggest that the null hypothesis, 
          that the given mean and the series-data have the same mean, is false.
             
          '''.format(p_value))
    else:
        print('''The high p-value ({0:0.3%}) suggest that the null hypothesis, 
              that the given mean and the series-data have the same mean, is True.
                 
              '''.format(p_value))
     
    
    return p_value


if '__main__' == __name__:
    A = np.random.normal(size=100)
    two_sample_bootstrap(A, A)