'''
    Author: Rishab Lalwani
    Title: Kmeans clustering using Mahalanobis distance
    Version Python 3.7
'''


from scipy.spatial import distance
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

def kmeans(k_clusters,arr):
    '''
    :param k_clusters: Number of clusters initialised by user
    :param arr: Data frame consisting of the datapoints
    :return: cluster centers
    '''
    Squared_error=[]
    cluster_dict={}
    count = 0
    dict1 = {}
    centre_of_mass=[]
    number_of_datapoints={}

    '''
        Random K centroids chosen from dataframe and saved in a dictionary (cluster_dict)
        Keys = Centroid ID (0,1,2...)
        Values =  Random unique centroid 0:(x,y,z),1:(x1,y1,z1)...
    '''
    var = arr.sample(n=k_clusters)
    var = var.values.tolist()

    for rows in var:
        centroid = tuple(rows)
        index = var.index(rows)
        cluster_dict[index] = centroid

    '''
        Over loop of 100 iterations for calculating the new centroids
    '''
    while(count < 100):
        '''
            Dict0: Key (datapoint)
                   Value (List of distances between each centroid)
            Prev: Value of centroids preserved for future comparison
            iv: Inverse covariance matrix for mahalanobis
        '''
        dict0 = {}
        prev= list(cluster_dict.values())
        iv=np.array(arr)

        '''
            Iterate over the dataframe arr
            Create datapoint as tuple (x,y,z)
            Create data list for distances
        '''
        for index,rows in arr.iterrows():
            datapoint=(arr["x"][index], arr["y"][index], arr["z"][index])
            data_list=[]
            check=0
            '''
                For each data point calculate distance between each centroid
                using mahalanobis distance
            '''
            for clusters in cluster_dict:
                m_d=distance.mahalanobis(datapoint, cluster_dict[clusters], np.linalg.inv(np.cov(iv.T)))

                '''
                    If m_d (mahalanobis distance) > 3 for all centroids, ignore that data-point
                    Append all distances to data list
                '''
                if m_d>3:
                    check+=1
                data_list.append(m_d)
            if k_clusters==check:
                continue
            #The values appended are distances
            else:
                dict0[datapoint]= data_list

        '''
            Iterate over dict0 
            Dict0: Key (datapoint)
                   Value (List of distances between each centroid)
            Create new Dictionary Dict1 
            Dict1: Key (Cluster_ID)
                   Value (List of Datapoints(x,y,z) in this cluster_id)
        '''
        for key,value in dict0.items():
            '''
                The minimum mahalanobis distance's corresponding cluster ID is stored in val
            '''
            val = value.index(min(value))
            '''
                Coordinate list= centroids
                val = cluster_ID
            '''
            if val not in dict1:
                '''
                    Dict1: Key (Cluster_ID)
                           Value (List of Datapoints(x,y,z) in this cluster_id)
                '''
                co_ordinate_list = []
                co_ordinate_list.append(key)
                dict1[val] = co_ordinate_list

            # If cluster_ID already present then append the data-point corresponding to that cluster_ID
            else:
                dict1[val].append(key)

        '''
            Dict1: Key (Cluster_ID)
                   Value (List of Datapoints(x,y,z) in this cluster_id)
        '''
        for key,value in dict1.items():
            x_value = 0
            y_value = 0
            z_value = 0
            '''
                Calculate new centroid
                x_value= total x values of that cluster
                y_value= total y values of that cluster
                z_value= total z values of that cluster
            '''
            for rows in value:
                x_value+=rows[0]
                y_value+=rows[1]
                z_value+=rows[2]
            '''
                cluster_dict: Key(Cluster_Id)
                              Value( Centroid(x,y,z) )
                centroids rounded to the nearest 1 decimal.
            '''
            cluster_dict[key]=(round(x_value/len(value),1),round(y_value/len(value),1), round(z_value/len(value),1))

        '''
            Create list (curr) of new centroid values
            print '.' for every iteration
            Compare curr with prev (list of old centroids)
        '''
        curr = list(cluster_dict.values())
        print(".",end='')
        '''
            If same then break 
            else increase counter
        '''
        if curr == prev:
            break
        else:
            count+=1

    '''
        Calculate SSE( Sum of Squared Errors)
        Dict1: Key (Cluster_ID)
                   Value (List of Datapoints(x,y,z) in this cluster_id)
        Centre of mass: list of centroids
        Number of datapoints: Key (Cluster_ID)
                              Value (number of data points in that cluster)
        sse: Error value for each cluster 
        Squared_error: list of sse values of each cluster 
    '''
    for key, value in dict1.items():
        sse=0
        centre_of_mass.append(cluster_dict[key])
        number_of_datapoints[key]=len(value)
        for datapoints in value:
            '''
                Uncomment L1 to calculate sse using L1 norm
                Default: L2 norm selected
            '''
            #L1 Norm
            # sse+=np.sum(np.subtract(cluster_dict[key],datapoints))
            #L2 Norm
            sse+= np.sum(np.subtract(cluster_dict[key],datapoints)**2)
            # sse += (distance.euclidean(key, datapoints))**2
        Squared_error.append(sse)

    return Squared_error,number_of_datapoints,centre_of_mass

