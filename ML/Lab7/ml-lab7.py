# Linear Regression With Stochastic Gradient Descent for Wine Quality
from random import seed
from random import randrange
from csv import reader
from math import sqrt
 
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset
 
# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
 
# Find the min and max values for each column
def dataset_minmax(dataset):
	minmax = list()
	for i in range(len(dataset[0])):
		col_values = [row[i] for row in dataset]
		value_min = min(col_values)
		value_max = max(col_values)
		minmax.append([value_min, value_max])
	return minmax
 
# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
	for row in dataset:
		for i in range(len(row)):
			row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
 
# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 
# Calculate root mean squared error
def rmse_metric(actual, predicted):
	sum_error = 0.0
	for i in range(len(actual)):
		prediction_error = predicted[i] - actual[i]
		sum_error += (prediction_error ** 2)
	mean_error = sum_error / float(len(actual))
	return sqrt(mean_error)
 
# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
		predicted = linear_regression(algorithm, train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		rmse = rmse_metric(actual, predicted)
		scores.append(rmse)
	return scores
 
# Make a prediction with coefficients
def predict(row, coefficients):
	yhat = coefficients[0]
	for i in range(len(row)-1):
		yhat += coefficients[i + 1] * row[i]
	return yhat
 
# Estimate linear regression coefficients using stochastic gradient descent
def coefficients_sgd(train, l_rate, n_epoch):
	coef = [0.0 for i in range(len(train[0]))]
	for epoch in range(n_epoch):
		for row in train:
			yhat = predict(row, coef)
			error = yhat - row[-1]
			coef[0] = coef[0] - l_rate * error
			for i in range(len(row)-1):
				coef[i + 1] = coef[i + 1] - l_rate * error * row[i]
			# print(l_rate, n_epoch, error)
	return coef

# Estimate linear regression coefficients using batch gradient descent
def coefficients_bgd(train, l_rate, n_epoch):
	coef = [0.0 for i in range(len(train[0]))]
	for epoch in range(n_epoch):
		for i in range(len(train[0])-1):
			for row in train:
				sum_error_row = 0
				yhat = predict(row, coef)
				error = yhat - row[-1]
				coef[0] = coef[0] - l_rate * error
				for i in range(len(row)-1):
					sum_error_row = sum_error_row + error * row[i]		
			coef[i + 1] = coef[i + 1] - l_rate * sum_error_row
			print(coef[i + 1],i)
			# print(l_rate, n_epoch, error)
	return coef

# Linear Regression Algorithm With Passed Gradient Descent Algorithm
def linear_regression(coefficients_algorithm, train, test, l_rate, n_epoch):
	predictions = list()
	coef = coefficients_algorithm(train, l_rate, n_epoch)
	for row in test:
		yhat = predict(row, coef)
		predictions.append(yhat)
	return(predictions)
 
# Linear Regression on iris dataset
seed(1)
# load and prepare data
filename = 'iris.data'
dataset = load_csv(filename)
for i in range(len(dataset[0])):
	str_column_to_float(dataset, i)
# normalize
minmax = dataset_minmax(dataset)
normalize_dataset(dataset, minmax)
# evaluate algorithm
n_folds = 10
l_rate = 0.01
n_epoch = 50
sgd_scores = evaluate_algorithm(dataset, coefficients_sgd, n_folds, l_rate, n_epoch)
print('SGD - Scores: %s' % sgd_scores)
print('SGD - Mean RMSE: %.3f' % (sum(sgd_scores)/float(len(sgd_scores))))
bgd_scores = evaluate_algorithm(dataset, coefficients_bgd, n_folds, l_rate, n_epoch)
print('BGD - Scores: %s' % bgd_scores)
print('BGD - Mean RMSE: %.3f' % (sum(bgd_scores)/float(len(bgd_scores))))
