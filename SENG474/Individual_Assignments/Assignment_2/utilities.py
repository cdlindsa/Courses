# Python 3.7 used
# Must have fashion-mnist repo locally
# import sklearn as sk

# File contains a list of Helper functions for the various models and methods utilized in this assignment
import matplotlib.pyplot as plt
import numpy as np
import importlib
import scipy.stats
fashion_mnist = importlib.import_module("fashion-mnist")
mnist_reader = importlib.import_module("fashion-mnist.utils.mnist_reader")
from sklearn import metrics
from sklearn.model_selection import learning_curve
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Returns data containing only 5 and 7 from classifiers, rescales input by 255, turns 5 and 7 to 0 and 1, respectively
def remove_labels(X, y):
	filter_array = (y == 5) | (y == 7)
	X_new = X[filter_array]
	X_new = np.divide(X_new, 255)
	y_new = y[filter_array]
	y_new = np.where(y_new > 5, 1, 0)
	return X_new, y_new

# Preprocesses and splits the dataset for training/testing
def prepare_data():
	X_train, y_train = mnist_reader.load_mnist('fashion-mnist/data/fashion', kind='train')
	X_test, y_test = mnist_reader.load_mnist('fashion-mnist/data/fashion', kind='t10k')
	X_train, y_train = remove_labels(X_train, y_train)
	X_test, y_test = remove_labels(X_test, y_test)
	X_full = np.array(X_train)
	X_full = np.append(X_full, X_test, axis=0)
	y_full = np.array(y_train)
	y_full = np.append(y_full, y_test)
	return X_train, y_train, X_test, y_test, X_full, y_full

# Prints the Mean Absolute Error, RMSE, Confusion Matrix, Classification Matrix, F1-Values, and Accuracy Score of the Tree's test data
def print_info(y_test, y_pred):
    print('Mean Absolute Error: ', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error: ', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error: ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
    print('Classification Report:\n', classification_report(y_test, y_pred))
    print('Accuracy Score: ', accuracy_score(y_test, y_pred))

# Plots learning curve data of a model
def learning_curve_plot(model, data, target, label, scoring = 'accuracy', colorTrain='blue', colorTest='red'):
	train_sizes, train_scores, validation_scores = learning_curve(model, X = data, y = target, scoring = scoring)
	train_scores_mean = train_scores.mean(axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	validation_scores_mean = validation_scores.mean(axis=1)
	validation_scores_std = np.std(validation_scores, axis=1)
	plt.fill_between(train_sizes, validation_scores_mean - validation_scores_std, validation_scores_mean + validation_scores_std, alpha=0.1, color=colorTest)
	plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color=colorTrain)
	plt.plot(train_sizes, validation_scores_mean, label = 'Testing score ' + label, color=colorTest)
	plt.plot(train_sizes, train_scores_mean, label = 'Training score ' + label, color=colorTrain)

# Performs an F-test with a 95% Confidence Interval. 
# Code Adapated From SciPy.org, scipy.stats.f_oneway (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html), Summer 2020
def F_test_oneway(data1, data2, data3, alpha=0.05):
	F,  p_value = scipy.stats.f_oneway(data1, data2, data3)
	if p_value > alpha:
		print("Hypothesis testing failed, p: " + str(p_value) + " > " + str(alpha))
	else:
		print("Hypothesis testing succeeded, p: " + str(p_value) + " < " + str(alpha))

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
def boxplot_plot(data, title = 'Comparison of Training Alone vs. Whole Dataset', labels = ['Training', "Whole"], ylabel = 'Accuracy', xlabel = 'Dataset'):
	fig, axes = plt.subplots()
	axes.set_title(title)
	axes.boxplot(data, notch=True, vert=True, labels = labels, showmeans=True)
	axes.yaxis.grid(True)
	axes.set_xlabel(xlabel)
	axes.set_ylabel(ylabel)
	plt.show()

# Displays a Simple Plot of >1 datasets
def validation_curve_custom(data_x, data_validation, data_test, rangelow=0.18, rangehigh=0.22):
	fig, axes = plt.subplots()
	xi = list(range(len(data_x)))
	plt.plot(xi, data_validation, label = "Validation")
	plt.plot(xi, data_test, label = "Test")
	plt.ylim(0.12, 0.18)
	plt.xticks(xi, data_x)
	axes.grid()
	
# Shows final graph with appropriate axis labels
def title_and_labels(y_label = 'Accuracy', x_label = 'Training set size', title = 'Learning Curve'):
	plt.ylabel(y_label, fontsize = 14)
	plt.xlabel(x_label, fontsize = 14)
	plt.title(title, fontsize= 16)
	plt.legend()
	plt.show()



