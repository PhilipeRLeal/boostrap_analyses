
import numpy as np



def diff_of_means(data_1, data_2):
    """Difference in means of two arrays."""

    # The difference of means of data_1, data_2: diff
    diff = np.mean(data_1) - np.mean(data_2)

    return diff    


def _permutation_sample(data):
    
    
    permuted_data = np.random.permutation(data)
    
 
    return permuted_data


def permutation_over_two_series(data1, data2):
    """Generate a permutation sample from two data sets."""

    # Concatenate the data sets: data
    data = np.concatenate((data1, data2))

    # Permute the concatenated array: permuted_data
    permuted_data = _permutation_sample(data)

    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]

    return perm_sample_1, perm_sample_2


def draw_perm_reps(data_1, data_2, func, size=1):
    """Generate multiple permutation replicates."""

    # Initialize array of replicates: perm_replicates
    perm_replicates = np.empty(size)

    for i in range(size):
        # Generate permutation sample
        perm_sample_1, perm_sample_2 = permutation_over_two_series(data_1, data_2)

        # Compute the test statistic
        perm_replicates[i] = func(perm_sample_1, perm_sample_2)

    return perm_replicates
    


def eval_permutation_p_value(samples_A, samples_B, reducer=diff_of_means, size=10000, condition='gt'):


    # Compute difference of mean impact force from experiment: empirical_diff_means
    empirical_diff_means = reducer(samples_A, samples_B)

    # Draw 10,000 permutation replicates: perm_replicates
    perm_replicates = draw_perm_reps(samples_A, samples_B,
                                     reducer, size=size)

    # Compute p-value:
        # the p_value is the sum of all positive cases divided by the 
        #number of samples
        # the positive cases are those whose perm_replicate value is equal 
        #or higher (more extreme) than the observed value.
    
    
    if condition.lower() == 'gt':
    
        p_value = np.mean(perm_replicates >= empirical_diff_means)
        
    elif condition.lower() == 'lt':
        p_value = np.mean(perm_replicates <= empirical_diff_means)
        
    else:
        mask1 = perm_replicates <= empirical_diff_means
        
        mask2 = perm_replicates >= empirical_diff_means
    
        Conditional = perm_replicates[mask1 | mask2]
        p_value = np.sum(Conditional)/len(perm_replicates)

    
    return {'p_value':p_value, 
            'perm_replicates':perm_replicates,
            'empirical_diff_means':empirical_diff_means}

    
if '__main__' == __name__:
    """
    Description:
    
        Assuming that we wish to evaluate the probability that two 
        populations have same statistics (i.e.: mean).
        
        A possible solution for this hypothesis test is the t-statistics. 
        
        Another solution is the permutation replicate technique using a 
        mean difference as a reducer function.
    
    
    Case example:
        samples_A: samples from population A (i.e.: petal length without treatment)
        samples_B: samples from population B (i.e.: petal length with treatment)
        
        
        Reducer: diff_of_means. It evaluates the difference between 
        Population Means
    
    
        H0: Population means are the same
        Ha: Population means are not equal
    
    Result: 
        p_value (reprents the probability of retrieving a value more extreme
                 than the observed, assuming that hypothesis null is True.
        
        When we assume alpha == 0.05, if p_value < alpha, we reject H0,
        and accept the alternative (Ha).
        
        
    """
    
    
    print('''Case example:
        samples_A: samples from population A (i.e.: petal length without treatment)
        samples_B: samples from population B (i.e.: petal length with treatment) 
        
        '''
        )
    
    samples_A = np.random.normal(4, 5, size=500)
    
    samples_B = np.random.normal(3.7, 7.5, size=500)

    # Compute difference of mean impact force from experiment: empirical_diff_means
    empirical_diff_means = diff_of_means(samples_A, samples_B)

    # Draw 10,000 permutation replicates: perm_replicates
    perm_replicates = draw_perm_reps(samples_A, samples_B,
                                     diff_of_means, size=10000)

    # Compute p-value: p
    p_value = np.mean(perm_replicates >= empirical_diff_means)

    print(perm_replicates)
    # Print the result
    print('p-value =', p_value)
    
    
    
    
