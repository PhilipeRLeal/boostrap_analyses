
import numpy as np



def _bootstrap_replicate_1d(data, reducer):
    
    bs_sample = np.random.choice(data, len(data))
    
    return reducer(bs_sample)
    
def _draw_bs_reps(data,
                  reducer,
                  n_reps):
    
    perm_reps = np.empty(n_reps)
    
    
    for i in range(n_reps):
        perms = _bootstrap_replicate_1d(data, reducer=reducer)
        
        perm_reps[i] = perms
        
    return perm_reps
