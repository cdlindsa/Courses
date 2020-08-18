# Python 3.7 used
# Must have fashion-mnist repo locally
import utilities as util
import numpy as np
from sklearn import metrics
from sklearn.svm import SVC

def init_svm(X_train, y_train, X_test, y_test, kernel='linear', C = 1.0, max_iter = 5000):
	clf = SVC(kernel = kernel, C=C, max_iter=max_iter)
	model = clf.fit(X_train, y_train)
	return model

if __name__ == "__main__":
	# Prep Data
	x_train, y_train, x_test, y_test, data, target = util.prepare_data()

	# Plotting the Optimized Model Learning Curves
	# Set 1:
	util.learning_curve_plot(SVC(kernel='linear', C=100, max_iter = 5000), data, target, label='C=100', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	svm_1 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=100)
	pred_1 = svm_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(SVC(kernel='linear', C=10, max_iter = 5000), data, target, label='C=10', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	svm_2 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=10)
	pred_2 = svm_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(SVC(kernel='linear', C=1, max_iter = 5000), data, target, label='C=1', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	svm_3 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=1)
	pred_3 = svm_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 2:
	util.learning_curve_plot(SVC(kernel='linear', C=0.1, max_iter = 5000), data, target, label='C=1e-1', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	svm_1 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.1)
	pred_1 = svm_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(SVC(kernel='linear', C=0.01, max_iter = 5000), data, target, label='C=1e-2', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	svm_2 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.01)
	pred_2 = svm_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(SVC(kernel='linear', C=0.001, max_iter = 5000), data, target, label='C=1e-3', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	svm_3 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.001)
	pred_3 = svm_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 3:
	util.learning_curve_plot(SVC(kernel='linear', C=0.3, max_iter = 5000), data, target, label='C=0.3', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	svm_1 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.3)
	pred_1 = svm_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(SVC(kernel='linear', C=0.6, max_iter = 5000), data, target, label='C=0.6', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	svm_2 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.6)
	pred_2 = svm_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(SVC(kernel='linear', C=0.9, max_iter = 5000), data, target, label='C=0.9', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	svm_3 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.9)
	pred_3 = svm_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 4:
	util.learning_curve_plot(SVC(kernel='linear', C=0.45, max_iter = 5000), data, target, label='C=0.45', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	svm_1 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.45)
	pred_1 = svm_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(SVC(kernel='linear', C=0.75, max_iter = 5000), data, target, label='C=0.75', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	svm_2 = init_svm(x_train, y_train, x_test, y_test, kernel= 'linear', max_iter = 5000, C=0.75)
	pred_2 = svm_2.predict(x_test)
	util.print_info(y_test, pred_2)

	util.title_and_labels(y_label = 'Negative Mean SE', x_label = 'Training set size', title = 'Learning Curve')