if '__main__' == __name__:
    # Case 2 (Bernoulli situation)
    
    """
    Description:
    
        Assume that a given population A (democrats - dems) have a 
        certain tendency towards voting in favor (boolean False X True) 
        for a given Legislation, and population B (republicans - reps) 
        have a second tendency.


        We wish to evaluate the probability that the populations have equal 
        tendency in the voting.
        
        
    Conditions:
    
        Since it is a Bernoulli situation, the differences in population 
        does no longer apply for this test.
        
        It is necessary to evaluate the respective frequencies of voting 
        per group:
    
        
        
        
    """
    print('''
          \n\n 
          
          ---------------------------------------------------
          
          Description:
    
        Assume that a given population A (democrats - dems) have a 
        certain tendency towards voting in favor (boolean False X True) 
        for a given Legislation, and population B (republicans - reps) 
        have a second tendency.


        We wish to evaluate the probability that the populations 
        have equal tendency in the voting.
        
        
        \n\n
        
        ------------------------------------ \n'''
        )
        
    # Construct arrays of data: dems, reps
    dems = np.array([True] * 153 + [False] * 91)
    reps = np.array([True] * 136 + [False] * 35)
    
    
    
    def frac_yea_dems(group_A, group_B=None):
        """Compute fraction of group_A."""
        frac = group_A[group_A==True].size / (group_A.size)
        return frac

    # Acquire permutation samples: perm_replicates
    perm_replicates = draw_perm_reps(dems, reps, frac_yea_dems, 10000)
    real_fraction = frac_yea_dems(dems)
    # Compute and print p-value: p
    p = np.sum(perm_replicates <= real_fraction) / len(perm_replicates)
    print('p-value =', p)

if '__main__' == __name__:
    """
    Description:
    
        population A: each sample from population A represents the 
        amount of time (in accumulated months) that a given event reoccurs.
        
        After a given treatment, which could have changed the rates 
        in the events of population A, a second sample set (Population B)
        was evaluated.
        
        
    Question:
        Is there a significant statistical change prior and after the 
        treatment?
        
        In another words: what is the probability that the treatment 
        causes a negative change in the event occurence given that the null hypothesis is true 

    
    
    
    Condition: 
        since the treatment changed the rates in the events in a negative 
        way (i.e., longer average time between event occurrence), we are interested in the "<=" condition for p-value test statistics
        
        
    
    Hypothesis:
        H0: treatment does not change the rates in the events occurence. 
        In another words, rates of Population A are equal to Population B:
        Ha: the treatment does change the rates
    """
    
    
    print('''
          \n\n 
          
          Description:
    
        population A: each sample from population A represents the 
        amount of time (in accumulated months) that a given event reoccurs.
        
        After a given treatment, which could have changed the rates in 
        the events of population A, a second sample set (Population B) 
        was evaluated.
        
        
    Question:
        Is there a significant statistical change prior and after the treatment?
        
        In another words: what is the probability that the treatment 
        causes a negative change in the event occurence given that 
        the null hypothesis is true 

    
    
        \n\n
        
        ------------------------------------ \n'''
        )
    
    
    
    eval_permutation_p_value(samples_A, samples_B, reducer=diff_of_means, size=10000, condition='gt')
    
    
    
if '__main__' == __name__:
    """
    Correlation test statistics
    
    
    Description:
    
        In this example, the statistical confidence (p-value) of the 
        correlation coefficient is evaluated.
        
        
    The condition evaluated is:
        what is the probability of getting a correlation 
        coefficient equal or higher than the observed? 
    
    """
    
    def pearson_r (x,y):
        
        return np.corrcoef(x,y)[0][1]
    
    Result = eval_permutation_p_value(samples_A, samples_B, reducer=pearson_r, size=10000, condition='gt')
    
    print('p_value =', Result['p_value'])