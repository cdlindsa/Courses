Cameron Lindsay
V00927778

Please note: Parts of the code were adapted from the following resources, Authors Unknown, Summer 2020: 
SENG 474 Laboratory 6.
F-Test: Code Adapated From Zach, Statology: How to Perform an F-Test in Python (https://www.statology.org/f-test-python/), Summer 2020
Scikit Learn pages including 
	Hierarchical Agglomerative Clustering: “Sklearn.cluster.AgglomerativeClustering.” Scikit, scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html. Accessed July 26, 2020.
	
Libraries required:
import scipy.stats
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

Databases required:
dataset1.csv
dataset2.csv
import code used:
    dataset1 = pd.read_csv("dataset1.csv", sep=',', names= ['X', 'Y'])
    dataset2 = pd.read_csv("dataset2.csv", sep=',', names= ['X', 'Y', 'Z'])

Instructions: 
All python files run independently and require databases to be stored locally with the files. 
To perform a particular operation of interest, the user needs to comment/uncomment that line of code. Each step is commented with an appropriate heading describing the task. 

K-means Using Random Initialization and K-means++:
kmeans.py

Hierarchical Agglomerative Clustering:
hcluster.py