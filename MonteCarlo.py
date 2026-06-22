from scipy import stats
import numpy as numpy

def T_TestMonteCarloSampleSize(alpha: float = .05, power: float= .80, cohens_d: float= 0, iterations = 1000) -> str:

    '''
    Given an alpha level, desried power level, and Cohen's d, this function uses Monte Carlo simulation to iteratively
    find the sample size that yields that desired power level.
    '''

    # Initialize the starting sample size as 2. T-tests require a mean and SD which is not possible with n = 1.
    n = 2

    while True:
        # Collect the number of significant T-tests.
        SignificanceCounts = 0

        # Grab 2 random samples from 2 normal distributions according to the inputted Cohen's d and calculate their T-test
        # If significant you increase the SignificanceCounts by 1. Repeat this sampling, t-testing, and recording sig 1000 times.
        for i in range(iterations):
            Tensor1 = numpy.random.normal(0, 1, n)
            Tensor2 = numpy.random.normal(cohens_d, 1, n)
            TestStat = stats.ttest_ind(Tensor1, Tensor2, equal_var=True)

            if TestStat.pvalue < alpha:
                SignificanceCounts += 1

        # Power is defined as the probability of finding a sig effect given one exists. We can calculate this by seeing
        # how many times there was a sig effect over the 1000 iterations.
        EstimatedPower = SignificanceCounts / iterations

        # If this Monte Carlo estimated power is at the desired power level, return that sample size
        if EstimatedPower >= power:
            return f'Total Sample Size: {n*2}; Group Sample Size: {n}'
        # Otherwise, we increase the sample size by 1, reset the significance counts, and try doing that 1000 t-test procedure
        # with this new n.
        else:
            n +=1

def T_TestMonteCarloAchievedPower(alpha: float = .05, cohens_d: float= 0, iterations = 1000, total_N = 0):
    '''Given an alpha level, Cohen's d, and the total_N of your study, this function calculates the achieved power.'''

    n = int(total_N/2)
    SignificanceCounts = 0

    # Using the sample size, repeatedly sample and calculate t-tests according do your Cohen's d and count up how many are sig.
    for i in range(iterations):
        Tensor1 = numpy.random.normal(0, 1, n)
        Tensor2 = numpy.random.normal(cohens_d, 1, n)
        TestStat = stats.ttest_ind(Tensor1, Tensor2, equal_var=True)

        if TestStat.pvalue < alpha:
            SignificanceCounts += 1
    
    # Power would be the proportion of t-tests that were sig.
    AchievedPower = SignificanceCounts/iterations
    return f'{AchievedPower*100}%'
