# Python 3.7 used
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn import metrics
from sklearn.model_selection import train_test_split, validation_curve, learning_curve
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC

def validation_curve_plot(data, target, param_range):
	train_scores, test_scores = validation_curve(SVC(kernel='linear'), data, target, param_name="C", param_range=param_range, scoring="accuracy", cv=5)
	train_scores_mean = train_scores.mean(axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	validation_scores_mean = test_scores.mean(axis=1)
	validation_scores_std = np.std(test_scores, axis=1)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.fill_between(param_range, validation_scores_mean - validation_scores_std, validation_scores_mean + validation_scores_std, alpha=0.1)
	plt.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1)
	plt.plot(param_range, validation_scores_mean, label = 'Cross-Validation Score')
	plt.plot(param_range, train_scores_mean, label = 'Training Score')
	ax.set_xscale('log')
	plt.ylabel('Accuracy Score', fontsize = 14)
	plt.xlabel('γ', fontsize = 14)
	plt.legend()

def learning_curve_plot(model, data, target, scoring = 'accuracy', colorTrain='blue', colorTest='green'):
	train_sizes, train_scores, validation_scores = learning_curve(SVC(kernel = 'linear', C=7.5e-5), X = data, y = target, scoring = scoring)
	train_scores_mean = train_scores.mean(axis=1)
	train_scores_std = np.std(train_scores, axis=1)
	validation_scores_mean = validation_scores.mean(axis=1)
	validation_scores_std = np.std(validation_scores, axis=1)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.fill_between(train_sizes, validation_scores_mean - validation_scores_std, validation_scores_mean + validation_scores_std, alpha=0.1, color=colorTrain)
	plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color=colorTest)
	plt.plot(train_sizes, validation_scores_mean, label = 'Cross-Validation Score', color=colorTrain)
	plt.plot(train_sizes, train_scores_mean, label = 'Training score', color=colorTest)
	plt.ylabel('Accuracy Score', fontsize = 14)
	plt.xlabel('Training Examples', fontsize = 14)
	plt.legend()

def print_info(y_test, y_pred):
    print('Mean Absolute Error: ', metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error: ', metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error: ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
    print('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
    print('Classification Report:\n', classification_report(y_test, y_pred))
    print('Accuracy Score: ', accuracy_score(y_test, y_pred))


def print_results(true_value, pred):
    from sklearn.metrics import classification_report, confusion_matrix, \
    accuracy_score, f1_score, roc_auc_score, precision_score, recall_score
    print("accuracy: {}".format(accuracy_score(true_value, pred)))
    print("precision: {}".format(precision_score(true_value, pred)))
    print("recall: {}".format(recall_score(true_value, pred)))    
    print("roc-auc: {}".format(roc_auc_score(true_value, pred)))
    print("f1: {}".format(f1_score(true_value, pred)))
    print("weighted f1 score: ", f1_score(true_value, pred, average="weighted"))
    print(classification_report(true_value, pred))
    print("confusion_matrix: ", confusion_matrix(true_value, pred))

if __name__ == "__main__":
	# Prep Data, databases kept locally
	# SMOTE PCA ONEHOT Load
	# pickle_in = open('SMOTE_PCA_ONEHOT_DATA_X.pickle', "rb")
	# dataX = pickle.load(pickle_in)
	# pickle_in.close()
	# pickle_in = open('SMOTE_PCA_ONEHOT_DATA_Y.pickle', "rb")
	# dataY = pickle.load(pickle_in)
	# pickle_in.close()

	# Validation Curves
	# param_range = np.logspace(-30, -3, 10)
	# param_range = np.logspace(-8, -3, 10)
	# print(param_range)
	# validation_curve_plot(dataX, dataY, param_range)
	# plt.savefig("Valid_Curve_Linear_1e-3_1e3.png")
	# plt.savefig("Valid_Curve_Linear_1e-8_1e-3.png")
	# plt.show()
	# plt.clf()

	# 7.5e-05 optimal
	# optimal = 7.5e-05
	# svm = SVC(kernel = 'linear', C=optimal)

	# Plot Learning Curve
	# learning_curve_plot(svm, dataX, dataY)
	# plt.savefig("Learning_Curve_Linear.png")
	# plt.show()
	# plt.clf()

	# Print Testing data
	# x_train, x_test, y_train, y_test = train_test_split(dataX, dataY, test_size=0.2, random_state=0)
	# model = svm.fit(x_train, y_train)
	# pred = svm.predict(x_test)
	# print_results(y_test, pred)

	# Prep Data, databases kept locally
	# SMOTE PCA Load
	pickle_in = open('SMOTE_PCA_DATA_X.pickle', "rb")
	dataX = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open('SMOTE_PCA_DATA_Y.pickle', "rb")
	dataY = pickle.load(pickle_in)
	pickle_in.close()

	# Validation Curves
	# param_range = np.logspace(-5, 1, 10)
	# param_range = np.logspace(-3, -1, 10)
	# print(param_range)
	# validation_curve_plot(dataX, dataY, param_range)
	# plt.savefig("Valid_Curve_Linear_1e-5_1e1.png")
	# plt.savefig("Valid_Curve_Linear_1e-3_1e-1.png")
	# plt.show()
	# plt.clf()

	# 7.5e-03 optimal
	optimal = 8e-03
	svm = SVC(kernel = 'linear', C=optimal)

	# Plot Learning Curve
	# learning_curve_plot(svm, dataX, dataY)
	# plt.savefig("Learning_Curve_Linear.png")
	# plt.show()
	# plt.clf()

	# Print Testing data
	x_train, x_test, y_train, y_test = train_test_split(dataX, dataY, test_size=0.2, random_state=0)
	model = svm.fit(x_train, y_train)
	pred = svm.predict(x_test)
	print_results(y_test, pred)
	
