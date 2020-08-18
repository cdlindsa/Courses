# Python 3.7.7, scikit-learn v.0.23.1 used
# Must have datasets 1 and 2 locally
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt

# PsuedoCode Modifed from SENG 474: Lecture 15-16 slides and Sara Jensen's YouTube Video Explanation (KMeans++, Published May 8,2020) from: https://www.youtube.com/watch?v=HatwtJSsj5Q, Summer 2020
def kmeans_plusplus(data, k):
    # Randomly sample first centroid from dataset
    centroids = data.sample(n=1, replace = False, random_state = 1)
    # this reindexes the dataframe for referencing later
    centroids.index = np.arange(len(centroids))
    distances = pd.DataFrame()
    # For each data point compute its distance (squared distance) from a nearest, previously chosen centroid.  
    # Squared Distance = (x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2 + ... 
    while len(centroids) != k:
        temp_distance = []
        min_distance = []
        probabilities = []
        j = len(centroids)-1
        for i in range(len(data)):
            try:
                temp_distance.append((data.loc[i,'X'] - centroids.loc[j,'X']) ** 2 + (data.loc[i,'Y'] - centroids.loc[j,'Y']) ** 2 + (data.loc[i,'Z'] - centroids.loc[j,'Z']) ** 2)
            except:
                temp_distance.append((data.loc[i,'X'] - centroids.loc[j,'X']) ** 2 + (data.loc[i,'Y'] - centroids.loc[j,'Y']) ** 2)
        distances['distance_centroid{}'.format(j)] = temp_distance
        for i in range(len(data)):
            min_distance.append(distances.loc[i].min())
        probabilities = min_distance/sum(min_distance)
        # Choose remaining example x with probability proportional to the squared distance of that example to its closest existing center
        next_centroid = np.where(probabilities == np.max(probabilities))
        centroids.loc[len(centroids)] = data.loc[next_centroid[0][0]]
    # Remainder of algorithm is run with LLoyd's    
    data = assignment(data, centroids, k)
    while True:
        closest_centroids = data['closest_centroid'].copy()
        centroids = update(data, centroids, k)
        data = assignment(data, centroids, k)
        if closest_centroids.equals(data['closest_centroid']):
            break
    SE_calc(data, k)
    return data


# PsuedoCode Modifed from SENG 474: Lecture 15-16 slides and StatQuest's YouTube Video Explanation (StatQuest: KMeans clustering, Published May 23,2018) from: https://www.youtube.com/watch?v=4b5d3muPQmA&t=2s, Summer 2020
def kmeans(data, k):
    # Randomly sample k values as centroids from dataset (initialization)
    centroids = data.sample(n=k, replace = False, random_state = 1)
    # this reindexes the dataframe for referencing later
    centroids.index = np.arange(len(centroids))
    data = assignment(data, centroids, k)
    while True:
        closest_centroids = data['closest_centroid'].copy()
        centroids = update(data, centroids, k)
        data = assignment(data, centroids, k)
        if closest_centroids.equals(data['closest_centroid']):
            break
    SE_calc(data, k)
    return data

def assignment(data, centroids, k): 
    # k clusters are created by associating each data point based on the nearest centroid (via Euclidean distance)
    # Euclidean Distance = sqrt((x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2 + ... )
    try:
        for j in range(k):
            data['distance_from_k{}'.format(j)] = [
                np.sqrt((data.loc[i,'X'] - centroids.loc[j,'X']) ** 2 + (data.loc[i,'Y'] - centroids.loc[j,'Y']) ** 2 + (data.loc[i,'Z'] - centroids.loc[j,'Z']) ** 2) for i in range(len(data))
                ]
    except:
        for j in range(k):
            data['distance_from_k{}'.format(j)] = [
                np.sqrt((data.loc[i,'X'] - centroids.loc[j,'X']) ** 2 + (data.loc[i,'Y'] - centroids.loc[j,'Y']) ** 2) for i in range(len(data))
                ]
    # Determining the closest centroid
    data['closest_centroid'] = data[['distance_from_k{}'.format(i) for i in range(k)]].T.idxmin()   
    # Stripping the name 
    data['closest_centroid'] = data['closest_centroid'].map(lambda x: int(x.lstrip('distance_from_k')))
    return data

