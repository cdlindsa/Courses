# Python 3.7.7, scikit-learn v.0.23.1 used
# Must have datasets 1 and 2 locally
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
import sklearn
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

# Code modified from SENG 474 Lab 6: Author Unknown, Summer 2020
def plot_dendrogram(model, **kwargs):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count
    linkage_matrix = np.column_stack([model.children_, model.distances_, counts]).astype(float)
    dendrogram(linkage_matrix, **kwargs)

if __name__ == "__main__":
    dataset1 = pd.read_csv("dataset1.csv", sep=',', names= ['X', 'Y'])
    dataset2 = pd.read_csv("dataset2.csv", sep=',', names= ['X', 'Y', 'Z'])

# Dataset 1

    # Dendrogram with average linkage
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, affinity='euclidean', linkage='average')
    model = model.fit(dataset1)
    plt.title('Hierarchical Clustering Dendrogram Using Average Linkage')
    plot_dendrogram(model, truncate_mode='level', p=5)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.ylabel("Distance")
    plt.savefig("hac_dataset1_avg.png")
    plt.show() 
    plt.clf()
    
    # Scatter plot with average linkage
    plt.title('Scatter Plot Average Linkage', fontsize = 16)
    model = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='average')
    model = model.fit(dataset1)
    plt.scatter(dataset1['X'], dataset1['Y'], c=model.labels_, marker='o', edgecolors='black')
    plt.xlabel("X", fontsize = 14)
    plt.ylabel("Y", fontsize = 14)
    plt.savefig("dataset1_avg_scatter.png")
    plt.show() 
    plt.clf()

    # Dendrogram with single linkage
    model = AgglomerativeClustering(distance_threshold=0, affinity='euclidean', n_clusters=None, linkage='single')
    model = model.fit(dataset1)
    plt.title('Hierarchical Clustering Dendrogram Using Single Linkage')
    plot_dendrogram(model, truncate_mode='level', p=5)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.ylabel("Distance")
    plt.savefig("hac_dataset1_sgl.png")
    plt.show()
    plt.clf()

    # Scatter plot with average linkage
    plt.title('Scatter Plot Single Linkage', fontsize = 16)
    model = AgglomerativeClustering(n_clusters=1, affinity='euclidean', linkage='single')
    model = model.fit(dataset1)
    plt.scatter(dataset1['X'], dataset1['Y'], c=model.labels_, marker='o', edgecolors='black')
    plt.xlabel("X", fontsize = 14)
    plt.ylabel("Y", fontsize = 14)
    plt.savefig("dataset1_sgl_scatter.png")
    plt.show() 
    plt.clf()

# Dataset 2

    # Dendrogram with average linkage
    model = AgglomerativeClustering(distance_threshold=0, affinity='euclidean', n_clusters=None, linkage='average')
    model = model.fit(dataset2)
    plt.title('Hierarchical Clustering Dendrogram Using Average Linkage')
    plot_dendrogram(model, truncate_mode='level', p=5)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.ylabel("Distance")
    plt.savefig("hac_dataset2_avg.png")
    plt.clf()

    # Scatter plot with average linkage
    model = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='average')
    model = model.fit(dataset2)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.scatter(dataset2['X'], dataset2['Y'], dataset2['Z'], c=model.labels_, marker='o', edgecolors='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig("scatter_dataset2_avg.png")
    plt.show() 
    plt.clf()

    # Dendrogram with single linkage
    model = AgglomerativeClustering(distance_threshold=0, affinity='euclidean', n_clusters=None, linkage='single')
    model = model.fit(dataset2)
    plt.title('Hierarchical Clustering Dendrogram Using Single Linkage')
    plot_dendrogram(model, truncate_mode='level', p=5)
    plt.xlabel("Number of points in node (or index of point if no parenthesis).")
    plt.ylabel("Distance")
    plt.savefig("hac_dataset2_sgl.png")
    plt.clf()

    # Scatter plot with single linkage
    model = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='single')
    model = model.fit(dataset2)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.scatter(dataset2['X'], dataset2['Y'], dataset2['Z'], c=model.labels_, marker='o', edgecolors='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig("scatter_dataset2_sgl.png")
    plt.show() 
    plt.clf()

    

    
