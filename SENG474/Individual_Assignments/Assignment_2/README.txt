Cameron Lindsay
V00927778

Please note: Parts of the code were adapted from the following resources, Authors Unknown, Summer 2020: 
SENG 474 Laboratories 3 and 4.
Oneway ANOVA: SciPy.org, scipy.stats.f_oneway (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html), Summer 2020
F-Test: Code Adapated From Zach, Statology: How to Perform an F-Test in Python (https://www.statology.org/f-test-python/), Summer 2020
Scikit Learn pages including 
	Learning Curves: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html 
	Logistic Regression: “Sklearn. linear_model.LogisticRegression.” Scikit, scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html. Accessed July 10, 2020.
	SVM: “Sklearn.svm.SVC.” Scikit, scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html. Accessed July 10, 2020.
	
Libraries required:
	import matplotlib.pyplot
	import numpy
	import importlib
	import scipy.stats
	import sklearn
		from sklearn import metrics
		from sklearn.model_selection import learning_curve
		from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
		from sklearn.utils import shuffle
		from sklearn.linear_model import LogisticRegression
		from sklearn.svm import SVC

Databases required:
fashion-MNIST (https://github.com/zalandoresearch/fashion-mnist)
import code used:
	fashion_mnist = importlib.import_module("fashion-mnist")
	mnist_reader = importlib.import_module("fashion-mnist.utils.mnist_reader")

Instructions: 
All python files require utilities.py and fashion-MNIST to stored locally with the files. 
To perform a particular operation of interest, the user needs to uncomment that line of code. Each step is commented with an appropriate heading describing the task. 

Learning Curves:
logistic_regression.py
svm.py

Hyperparameter Optimization and Model Comparison:
kfold.py
	
