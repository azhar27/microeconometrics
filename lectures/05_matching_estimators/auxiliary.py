import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from collections import OrderedDict

a_grid = np.linspace(0.01, 1.00, 100)
b_grid = np.linspace(0.01, 1.00, 100)

def get_potential_outcomes(a, b):
    """ Get potential outcomes.
    
    This function calculates the potential outcomes based on the 
    functional from as described in our textbook on p. 153.
    
    Args:
        a: a float
        b: a float
    
    Returns:
        A list with the individuals potential outcomes.
    """
    v_0, v_1 = np.random.normal(0, 5, size=2)
    y_0 = 100.0 + 3.0 * a + 2.0 * b + v_0
    y_1 = 102.0 + 6.0 * a + 4.0 * b + v_1
    return [y_1, y_0]
    


def get_sample_matching_demonstration_3():
    sample = list()
    
    counts = np.tile(np.nan, (3, 100, 100))
    
    for i, a in enumerate(a_grid):
        for j, b in enumerate(b_grid):

            prob = get_propensity_score(a, b)

            # Now we determine the number of observed individuals
            for k, is_treat in enumerate([True, False]):
                if is_treat:
                    lambda_ = prob
                else:
                    lambda_ = 1.0 - prob

                num_sample = np.random.poisson(lambda_)
                counts[k, i, j] = num_sample
                
                for _ in range(num_sample):
                    d = np.random.choice([1, 0], p=[prob, 1 - prob])
                    y_1, y_0 = get_potential_outcomes(a, b)
                    y = d * y_1 + (1 - d) * y_0

                    sample += [[a, b, d, y, y_1, y_0, prob]]
            counts[2, i, j] = np.sum(counts[:2, i, j])
            
    df = pd.DataFrame(sample, columns=['a', 'b', 'd', 'y', 'y_1', 'y_0', 'prob'])
    return df, counts

def get_propensity_score(a, b):
    """ Get probensity score.
    
    This function calculates the propensity based on the
    functional form as described in our textbook on p. 153.
    
    Args:
        a: a float
        b: a float
    
    Returns:
        A float with the individuals propensity score.
    """
    index = 0
    index += -2.0 + 3.0 * a - 3.0 * (a - 0.1) + 2.0 * (a - 0.3)
    index += -2.0 * (a - 0.5) + 4.0 * (a - 0.7) - 4.0 * (a - 0.9)
    index += +1.0 * b - 1.0 * (b - 0.1) + 2.0 * (b - 0.7)
    index += -2.0 * (b - 0.9)  + 3.0 * (a - 0.5) * (b - 0.5)
    index += -3.0 * (a - 0.7) * (b - 0.7)
    
    prob = np.exp(index) / (1.0 + np.exp(index))
    
    return prob

def plot_propensity_score(a_grid, b_grid):

    X, Y = np.meshgrid(*(a_grid, b_grid))
    Z = get_propensity_score(X, Y)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 500)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlim([0, 1])
    ax.set_zlabel('Propensity Score');
    
    
def get_sample_matching_demonstration_1(num_agents):
    def get_potential_outcomes(s):
        if s == 1:
            y_1, y_0 = 4, 2
        elif s == 2:
            y_1, y_0 = 8, 6
        elif s == 3:
            y_1, y_0 = 14, 10
        else:
            raise AssertionError
            
        # We want some randomness
        y_1 += np.random.normal()
        y_0 += np.random.normal()
                
        return y_1, y_0

        
    data = np.tile(np.nan, (num_agents, 5))
    for i in range(num_agents):
        u = np.random.uniform()

        if 0.00 <= u < 0.36:
            s, d = 1, 0
        elif 0.36 <= u < 0.48:
            s, d = 2, 0
        elif 0.48 <= u < 0.60:
            s, d = 3, 0
        elif 0.60 <= u < 0.68:
            s, d = 1, 1
        elif 0.68 <= u < 0.80:
            s, d = 2, 1
        else:
            s, d = 3, 1


        y_1, y_0 = get_potential_outcomes(s)
        y = d * y_1 + (1 - d) * y_0  
        
        data[i, :] = y, d, s, y_1, y_0

    info = OrderedDict()
    info['Y'] = np.float
    info['D'] = np.int
    info['S'] = np.int
    info['Y_1'] = np.float
    info['Y_0'] = np.float
    
    df = pd.DataFrame(data, columns=info.keys())
    df = df.astype(info)
    return df

def get_sample_matching_demonstration_2(num_agents):
    def get_potential_outcomes(s):
        if s == 1:
            y_1, y_0 = -99, 2
        elif s == 2:
            y_1, y_0 = 8, 6
        elif s == 3:
            y_1, y_0 = 14, 10
        else:
            raise AssertionError
            
        # We want some randomness
        y_1 += np.random.normal()
        y_0 += np.random.normal()
                
        return y_1, y_0

        
    data = np.tile(np.nan, (num_agents, 5))
    for i in range(num_agents):
        u = np.random.uniform()

        if 0.00 <= u < 0.40:
            s, d = 1, 0
        elif 0.40 <= u < 0.50:
            s, d = 2, 0
        elif 0.50 <= u < 0.60:
            s, d = 3, 0
        elif 0.60 <= u < 0.73:
            s, d = 2, 1
        else:
            s, d = 3, 1


        y_1, y_0 = get_potential_outcomes(s)
        y = d * y_1 + (1 - d) * y_0  
        
        data[i, :] = y, d, s, y_1, y_0

    info = OrderedDict()
    info['Y'] = np.float
    info['D'] = np.int
    info['S'] = np.int
    info['Y_1'] = np.float
    info['Y_0'] = np.float
    
    df = pd.DataFrame(data, columns=info.keys())
    df = df.astype(info)
    df.replace(-99, np.nan, inplace=True)
    
    return df

def get_sparsity_pattern_overall(counts):
    fig, ax = plt.subplots(1, 1)
    ax.spy(counts[2, :, :])
    ax.set_title('Sparsity pattern', pad=15)
    
def get_sparsity_pattern_by_treatment(counts):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.spy(counts[0, :, :])
    ax1.set_title('Treated', pad=15)

    ax2.spy(counts[1, :, :])
    ax2.set_title('Untreated', pad=15)

    fig.suptitle('Sparsity pattern')