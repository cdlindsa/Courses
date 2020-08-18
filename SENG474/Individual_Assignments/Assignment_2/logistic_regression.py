# Python 3.7 used
# Must have fashion-mnist repo locally
import utilities as util
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

def init_logistic_regression(X_train, y_train, X_test, y_test, penalty = 'l2', C = 1.0, max_iter = 5000, solver='lbfgs'):
	clf = LogisticRegression(penalty=penalty, C=C, max_iter=max_iter, solver=solver)
	model = clf.fit(X_train, y_train)
	return model

if __name__ == "__main__":
	# Prep Data
	x_train, y_train, x_test, y_test, data, target = util.prepare_data()
	
	# Plotting the Optimized Model Learning Curve
	# Set 1:
	util.learning_curve_plot(LogisticRegression(C=100), data, target, label='C=100', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	lgr_1 = init_logistic_regression(x_train, y_train, x_test, y_test, C=100, max_iter=5000)
	pred_1 = lgr_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(LogisticRegression(C=10), data, target, label='C=10', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	lgr_2 = init_logistic_regression(x_train, y_train, x_test, y_test, C=10, max_iter=5000)
	pred_2 = lgr_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(LogisticRegression(C=1), data, target, label='C=1', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	lgr_3 = init_logistic_regression(x_train, y_train, x_test, y_test, C=1, max_iter=5000)
	pred_3 = lgr_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 2:
	util.learning_curve_plot(LogisticRegression(C=0.1), data, target, label='C=1e-1', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	lgr_1 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.1, max_iter=5000)
	pred_1 = lgr_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(LogisticRegression(C=0.01), data, target, label='C=1e-2', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	lgr_2 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.01, max_iter=5000)
	pred_2 = lgr_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(LogisticRegression(C=0.001), data, target, label='C=1e-3', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	lgr_3 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.001, max_iter=5000)
	pred_3 = lgr_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 3:
	util.learning_curve_plot(LogisticRegression(C=0.3), data, target, label='C=0.3', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	lgr_1 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.3, max_iter=5000)
	pred_1 = lgr_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(LogisticRegression(C=0.6), data, target, label='C=0.6', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	lgr_2 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.6, max_iter=5000)
	pred_2 = lgr_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(LogisticRegression(C=0.9), data, target, label='C=0.9', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	lgr_3 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.9, max_iter=5000)
	pred_3 = lgr_3.predict(x_test)
	util.print_info(y_test, pred_3)

	# Set 4:
	util.learning_curve_plot(LogisticRegression(C=0.2), data, target, label='C=0.2', scoring='neg_mean_squared_error', colorTrain='blue', colorTest='magenta')
	lgr_1 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.2, max_iter=5000)
	pred_1 = lgr_1.predict(x_test)
	util.print_info(y_test, pred_1)

	util.learning_curve_plot(LogisticRegression(C=0.4), data, target, label='C=0.4', scoring='neg_mean_squared_error', colorTrain='green', colorTest='yellow')
	lgr_2 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.4, max_iter=5000)
	pred_2 = lgr_2.predict(x_test)
	util.print_info(y_test, pred_2)
	
	util.learning_curve_plot(LogisticRegression(C=0.5), data, target, label='C=0.5', scoring='neg_mean_squared_error', colorTrain='cyan', colorTest='red')
	lgr_3 = init_logistic_regression(x_train, y_train, x_test, y_test, C=0.5, max_iter=5000)
	pred_3 = lgr_3.predict(x_test)
	util.print_info(y_test, pred_3)

	util.title_and_labels(y_label = 'Negative Mean SE', x_label = 'Training set size', title = 'Learning Curve')
