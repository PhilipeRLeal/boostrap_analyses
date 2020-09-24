# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:23:54 2020

@author: Philipe_Leal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 

path = os.path.join(os.getcwd(), 'Data_example.csv')
df = pd.read_csv(path, sep=',', decimal='.', encoding='latin')

print(df.head())


#########3
import seaborn as sns

# Create bee swarm plot
years = np.array([df['Year'].min(), df['Year'].max()])

def year_grouper(date):
    
    if date <= years.mean():
        return 1974
    
    else:
        return 2012

groups = []
for idx, group in df.set_index('Year').groupby(year_grouper):
    group = group.copy()
    group['year'] = idx
    group.set_index('year', drop=True, inplace=True)
    group.reset_index(inplace=True)
    groups.append(group)
    
df = pd.concat(groups )


print(df.head())


_ = sns.swarmplot(x='year', y='Beak length',
data=df)

# Label the axes
_ = plt.xlabel('Year')
_ = plt.ylabel('beak length (mm)')

# Show the plot
plt.show()



########## Compargin the mean between populations:




bd_1975 = df.loc[df['year'] == 1974, 'Beak length']
bd_2012 = df.loc[df['year'] == 2012, 'Beak length']

# Compute the difference of the sample means: mean_diff
mean_diff = np.mean(bd_2012) - np.mean(bd_1975)

# Get bootstrap replicates of means

from bootstrap_replicate import _draw_bs_reps

n_reps = 10000
bs_replicates_1975 = _draw_bs_reps(bd_1975, np.mean, n_reps)
bs_replicates_2012 = _draw_bs_reps(bd_2012, np.mean, n_reps)

# Compute samples of difference of means: bs_diff_replicates
bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975

# Compute 95% confidence interval: conf_int
conf_int = np.percentile(bs_diff_replicates, [2.5, 97.5])

# Print the results
print('difference of means =', mean_diff, 'mm')
print('95% confidence interval =', conf_int, 'mm')



# Compute mean of combined data set: combined_mean
combined_mean = np.mean(np.concatenate((bd_1975, bd_2012)))

# Shift the samples
bd_1975_shifted = bd_1975 - np.mean(bd_1975) + combined_mean
bd_2012_shifted = bd_2012 - np.mean(bd_2012) + combined_mean

n_reps = 10000

# Get bootstrap replicates of shifted data sets
bs_replicates_1975 = _draw_bs_reps(bd_1975_shifted, np.mean, n_reps)
bs_replicates_2012 = _draw_bs_reps(bd_2012_shifted, np.mean, n_reps)

# Compute replicates of difference of means: bs_diff_replicates
bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975

# Compute the p-value
p = np.mean(bs_diff_replicates >= mean_diff)

# Print p-value
print('p =', p)

print('''Notice that the p_value is non-significant. Therefore, assuming that 
      the peak size changed something around {0} in only 40 years,
      a diminishment of 50% could happen in only 400 years'''.format(mean_diff))