
import pymc as pm
import numpy as np
import pandas as pd

from scipy.stats import bernoulli, expon
from dataclasses import dataclass

@dataclass
class RevenueData:
    visitors: int
    purchased: int
    total_revenue: float

#---------------------------------------------HANDS ON 1


def get_posterior(priors, trials, successes):

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

#---------------------------------------------HANDS ON 2

def get_data(variants, true_conversion_rates, true_mean_purchase, samples_per_variant):

    # step 1: simulate data based on conversion rates and mean purchase
    converted = {}
    mean_purchase = {}
    
    for variant, p, mp in zip(variants, true_conversion_rates, true_mean_purchase):
        
        converted[variant] = bernoulli.rvs(p, size=samples_per_variant)
        print('generated',samples_per_variant, 'obs from a Bernoulli rv based on', p, 'rate for variant', variant)
        
        mean_purchase[variant] = expon.rvs(scale=mp, size=samples_per_variant)
        print('generated',samples_per_variant, 'obs from an Exponential rv based on', mp, 'for variant', variant)
        print('----------------------------------------------------------------------')

    converted     = pd.DataFrame(converted)
    mean_purchase = pd.DataFrame(mean_purchase)
    revenue = converted * mean_purchase

    # step 2: put this together with a dataclass
    generated = pd.concat([
        converted.aggregate(["count", "sum"]).rename(index={"count": "visitors", "sum": "purchased"}),
        revenue.aggregate(["sum"]).rename(index={"sum": "total_revenue"}),
                            ])

    print('\n Below is the outcome and we are now going to use them as input in the PyMC model:')
    display(generated.round())

    data = [RevenueData(**generated[v].to_dict()) for v in variants]

    visitors      = [d.visitors for d in data]
    purchased     = [d.purchased for d in data]
    total_revenue = [d.total_revenue for d in data]

    return purchased, total_revenue
    


def get_posterior2(beta_priors, 
                    gamma_priors,
                    visitors,
                    purchased,
                    total_revenue):

    with pm.Model() as model:

        #------------------------------------------------conversion rate model
        # Priors for unknown model parameters
        theta = pm.Beta("theta", 
                        alpha = beta_priors[0], 
                        beta  = beta_priors[1], 
                        shape = 2)
        
        # Likelihood of observations
        converted = pm.Binomial("converted", 
                                n        = visitors,      # total visitors
                                observed = purchased,     # total visitors converted
                                p        = theta,         # chance they convert
                                shape    = 2)  
        
        #------------------------------------------------revenue model
        # Priors for unknown model parameters
        lamda = pm.Gamma( "lamda", 
                        alpha = gamma_priors[0],
                        beta  = gamma_priors[1],
                        shape = 2)
        
        # Likelihood of observations
        revenue = pm.Gamma("revenue", 
                            alpha    = purchased,            # total visitors converted
                            observed = total_revenue, 
                            beta     = lamda, 
                            shape    = 2)        
        
        # get the revenue per visitor
        revenue_per_visitor = pm.Deterministic("revenue_per_visitor", theta / lamda)

        #------------------------------------------------relative uplifts
        # get the uplifts
        theta_uplift = pm.Deterministic(f"theta uplift", theta[1] / theta[0] - 1)
        lamda_uplift = pm.Deterministic(f"lamda uplift", (1 / lamda[1]) / (1 / lamda[0]) - 1)
        uplift       = pm.Deterministic(f"uplift", revenue_per_visitor[1] / revenue_per_visitor[0] - 1)

        #------------------------------------------------posterior
        # draw posterior samples
        trace = pm.sample(draws=5000, return_inferencedata=True, progressbar=False, chains=4)

    return trace