'''
    Author: Rishab Lalwani
    Title: Decision Tree
    Version : python 3.6
'''
import pandas as pd
import numpy as np


writer = ""

def entropy(data):
    '''
    :param data: count of muffins/cupcakes
    :return: entropy for data
    '''
    prob_dict = {x:data.count(x)/len(data) for x in data}
    probs = np.array(list(prob_dict.values()))
    return - probs.dot(np.log2(probs))

def weights(muffins, cupcakes):
    '''
    :param muffins: muffins in recipe type
    :param cupcakes: cupcakes in recipe type
    :return: mixed entropy
    '''

    mixed_entropies = (len(muffins) / (len(muffins) + len(cupcakes)) * entropy(muffins)) + (len(cupcakes) / (len(muffins) + len(cupcakes)) * entropy(cupcakes))

    return mixed_entropies

def threshold(trainer_frame):
    '''

    :param trainer_frame:  Training dataframe
    :return: threshold and its index number
    '''
    '''
        Setting the maximum threshold value to 10
        since there is no value in the data of training greater than 11
        Hence considering it as the maximum value
    '''
    min_thresh=1
    max_thresh=10
    best_mixed_entropy = 99999999
    # step_size=0.5
    colum_num = ""
    thresh = 0
    '''
        Find threshold value using weighted entropy
        Also return the index at which it is

    '''
    for cols in trainer_frame.columns:
        for thresholds in range(min_thresh,max_thresh):
            cupcakes = []
            muffins = []

            # Calculate current entropy from the weighted entropies
            for index, value in trainer_frame.iterrows():
                if (trainer_frame[cols][index]) <= thresholds:
                    muffins.append(trainer_frame['RecipeType'][index])
                else:
                    cupcakes.append(trainer_frame['RecipeType'][index])
            weighted_entropy = weights(muffins, cupcakes)

            # Calculate least mixed entropy value
            if (len(muffins) >= 5 and len(cupcakes) >= 5) and (weighted_entropy < best_mixed_entropy):
                best_mixed_entropy = weighted_entropy
                colum_num = cols
                thresh = thresholds

    return colum_num, thresh

def decision_tree(trainer_frame, iteration):

    global writer
    muffins =cupcake= 0
    tab="\t"
    new_line='\n'
    target=trainer_frame['RecipeType']
    '''
        Keep count of cupcakes and muffins (450 each)
    '''
    # index,unique=(np.unique(target,return_counts=True))

    for rows in target:
        if rows==1:
            cupcake+=1
        else:
            muffins+=1

    # Stopping criteria for Decision tree learning
    '''
        if tuples less than 23 then break the recursion
        if % of cupcakes or muffins greater than 90 then stop
        if number of iterations more than 11 then stop
    '''
    if len(trainer_frame) < 23 or (cupcake/ len(trainer_frame) > 0.9 or muffins / len(
            trainer_frame) > 0.9) or iteration > 11:

        if muffins >= cupcake:
            writer += tab * iteration + "report.append([" + str(0) + "])\n"
        else:
            writer += tab * iteration + "report.append([" + str(1) + "])\n"

    # Create Decision tree here
    else:
        # find best split and index of that
        best_index, split_value = threshold(trainer_frame)

        # Create left and right trees using pandas dataframes
        left_subtree= pd.DataFrame()
        right_subtree = pd.DataFrame()


        '''
            Iterate over the entire training set and create nodes in left tree or right tree
            If node value less than equal to threshold append to left tree else right tree
        '''
        for index, values in trainer_frame.iterrows():
            # Create node list
            node=list(trainer_frame.columns.values.tolist())

            if trainer_frame[best_index][index] <= split_value:
                left_subtree = left_subtree.append(trainer_frame.loc[index, node])
            else:
                right_subtree = right_subtree.append(trainer_frame.loc[index, node])

        spaces=tab* iteration
        writer += spaces
        writer+="if data_train['" + best_index + "'][index]<=" + str(split_value) + ":\n"

        writer+=new_line
        '''
            Recursively pass left subtree and right subtree into the decision tree method
        '''
        decision_tree(left_subtree, iteration + 1)
        writer +=(tab*iteration)+"else:\n"
        decision_tree(right_subtree, iteration + 1)

def main():
    '''
    :Read training set and save it in dataframe called the train frame
    :Save the target attribute('Recipe type') as target
    '''

    train_frame = pd.read_csv("/Users/rishab/Desktop/BDA/DT_Data_CakeVsMuffin_v012_TRAIN.csv")
    # test_frame= pd.read_csv("/Users/rishab/Desktop/BDA/DT_Data_CakeVsMuffin_v012_TEST.csv")
    target=train_frame['RecipeType']

    '''
        Convert the target into binary (0,1's)
        cupcake=1
        muffin=0
    '''
    for index in range(len(target)):
        if target[index] == "CupCake":
            train_frame['RecipeType'][index] = 1
        else:
            train_frame['RecipeType'][index] = 0

    '''
        Use a global variable to write a string which consists of the classifier program
    '''
    global writer
    writer += "import pandas as pd \nimport numpy as np \nimport csv\n\n"
    writer += "data_train = pd.read_csv(\"/Users/rishab/Desktop/BDA/DT_Data_CakeVsMuffin_v012_TRAIN.csv\")\n" \
              "report = []\n" \
              "report.append('Rishab_Lalwani_HW06-07')\n" \
              "for index,tuple_value in data_train.iterrows():\n"

    decision_tree(train_frame, 1)

    writer += "with open(\"HW06_Lalwani_Rishab_MyClassifications.csv\",'w', newline='') as file:\n" \
            "\twr = csv.writer(file)\n" \
            "\twr.writerows(report)\n"

    with open("HW06_Lalwani_Rishab_Classifier.py", "w+") as file:
        file.write(writer)
        file.close()

if __name__ == '__main__':
    main()
