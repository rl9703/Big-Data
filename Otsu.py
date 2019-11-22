'''
    Author: Rishab Lalwani
    Title: (Otsu's method)
    Version: Python 3.6
'''

import pandas as pd
import matplotlib.pyplot as plt
import math

def otsu(bins,start,end,speeds):
    '''
    :param bins: dictionary containing quantized speeds
    :param start: initial bin
    :param end: final bin
    :param speeds: Total number of speeds present
    :return: mixed_var(minimum variance value),mixed_variances(list of variance),
             threshold, slow_weight, fast_weight
    '''
    # Initialise backward weights,means and variance lists
    Weights_B = []
    Means_B = []
    Var_B = []
    # Initialise forward weights,means and variance lists
    Weights_f = []
    Means_f = []
    Var_f = []
    # Mixed variance initial value set to infinity
    mixed_var = math.inf
    # Create list for all mixed variances
    mixed_variances=[]
    # Initialise threshold, slow and fast weights
    threshold = 0
    slow_weight=0
    fast_weight=0

    for i in range(start,end):
        weight=0
        mean=0
        var=0

        # Formula for forward weights,means and variances
        for j in range(start,i+1):
            weight+=bins[j]
            mean+=j*bins[j]
        try:
            Weights_B.append(weight/speeds)
            Means_B.append(mean/weight)
        # Append 0 if divide by zero occurs
        except ZeroDivisionError:
            Means_B.append(0)

        for z in range(start,i+1):
            var+=((z-Means_B[-1])**2)*bins[z]
        try:
            Var_B.append(var/weight)
        except ZeroDivisionError:
            Var_B.append(0)

        weight = 0
        mean = 0
        var = 0
        # Formula for backward weights,means and variances
        for j in range(i+1,end):
            weight+=bins[j]
            mean+=j*bins[j]
        try:
            Weights_f.append(weight / speeds)
            Means_f.append(mean/weight)
        except ZeroDivisionError:
            Means_f.append(0)

        for z in range(i+1,end):
            var+=((z-Means_f[-1])**2)*bins[z]
        try:
            Var_f.append(var/weight)
        except ZeroDivisionError:
            Var_f.append(0)

        # Append mixed variances to list
        mixed_variances.append(Weights_B[-1]*Var_B[-1]+ Weights_f[-1]*Var_f[-1])

        if mixed_var > Weights_B[-1]*Var_B[-1]+ Weights_f[-1]*Var_f[-1]:
            mixed_var=Weights_B[-1]*Var_B[-1]+ Weights_f[-1]*Var_f[-1]
            threshold=i
            slow_weight = Weights_B[-1] * speeds
            fast_weight = Weights_f[-1] * speeds

    # Plot line dividing the two clusters
    plt.vlines(threshold, 0, 100, linestyle='dashed', colors='red')
    mixed_variances[0]=mixed_variances[1]
    return mixed_var,mixed_variances, threshold, slow_weight, fast_weight

def mixed_var_graph(speed,mixed_variance):
    '''
    :param speed: list of speeds
    :param mixed_variance: list of mixed variances
    :return: plot of car speeds vs mixed variances
    '''

    plt.plot(speed,mixed_variance)
    plt.plot(speed[mixed_variance.index(min(mixed_variance))],min(mixed_variance),marker='o')
    # Labels and title
    plt.xlabel('Car Speeds')
    plt.ylabel('Mixed variances')
    plt.title('Q4: Graphing')
    plt.show()

def objective_function(data):
    '''
    :param data: CSV data of speeds
    :return: mixed_variance(value), threshold, slow_weight, fast_weight
    '''
    # Save speeds data in dataframe using pandas
    data=pd.read_csv(data)
    df = pd.DataFrame(data)
    bins={}
    # Create dictionary of bins for quantized speeds
    for i in range(40,80):
        bins[i]=0
    # Speed attribute
    Speeds=df.loc[:,'Speed']
    # Quantize bins with car speeds
    for i in Speeds:
        r=math.floor(i)
        if r in bins:
            bins[r]+=1
    # Plot histogram of quantized speeds
    plt.bar(bins.keys(),bins.values())
    plt.ylabel('Quantized number of speeds')
    plt.xlabel('Car speeds')
    plt.title('Q1: Otsus method for 1D classification')
    mixed_variance,mixed_variances, threshold, slow_weight, fast_weight=otsu(bins,40,80,len(Speeds))
    plt.show()
    # Plot graph for car speeds vs mixed variances
    mixed_var_graph(list(range(40,80)),mixed_variances)
    return mixed_variances, threshold, slow_weight, fast_weight

def bonus(data,start,thresh,length):
    '''
    :param data: CSV data of speeds
    :param start:  initial quantized bin speed
    :param thresh: threshold speed( end speed)
    :param length: total number of car speeds upto threshold
    :return: plot histogram with 3 cluster of speeds
    '''
    data = pd.read_csv(data)
    df = pd.DataFrame(data)
    bins = {}
    for i in range(start, 80):
        bins[i] = 0
    Speeds = df.loc[:, 'Speed']
    for i in Speeds:
        r = math.floor(i)
        if r in bins:
            bins[r] += 1
    plt.bar(bins.keys(), bins.values())
    plt.ylabel('Quantized number of speeds')
    plt.xlabel('Car speeds')
    plt.title('Q6: Otsus method for multidimension classification')
    # Plot three groups
    otsu(bins, start,thresh, length)
    otsu(bins,thresh+1,80,1018-length)


def regularization(slow_weight,fast_weight,weight):
    '''
    :param slow_weight: Sum of Quantized weights upto threshold
    :param fast_weight: Sum of quantized weights from threshold till 80
    :return: Regularized list
    '''
    regularized_list = []
    # Alpha values list
    alpha = [100, 1, 1 / 5, 1 / 10,1/15,1/16,1/17,1/18,1/19, 1 / 20, 1 / 25, 1 / 50, 1 / 100, 1 / 1000]
    # Formula
    regularized = abs(slow_weight - fast_weight) / 50
    for i in alpha:
        regularized_list.append(round(i * regularized,3))
        if round(weight,3) in regularized_list:
            return i,i*regularized


def main():
    mixed_variance,threshold,slow_weight,fast_weight=objective_function('DATA_v2191_FOR_CLUSTERING_using_Otsu.csv')
    print('The best speed used to separate the two clusters is',threshold)
    mixed_variance.sort()
    print('The minimum mixed variance that resulted is',mixed_variance[0])
    # Regularization

    alpha,regularised=regularization(slow_weight,fast_weight,mixed_variance[1]-mixed_variance[0])
    # Calculating the total cost
    Cost_function = mixed_variance[0]+ regularised
    print('At alpha =',alpha, 'will cause the best splitting to change with cost function',Cost_function)

    # For Bonus Points
    print()
    print('Bonus Question Otsus method for multidimension classification plotted')
    bonus('DATA_v2191_FOR_CLUSTERING_using_Otsu.csv',40,threshold,slow_weight)
    plt.show()

if __name__ == '__main__':
    main()
