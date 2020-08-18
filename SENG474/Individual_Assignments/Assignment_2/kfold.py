# Python 3.7 used
# Must have fashion-mnist repo locally
import utilities as util
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np
from sklearn.utils import shuffle
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Process taken from: Jason Brownlee, May 23, 2018 https://machinelearningmastery.com/k-fold-cross-validation/
# Shuffle dataset randomly
# Split dataset into k groups (folds)
# For each unique group:
# 1. Take group as test dataset
# 2. Take remaining groups as training dataset
# 3. Fit model on training set and evaluate on the test set
# 4. Retain the evaluation score and discard the model
def k_fold(model, C, x, y, groups=5):
	error_array = np.array([])
	accuracy_array = np.array([])
	x_copy = np.copy(x)
	y_copy = np.copy(y)
	randomizer = np.arange(x_copy.shape[0])
	np.random.shuffle(randomizer)
	x_copy = x_copy[randomizer]
	y_copy = y_copy[randomizer]
	x_copy = np.array_split(x_copy, groups)
	y_copy = np.array_split(y_copy, groups)
	for fold in range(groups):
		train_x = np.copy(x_copy)
		train_y = np.copy(y_copy)
		test_x = train_x[fold]
		test_y = train_y[fold]
		train_x = np.delete(train_x, fold, axis=0)
		train_y = np.delete(train_y, fold, axis=0)
		train_x = np.concatenate(train_x, axis=0)
		train_y = np.concatenate(train_y, axis=0)
		mean_error, max_accuracy = kfold_testing(model, C, test_x, test_y, train_x, train_y)
		error_array = np.append(error_array, mean_error)
		accuracy_array = np.append(accuracy_array, max_accuracy)
	mean_error = np.mean(error_array)
	mean_accuracy = np.mean(accuracy_array)
	return mean_error, error_array, mean_accuracy, accuracy_array

# KFold testing of the model using root mean squared error and accuracy on tested models
def kfold_testing(model, C, test_x, test_y, train_x, train_y):
	if model == 'logreg':
		model = LogisticRegression(C = C, penalty = 'l2', solver='lbfgs', max_iter = 5000)
	elif model == 'svm_lin':
		model = SVC(kernel = 'linear', C = C, max_iter = 5000)
	else:
		model = SVC(kernel = 'rbf', C = C, gamma='scale', max_iter = 5000)
	model.fit(train_x, train_y)
	temp_predict = model.predict(test_x)
	error = np.sqrt(metrics.mean_squared_error(test_y, temp_predict))
	accuracy = metrics.accuracy_score(test_y, temp_predict)
	return error, accuracy