def main():
    k_list = []
    sse_l = []

    '''
        Read csv file using pandas as arr
        Convert to Dataframe
    '''
    arr=pd.read_csv("KMEANS_DATA_v810.csv",names=["x","y",'z'])
    r_data=pd.DataFrame(arr)

    '''
        k_values:1-12
    '''
    for k_values in range(1,13):
        k_list.append(k_values)
        sse=[]
        '''
            k=1
            Calculate :
                sse
                number of data points in each cluster
                centroids for each cluster
                time elapsed for each kmeans
        '''
        if k_values==1:
            start_time=time.time()
            error, n_dp, centres=kmeans(k_values,r_data)
            elapsed_time=time.time()-start_time
            sse.append(min(error))
            print('\n',"i. The Sum of Squared Errors for K = ", k_values, " is ", error, "\n"
            "ii. The number of data points in each cluster = ",n_dp, "\n"
            "iii. The center of mass of each cluster = ", centres, "\n"
            "iv. Measure of time(in seconds) that was required to execute the inner loop = ",elapsed_time)
        else:
            '''
            Calculate 500 times:
                sse
                number of data points in each cluster
                centroids for each cluster
                time elapsed for each kmeans
            '''
            for times in range(1, 501):
                print(k_values,"---------------------", times)
                start_time=time.time()
                error,n_dp,centres=kmeans(k_values,r_data)
                elapsed_time=time.time()-start_time
                sse.append(min(error))
                print("\n", "i. The Sum of Squared Errors for K = ",k_values," is ",error,"\n"
                    "ii. The number of data points in each cluster = ",n_dp,"\n"
                    "iii. The center of mass of each cluster = ",centres,"\n"
                    "iv. Measure of time(in seconds) that was required to execute the inner loop = ",elapsed_time,'seconds')
        '''
            Use minimum sse value of cluster and save in list
        '''
        sse_l.append(min(sse))


    '''
        BONUS section using Kmeans of Sklearn , 
        comparison
    '''
    # Uncomment this section to see the graph for Comparision
    #
    # SSE=[]
    # for k_values in range(1,13):
    #     kmeans=KMeans(n_clusters=k_values).fit(r_data)
    #     SSE.append(kmeans.inertia_)
    # x1,=plt.plot(k_list,SSE,'o-',color='red',label='Inbuilt_Kmeans')

    '''
        Plot SSE versus K 
    '''
    x2,=plt.plot(k_list,sse_l,'o-',color='blue',label='My_Kmeans')
    plt.title('SSE versus K for the L2 norm')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Sum of Squared Errors')
    plt.legend(handles=[x2])
    plt.show()

if __name__ == '__main__':
    main()
