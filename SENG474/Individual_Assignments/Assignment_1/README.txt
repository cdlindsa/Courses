Cameron Lindsay
V00927778
Please note: Parts of the code were adapted from the following resources, Authors Unknown, Summer 2020: 
SENG 474 Laboratories 1 and 2.
Scikit Learn pages including 
	Learning Curves: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.learning_curve.html 
	Validation Curves: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.validation_curve.html#sklearn.model_selection.validation_curve
	Validation Curves & Learning Curves: https://scikit-learn.org/stable/modules/learning_curve.html
	DecisionTreeClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
	RandomForestClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
	MLPClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
	
Libraries required:
import sklearn 
	from sklearn.datasets import load_digits, load_breast_cancer
	from sklearn.neural_network import MLPClassifier
	from sklearn.model_selection import train_test_split
	from sklearn.model_selection import GridSearchCV
	from sklearn import preprocessing
	from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
	from sklearn.model_selection import train_test_split, learning_curve, validation_curve
	from sklearn.datasets import load_files, load_breast_cancer
	from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
	from sklearn import tree, metrics
	from sklearn.tree import DecisionTreeClassifier
	from sklearn.tree._tree import TREE_LEAF
import matplotlib.pyplot
import numpy

Databases required:
cleaned_processed.cleveland.data (included)
load_breast_cancer (imported from sklearn)


Instructions: 
All jupyter notebooks can be independently run with cleaned_processed.cleveland.data stored locally with the file. 
All functions necessary to perform the necessary tests are included for clear view and not imported from a separate helper file.
To perform a particular operation of interest, the user needs to uncomment that line of code. 
	