def update(data, centroids, k):
    # Centroid of the clusters becomes the new mean
    try:
        for j in range(k):
            centroids.loc[j, 'X'] = np.mean(data.loc[data['closest_centroid'] == j, 'X'])
            centroids.loc[j, 'Y'] = np.mean(data.loc[data['closest_centroid'] == j, 'Y'])
            centroids.loc[j, 'Z'] = np.mean(data.loc[data['closest_centroid'] == j, 'Z'])
    except:
        for j in range(k):
            centroids.loc[j, 'X'] = np.mean(data.loc[data['closest_centroid'] == j, 'X'])
            centroids.loc[j, 'Y'] = np.mean(data.loc[data['closest_centroid'] == j, 'Y'])
    return centroids

# Calculates the Squared Error of the centroid from the associated datapoint
def SE_calc(data, k):
    for i in range(k):
        data.loc[data['closest_centroid'] == i, 'SE'] = data['distance_from_k{}'.format(i)]**2 
    return data

# Performs an F-test with a 95% Confidence Interval. 
# Code Adapated From Zach, Statology: How to Perform an F-Test in Python (https://www.statology.org/f-test-python/), Summer 2020
def F_test(data1, data2, alpha=0.05):
	df1 = np.var(data1, ddof=1)
	df2 = np.var(data2, ddof=1)
	F = df1/df2
	p_value = 1-scipy.stats.f.cdf(F, len(data1)-1, len(data2)-1)
	if p_value > alpha:
		print("Hypothesis testing failed, p: " + str(p_value) + " > " + str(alpha))
	else:
		print("Hypothesis testing succeeded, p: " + str(p_value) + " < " + str(alpha))

# Displays a Boxplot of >1 datasets and calculates mean and CI's
def boxplot_plot(data1, data2, filename, title = 'Comparison of Kmeans vs. Kmeans++', labels = ['Kmeans', "Kmeans++"], ylabel = 'SE', xlabel = 'Dataset'):
    fig, axes = plt.subplots()
    axes.set_title(title)
    axes.boxplot([data, data2], notch=True, vert=True, labels = labels, showmeans=True)
    axes.yaxis.grid(True)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    plt.savefig(filename)
    plt.show()
    plt.clf()

if __name__ == "__main__":
    dataset1 = pd.read_csv("dataset1.csv", sep=',', names= ['X', 'Y'])
    dataset2 = pd.read_csv("dataset2.csv", sep=',', names= ['X', 'Y', 'Z'])

# Dataset 1
    k= range(1, 10)
    SSE = []
    SSE_plusplus = []
    # Kmeans Elbow Plot
    for K in k:
        data = kmeans(dataset1, K)
        SSE.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans', fontsize = 16)
    plt.plot(k, SSE, label = 'Kmeans', color='b')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("elbow_dataset1_kmeans.png")
    plt.show()
    plt.clf()

    # # Kmeans++ Elbow Plot
    for K in k:
        data = kmeans_plusplus(dataset1, K)
        SSE_plusplus.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans++', fontsize = 16)
    plt.plot(k, SSE_plusplus, label = 'Kmeans++', color='g')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("elbow_dataset1_kmeans_plusplus.png")
    plt.show()
    plt.clf()

    # From the Elbow plots, we see that 4 is the optimal number of clusters
    k = 4
    colormap = {0: 'r', 1: 'b', 2: 'g', 3: 'y'}
    data = kmeans(dataset1, k)
    SSE = data['SE'].sum()
    plt.title('Scatter Plot Observing Clusters Determined by Kmeans', fontsize = 16)
    for i in range(len(data)):
        plt.scatter(data.loc[i, 'X'], data.loc[i, 'Y'], c=colormap[data.loc[i, 'closest_centroid']], marker='o', edgecolors='black')
    plt.xlabel("X", fontsize = 14)
    plt.ylabel("Y", fontsize = 14)
    plt.savefig("kmeans_4clusters.png")
    plt.show()
    plt.clf()

    data2 = kmeans_plusplus(dataset1, k)
    SSE_2 = data2['SE'].sum()
    plt.title('Scatter Plot Observing Clusters Determined by Kmeans++', fontsize = 16)
    for i in range(len(data2)):
        plt.scatter(data2.loc[i, 'X'], data2.loc[i, 'Y'], c=colormap[data2.loc[i, 'closest_centroid']], marker='o', edgecolors='black')
    plt.xlabel("X", fontsize = 14)
    plt.ylabel("Y", fontsize = 14)
    plt.savefig("kmeans_plusplus_4clusters.png")
    plt.show()
    plt.clf()

    # Time functions
    begin_time = datetime.datetime.now()
    kmeans(dataset1, k)
    print("kmeans: ", datetime.datetime.now() - begin_time)
    begin_time = datetime.datetime.now()
    kmeans_plusplus(dataset1, k)
    print("kmeans++: ", datetime.datetime.now() - begin_time)
    

    # Boxplot and F-test of data
    print(SSE, SSE_2)
    combined = pd.DataFrame()
    combined['kmeans'] = data['SE']
    combined['kmeans++'] = data2['SE']
    boxplot = combined.boxplot(column=['kmeans', 'kmeans++'])
    plt.savefig("boxplot_kmeans_8clusters_d1.png")
    plt.show()
    plt.clf()
    F_test(data['SE'], data2['SE'])


