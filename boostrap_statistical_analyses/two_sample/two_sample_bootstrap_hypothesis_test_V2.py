

import numpy as np
from scipy.stats import ttest_ind, f_oneway



def get_zscore(x, y):
    
    n = np.size(x)
    
    mu = 0 # expected value for Ho == True, in which the difference between the two population samples is 0:
    
    difObs = x - y
    
    funcObs = func(difObs)
    
    varObs = np.sum(((difObs - funcObs)**2))/(n-1) 
    
    tObs = (funcObs - mu)/(np.sqrt(varObs/n))
    
    return tObs
    
    
    

def boostrap_PDF_moments_comparison(prior_test_data, 
                                    after_test_data, 
                                    func=np.mean, 
                                    n_repeats=10000, 
                                    alpha=0.05):
    
    '''
    Description: 
        
        This function applies the Bootstrap hyphothesis testing,
                 according to:
                     
                     
    "O uso da técnica bootstrap como alternativa ao teste-t paramétrico"
    \t\t (Danny A. V. Tonidandel 02 de julho de 2017.)
                
                
    
    It verifies whether two given series have a same probability moment 
    (i.e.:mean, variance, standard deviation...)
    
    
    Parameters:
        
        prior_test_data (np.array or pandas series)
        
        after_test_data (np.array, pandas series)
        
        func (reducer): a callable reducer
            standard  == np.mean
        
        n_repeats (int): The number of repetitions to apply the boostrap
            standard == 10000
        
        alpha (float): the confidence interval
            standard == 0.05
    
    Returns: 
        
        p-value1 from uni-lateral test
        
        empirical pvalue from the right portion of the PDF (Pires e Branco, 1996)
    
        T-test pvalue: the empirical p-value of the t-test.
    '''
    
    
    
    n = np.size(prior_test_data)
    
    mu = 0 # expected value for Ho == True, in which the difference between the two population samples is 0:
    
    after_test_data = after_test_data[:n]
    
    tObs = get_zscore(prior_test_data, after_test_data)
    
    # BOOSTRAP - realiza o teste t pareado para as B amostras de boostrap 
    
    resultado = np.empty(shape=n_repeats)
    
    # Iterando sobre as N repetições:
    
    for i in range(n_repeats):
        
        amostraA = np.random.choice(prior_test_data, size=n, replace=True)
        amostraB = np.random.choice(after_test_data, size=n, replace=True)
        
        # Calculo da estattistica T sob H0 
        
        resultado[i] = get_zscore(amostraA, amostraB)
        
        
    
    
    # Calcula p-valor (sob H0) para o teste unilateral 
    
    sob_H0 = resultado - np.mean(resultado)
    
    pvalorD = np.sum(sob_H0 > tObs)/n_repeats 
    
    print("p-valor (sob H0): {0}".format(np.round(pvalorD, decimals=5)))
    
    # Calcula pvalor empirico à direita segundo (Pires e Branco, 1996) 
    
    pvalorD2 = np.sum(boots_PDF_moment > 0)/n_repeats 
    
    print("p-valor empírico: {0}".format(np.round(pvalorD2, decimals=5)))
    
    t_alpha = np.quantile(resultado,alpha) 
    
    ICD = funcObs - (t_alpha * np.sqrt(varObs/n) )
    
    print("Intervalo de confiança a 5%: {0} : {1}".format( np.round(ICD, decimals=5),"infinito"))
    
    
    if pvalorD <= alpha:
        print('''Para o nível de signicância especificado (alpha), \
e pelo método do valor p (pvalor < alpha), a hipótese nula deve ser rejeitada. 
              
Em outras palavras, há evidências para afirmar que as "{0}s" de ambas populações são diferentes. 
              '''.format(func.__name__))
        
    else:
        print('''Não há evidências de que as populações tenham médias diferentes
              ''')
    
    print('\n'*3, '-'*30, '\n')
        
    # Doing the old empirical T-test (mean test) for the data:    
    
    ANOVA_test = f_oneway(A,B)
    
    if ANOVA_test[1] < alpha:
        variance = True
    else:
        variance=False
    
    if func.__name__ == 'mean':
        
        Ttest_pvalue = ttest_ind(A,B, equal_var=variance)
        
    
        Results = {'Unilateral_pvalue':pvalorD, 
            'Empirical_pvalue':pvalorD2, 
            'Ttest_pvalue':Ttest_pvalue[1]}
        
    elif func.__name__ == 'var':
        
        Results = {'Unilateral_pvalue':pvalorD, 
            'Empirical_pvalue':pvalorD2, 
            'Ftest_pvalue':ANOVA_test[1],
            }

    Results['reducer'] = func.__name__
    
    return Results


if '__main__' == __name__:
    
    A = np.random.normal(size=100)
    B = np.random.normal(size=100)
    
    Concat = np.vstack((A,B))
    import pandas as pd
    
    df = pd.DataFrame(Concat.T, columns=['antes', 'depois'])
    
    df.to_csv(r'C:\Users\lealp\Downloads\temp\data.csv')
    
    
    ##############
    prior_test_data = A
    after_test_data = B
    funcs = [np.mean, np.var]
    
    n = np.size(prior_test_data)
    
    
    for func in funcs:
        Results = boostrap_PDF_moments_comparison(prior_test_data, 
                                                  after_test_data, 
                                                  func=func)
        
        
       
        print(Results)
        
    

