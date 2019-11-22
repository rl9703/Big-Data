'''
    Author: Rishab Lalwani
    Title: Classification
    Version: python 3.6
'''

import pandas as pd
import matplotlib.pyplot as plt
import math


def objective_function(data_,x=1,y=1):
    '''
    :param data_: CSV data of speeds and aggressiveness
    :param x: value to multiply with false negative rates
    :param y: value to multiply with false positive rates
    :return: best cost function
    '''
    # Read
    data=pd.read_csv(data_)
    df = pd.DataFrame(data)
    best_cost_func_yet=math.inf
    best_threshold_to_use=0

    # Create Bins
    bins={}
    for i in range(45,80):
        bins[i]=[]
        bins[i+0.5]=[]

    for idx,row in df.iterrows():
        r = round((row['Speed'] * 2)) / 2
        if r in bins:
            bins[r].append([row['Speed'],int(row['Aggressive'])])

    # Calculating cost and threshold
    best_idx=idx=0
    false_alarm_rate=[]
    true_pos_rate=[]
    cost_func=[]
    threshold_list = []
    Aggressive_drivers=non_reckless_drivers=0
    for threshold in bins:
        threshold_list.append(threshold)
        TP = TN = FP = FN = 0
        for index,rows in df.iterrows():
            if round(rows['Speed']*2)/2<= threshold:
                if rows['Aggressive']==1:
                    FN+=1
                else:
                    TN+=1
            else:
                if rows['Aggressive']==1:
                    TP+=1
                else:
                    FP+=1
        cost_func.append(x*FN+y*FP)
        # Best values
        if cost_func[-1]<= best_cost_func_yet:
            best_cost_func_yet=cost_func[-1]
            Aggressive_drivers=FN
            non_reckless_drivers=FP
            best_threshold_to_use=threshold
            best_idx=idx

        false_alarm_rate.append(FP / (TN + FP))
        true_pos_rate.append(TP / (FN + TP))

        idx+=1

    # Plotting and printing
    print(best_cost_func_yet)
    print(best_threshold_to_use)
    print(best_idx)
    plt.plot(false_alarm_rate,true_pos_rate,marker='o')
    plt.plot(false_alarm_rate[best_idx],true_pos_rate[best_idx],marker='o',color='black')
    plt.plot([1,0],[1,0],color='red',linestyle='dashed')
    plt.title('j) ROC curve of False Alarm Rate vs True Positive Rate')
    plt.xlabel('False Alarm Rate')
    plt.ylabel('True Positive Rate')
    plt.show()
    print('Cost Function:',min(cost_func))
    plt.plot(threshold_list,cost_func)
    plt.title('i) Threshold vs Cost function')
    plt.xlabel('Threshold')
    plt.ylabel('Cost Function')
    plt.plot(best_threshold_to_use,best_cost_func_yet,marker='o',color='red')
    plt.show()
    print('Aggressive drivers:',Aggressive_drivers)
    print('Non reckless drivers:',non_reckless_drivers)

    return best_cost_func_yet

def main():
    # Main cost Part C
    cost_function=objective_function('DATA_v2191_FOR_CLASSIFICATION_using_Threshold.csv')
    # Regularization Part E
    print('-------Temporary Modification---------')
    regularization=objective_function('DATA_v2191_FOR_CLASSIFICATION_using_Threshold.csv',2,1)-cost_function
    print()
    print('Regularization value is:',regularization)

if __name__ == '__main__':
    main()

