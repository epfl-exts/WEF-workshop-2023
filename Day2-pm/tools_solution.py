
import pymc as pm
import numpy as np

#---------------------------------------------


def get_posterior_ab(priors, trials, successes):

    """Get traces from a PyMC model.
    
    Parameters
    ----------
    
        
    Returns
    -------
    trace : posterior from the model.
    """
    with pm.Model() as model:   

        theta = pm.Beta("theta", 
                        alpha = priors[0], 
                        beta  = priors[1], 
                        shape = 2)
        
        pm.Binomial("y", 
                    n        = trials, 
                    p        = theta, 
                    observed = successes,
                    shape    = 2)
        
        pm.Deterministic("uplift", theta[1] / theta[0] - 1)
        
        # Draw samples from the posterior
        trace = pm.sample(draws=5000, return_inferencedata=True, progressbar=False)

    return trace
#---------------------------------------------
def get_posterior_abc(priors, trials, successes, variants):

    """Get traces from a PyMC model.
    
    Parameters
    ----------
    
        
    Returns
    -------
    trace : posterior from the model.
    """
    with pm.Model() as model:   

        theta = pm.Beta("theta", 
                        alpha = priors[0], 
                        beta  = priors[1], 
                        shape = len(variants))
        
        pm.Binomial("y", 
                    n        = trials, 
                    p        = theta, 
                    observed = successes,
                    shape    = len(variants))
        
        uplift = []
            
        for i in range(len(variants)):
            others = [theta[j] for j in range(len(variants)) if j != i]
            if len(others) > 1:
                comparison = pm.math.maximum(*others)
            else:
                comparison = others[0]

            uplift.append(pm.Deterministic(f"uplift_{i}", theta[i] / comparison - 1))

        
        # Draw samples from the posterior
        trace = pm.sample(draws=5000, return_inferencedata=True, progressbar=False)

    return trace
#---------------------------------------------

def sample_size_effect(sample_sizes, prior, successes_rate):

    trace_all = {}

    for n in sample_sizes:
        trace_all[n] =  get_posterior_ab( priors    = prior, 
                                        trials   = [n, n], 
                                        successes= np.dot(successes_rate,n))
    return trace_all

#---------------------------------------------