# Dataset 2
    k= range(1, 10)
    SSE = []
    SSE_plusplus = []
    # Kmeans Elbow Plot
    for K in k:
        data = kmeans(dataset2, K)
        SSE.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans', fontsize = 16)
    plt.plot(k, SSE, label = 'Kmeans', color='b')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("elbow_dataset2_kmeans.png")
    plt.show()
    plt.clf()

    # Kmeans++ Elbow Plot
    for K in k:
        data = kmeans_plusplus(dataset2, K)
        SSE_plusplus.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans++', fontsize = 16)
    plt.plot(k, SSE_plusplus, label = 'Kmeans++', color='g')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("elbow_dataset2_kmeans_plusplus.png")
    plt.show()
    plt.clf()

    k= range(1, 20)
    SSE = []
    SSE_plusplus = []
    # Kmeans Elbow Plot
    for K in k:
        data = kmeans(dataset2, K)
        SSE.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans', fontsize = 16)
    plt.plot(k, SSE, label = 'Kmeans', color='b')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("20_elbow_dataset2_kmeans.png")
    plt.show()
    plt.clf()

    # # Kmeans++ Elbow Plot
    for K in k:
        data = kmeans_plusplus(dataset2, K)
        SSE_plusplus.append(data['SE'].sum())
    plt.title('Elbow Plot Comparing K Values to SSE Using Kmeans++', fontsize = 16)
    plt.plot(k, SSE_plusplus, label = 'Kmeans++', color='g')
    plt.xlabel("k", fontsize = 14)
    plt.ylabel("Sum of squared errors (SSE)", fontsize = 14)
    plt.savefig("20_elbow_dataset2_kmeans_plusplus.png")
    plt.show()
    plt.clf()

    # From the Elbow plots, we see that 8 is the optimal number of clusters
    colormap = {0: 'r', 1: 'b', 2: 'g', 3: 'y', 4: 'c', 5: 'w', 6: 'k', 7: 'm'}
    k = 8
    plt.title('Scatter Plot Observing Clusters Determined by Kmeans', fontsize = 16)
    data = kmeans(dataset2, k)
    SSE = data['SE'].sum()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    for i in range(len(data)):
        ax.scatter(data.loc[i, 'X'], data.loc[i, 'Y'], data.loc[i, 'Z'], c=colormap[data.loc[i, 'closest_centroid']], marker='o', edgecolors='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig("scatter_kmeans_8clusters_d2.png")
    plt.show() 
    plt.clf()

    plt.title('Scatter Plot Observing Clusters Determined by Kmeans++', fontsize = 16)
    data2 = kmeans_plusplus(dataset2, k)
    SSE_2= data2['SE'].sum()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    for i in range(len(data2)):
        ax.scatter(data2.loc[i, 'X'], data2.loc[i, 'Y'], data2.loc[i, 'Z'], c=colormap[data2.loc[i, 'closest_centroid']], marker='o', edgecolors='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig("scatter_kmeans_pluslplus_8clusters_d2.png")
    plt.show() 
    plt.clf()

    # Time functions
    begin_time = datetime.datetime.now()
    kmeans(dataset2, k)
    print("kmeans: ", datetime.datetime.now() - begin_time)
    begin_time = datetime.datetime.now()
    kmeans_plusplus(dataset2, k)
    print("kmeans++: ", datetime.datetime.now() - begin_time)
    

    # Boxplot and F-test of data
    print(SSE, SSE_2)
    combined = pd.DataFrame()
    combined['kmeans'] = data['SE']
    combined['kmeans++'] = data2['SE']
    boxplot = combined.boxplot(column=['kmeans', 'kmeans++'])
    plt.savefig("boxplot_kmeans_8clusters_d2.png")
    plt.show()
    plt.clf()
    F_test(data['SE'], data2['SE'])
    

    