if __name__ == "__main__":
	# Preparing Dataset
	x_train, y_train, x_test, y_test, data, target = util.prepare_data()
	
	# Logistic regression c-values to test
	c_values = [0.300, 0.325, 0.350, 0.375, 0.4, 
				0.425, 0.450, 0.475, 0.500]
	errors_validation = []
	errors_test = []
	accuracy_validation = []
	accuracy_test = []
	for C in c_values:
		mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='logreg', C=C, x=x_train, y=y_train, groups = 5)
		errors_validation.append(mean_error)
		accuracy_validation.append(mean_accuracy)
	for C in c_values:
		mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='logreg', C=C, x=data, y=target, groups = 5)
		errors_test.append(mean_error_full)
		accuracy_test.append(mean_accuracy_full)
	util.validation_curve_custom(c_values, errors_validation, errors_test)
	util.title_and_labels(y_label = 'RMSE', x_label = 'C value', title = 'Validation Curve Logistic Regression')

	# F-test 
	mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='logreg', C=0.475, x=x_train, y=y_train, groups = 5)	
	mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='logreg', C=0.475, x=data, y=target, groups = 5)
	util.boxplot_plot(data=[error_array, error_array_full], ylabel='RMSE')
	util.F_test(error_array, error_array_full)

	# SVM (linear kernel) c-values to test
	c_values = [0.500, 0.525, 0.550, 0.575, 0.6,
				0.625, 0.65, 0.675, 0.7]
	errors_validation = []
	errors_test = []
	accuracy_validation = []
	accuracy_test = []
	for C in c_values:
		mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='svm_lin', C=C, x=x_train, y=y_train, groups = 5)
		errors_validation.append(mean_error)
		accuracy_validation.append(mean_accuracy)
	for C in c_values:
		mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='svm_lin', C=C, x=data, y=target, groups = 5)
		errors_test.append(mean_error_full)
		accuracy_test.append(mean_accuracy_full)
	util.validation_curve_custom(c_values, errors_validation, errors_test)
	util.title_and_labels(y_label = 'RMSE', x_label = 'C value', title = 'Validation Curve SVM Linear Kernel')

	# F-test 
	mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='svm_lin', C=0.6, x=x_train, y=y_train, groups = 5)	
	mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='svm_lin', C=0.6, x=x_train, y=y_train, groups = 5)
	util.boxplot_plot(data=[error_array, error_array_full], ylabel='RMSE')
	util.F_test(error_array, error_array_full)

	# SVM (Gaussian kernel) c-values to test
	c_values = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
	c_values = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
	c_values = [55, 56, 57, 58, 59,
				60, 61, 62, 63, 64, 65]
	errors_validation = []
	errors_test = []
	accuracy_validation = []
	accuracy_test = []
	for C in c_values:
		mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='svm_g', C=C, x=x_train, y=y_train, groups = 5)
		errors_validation.append(mean_error)
		accuracy_validation.append(mean_accuracy)
	for C in c_values:
		mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='svm_g', C=C, x=data, y=target, groups = 5)
		errors_test.append(mean_error_full)
		accuracy_test.append(mean_accuracy_full)
	util.validation_curve_custom(c_values, errors_validation, errors_test)
	util.title_and_labels(y_label = 'RMSE', x_label = 'Gamma', title = 'Validation Curve SVM Gaussian Kernel')

	# F-test 
	mean_error, error_array, mean_accuracy, accuracy_array = k_fold(model='svm_g', C=60, x=x_train, y=y_train, groups = 5)	
	mean_error_full, error_array_full, mean_accuracy_full, accuracy_array_full = k_fold(model='svm_g', C=60, x=data, y=target, groups = 5)
	util.boxplot_plot(data=[error_array, error_array_full], ylabel='RMSE')
	util.F_test(error_array, error_array_full)

	# Oneway ANOVA, F-test 
	mean_error_logreg, error_array_logreg, mean_accuracy_logreg, accuracy_array_logreg = k_fold(model='logreg', C=0.475, x=data, y=target, groups = 5)
	mean_error_svm, error_array_svm, mean_accuracy_svm, accuracy_array_svm = k_fold(model='svm_lin', C=0.6, x=x_train, y=y_train, groups = 5)
	mean_error_svmg, error_array_svmg, mean_accuracy_svmg, accuracy_array_svmg = k_fold(model='svm_g', C=60, x=data, y=target, groups = 5)
	util.boxplot_plot(data=[error_array_logreg, error_array_svm, error_array_svmg],title = 'Comparison of Final Models Using Full Dataset', ylabel='RMSE', labels = ['Logistic Regression', "SVM Linear Kernel", "SVM Gaussian Kernel"])
	util.F_test_oneway(error_array_logreg, error_array_svm, error_array_svmg)

	# Reporting scores:
	print('Minimum Error - Test Curve:', min(errors_test))
	print(errors_test)
	print('Maximum Accuracy - Test Curve:', max(accuracy_test))
	print(accuracy_test)
	print('Minimum Error - Validation Curve:', min(errors_validation))
	print(errors_validation)
	print('Maximum Accuracy - Validation Curve:', max(accuracy_validation))
	print(accuracy_validation)