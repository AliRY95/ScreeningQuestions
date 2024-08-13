import numpy as np

def prob_rain_more_than_n(p, n):
    if n >= len(p):
        """
        The probability of having more rainy days
        than the total number of days is zero, even
        in Vancouver!
        """
        return 0
    if n < 0: 
        """
        The probability of having atleast 0 (or fewer)
        rainy days is 1
        """
        return 1
    
    """
    Calculating of having exactly j rainy days in the
    first i days of the year
    """
    prob_grid = get_prob_grid(p)
   
    """
    The probability of having more than n rainy days
    is 1 minus the probabilty of having n or fewer
    rainy days
    """
    return 1 -  np.sum(prob_grid[-1, :n+1])
    


def get_prob_grid(p):
    """
    Returns a grid g, such that g[i,j]
    is the probability of having exactly
    j rainy days in the first i days
    """
    total_days = len(p)
    g = np.zeros((total_days + 1,
                  total_days + 1))

    # The base case, the probability of 0 occurance of 0 events
    g[0,0] = 1

    # Filling the grid
    for i in range(1, total_days + 1):
        """
        The probability of having more than i rainy days
        in the first i days is zero, if j>i: g[i,j] = 0 
        """
        for j in range(i + 1):
            """
            Probability that the i-th day is not rainy, given
            that there's been j rainy days in the first i - 1
            days
            """
            g[i,j] = (1 - p[i-1]) * g[i-1,j]
            if j == 0:
                continue
            """
            Probability that the i-th day is rainy, so there
            should be j-1 rainy days in the first i-1 days
            """
            g[i,j] += p[i-1] * g[i-1,j-1]

    return g


if __name__ == '__main__':

    # Parameters
    num_days = 365
    #last year Vancouver had 160 rainy days
    #160/365 ~ 0.44
    mean_probability = 0.44
    amplitude = 0.2  # Amplitude of the seasonal change
    random_noise_std = 0.05  # Standard deviation of random noise

    # Generate a seasonal trend using a sinusoidal function
    # The period is 365 days, and the phase shift ensures the cycle starts in January
    days = np.arange(num_days)
    seasonal_trend = mean_probability + amplitude * np.sin(2 * np.pi * (days / num_days) + np.pi)

    # Add random noise
    random_noise = np.random.normal(0, random_noise_std, num_days)

    # Combine the seasonal trend and random noise
    rain_probabilities = seasonal_trend + random_noise

    # Clip the values to ensure they are within the probability range [0, 1]
    p = np.clip(rain_probabilities, 0., 1)    
    n = 160    
    probability = prob_rain_more_than_n(p,n)

    print(f'The probability of raining more than {n} days is {probability}')

