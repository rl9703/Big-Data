'''
    Author:Rishab Lalwani
    Version: Python 3.6
    Title: Program that writes a program
    Description: Finds the minimum missclassification error of target attribute with other attributes in dataframe
'''


import pandas as pd

def write_to_py(yes_values):
    '''
    :param yes_values: people who are liked to be classified into groups
    :return: New py file written
    '''
    with open('HW05_LALWANI_Rishab_Rule.py','w') as p:
        p.write('import pandas as pd')
        p.write('\n\n')
        p.write('filename=input("Enter filename")')
        p.write('\n')
        p.write('''data=pd.read_csv(filename,encoding="latin-1")''')
        p.write('\n')
        p.write('df=pd.DataFrame(data)')
        p.write('\n')
        p.write('df=df.applymap(lambda s:s.lower() if type(s) == str else s)')
        p.write('\n\n')
        p.write('likestobeassignedtogroups=[]')
        p.write('\n')
        p.write('yes_values=')
        p.write(str(yes_values))
        p.write('\n\n')
        p.write('''for i,rows in df['Snack Food Preference?'].iteritems():''')
        p.write('\n')
        p.write('\t')
        p.write('''if rows == yes_values[0] or rows==yes_values[1] or rows==yes_values[2]:''')
        p.write('\n')
        p.write('\t\t')
        p.write('''likestobeassignedtogroups.append('yes')''')
        p.write('\n')
        p.write('\t')
        p.write('else:')
        p.write('\n')
        p.write('\t\t')
        p.write('''likestobeassignedtogroups.append('no')''')
        p.write('\n\n')
        p.write('''pd.DataFrame(likestobeassignedtogroups,columns=['likesbeingassignedtogroups']).to_csv('HW05_Lalwani_Rishab_Results.csv',index=False)''')


def min_miss():
    '''
    :return: yes values to the file writes
    '''
    test=pd.read_csv("CS720_Obtuse_data_Anonymous_v037.csv",encoding="latin-1")
    df=pd.DataFrame(test)
    # Use lambda function to lower case entire dataframe
    df=df.applymap(lambda s:s.lower() if type(s) == str else s)
    dict_all=[]
    miss_class_rate=[]
    # Iterate over entiree dataframe
    for col in df.head(0):
        ele=set(df[col])
        dict={}
        flag=True
        false_rate = 0
        total = 0
        for x in ele:
            dict[str(x)]=[0,0]
        for i,rows in df["WantAssignmentToGroup"].iteritems():
            if col=='WantAssignmentToGroup':
                flag=False
                break
            if rows=="yes":
                dict[str(df.loc[i, col])][0]+=1
            else:
                dict[str(df.loc[i, col])][1]+=1
        # Calculate missclass rate
        for key,value in dict.items():
            if not flag:
                break
            false_rate+=min(value)
            total+=sum(value)

        if flag:
            miss_class_rate.append(false_rate/total)
            dict_all.append([col,dict,false_rate/total])
    # Sort list on missclassification rate, return smallest missclassification rate
    print(dict_all)
    return sorted(dict_all,key=lambda l:l[2], reverse=True)[-1]

min_miss=min_miss()
yes_values=[]

# Select yes values of target variable from dictionary
for key in min_miss[1]:
    if min_miss[1][key][0]>min_miss[1][key][1]:
        yes_values.append(key)
write_to_py(yes_values)
