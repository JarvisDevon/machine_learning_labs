import numpy as np

gradient = 3
c_value = 5

def set_x_distribution_train():
	x_values = np.zeros((50), dtype='float64')
	for i in range(0, 100):
		if i%2 == 0:
			x_values[i/2] = i+2 
	return x_values

def set_x_distribution_test():
	x_values = np.zeros((50), dtype='float64')
	for i in range(0, 100):
		if i%2 == 0:
			x_values[i/2] = i+1 
	return x_values

def fill_coords_from_x_distribution(x_distribution):
	coords = np.zeros((50,10,2), dtype='float64')
	for normal_distribution in range(0, len(x_distribution)):
		noise = np.random.normal(0,1,10)
		for coords_of_distribution in range(0, len(noise)):
			x_coord = x_distribution[normal_distribution] #one normal distribution per x_coord (x and y have a 																			linear relationship)
			y_coord = (gradient * x_coord) + c_value + noise[coords_of_distribution] # y value is x value plus noise, one noise perturbation per coord
			coords[normal_distribution][coords_of_distribution][0] = x_coord  
			coords[normal_distribution][coords_of_distribution][1] = y_coord
	return coords

def generate_data(startRange, endRange):
	#data_points = [(x,y) for x in range(11) for y in range(11)]
	set_of_normal_distributions = np.zeros((50), dtype='float64')
	set_of_normal_distributions = set_x_distribution_train() 
	data_points = np.zeros((50,10,2), dtype='float64')
	data_points = fill_coords_from_x_distribution(set_of_normal_distributions)
	return data_points

def covariance_of_x_and_y(data):#data is a set of gauss distributions around a line for 50 x values, 10 y values per distribution
	covariance_sum = 0	
	for gaussian_distribution in data:
		for coord in gaussian_distribution:
			number_to_add = coord[0] * coord[1]
			covariance_sum = covariance_sum + number_to_add
	return covariance_sum
	
def variance_of_x(data):  #data is a set of gauss distributions around a line for 50 x values, 10 y values per distribution
	variance_sum = 0
	for gaussian_distribution in data:
		for coord in gaussian_distribution:
			number_to_add = coord[0] * coord[0]
			variance_sum = variance_sum + number_to_add
	return variance_sum

def find_theta_one(data):
	sigmaXiYi = covariance_of_x_and_y(data)
	sigmaXiXi = variance_of_x(data)
	return sigmaXiYi/sigmaXiXi
	
def average_x(data): #data is a set of gauss distributions around a line for 50 x values, 10 y values per distribution
	sum_x = 0
	for gaussian_distribution in data:
		for coord in gaussian_distribution:
			sum_x = sum_x + coord[0]
	average = sum_x/(len(data)*len(gaussian_distribution))
	#print average
	return average

def average_y(data): #data is a set of gauss distributions around a line for 50 x values, 10 y values per distribution
	sum_y = 0
	#print data
	for gaussian_distribution in data:
		for coord in gaussian_distribution:
			#print "sum y: " + str(sum_y) + " + " + str(coord[1]) + " = " + str(sum_y + coord[1])
			sum_y = sum_y + coord[1]
	average = sum_y/(len(data)*len(gaussian_distribution))
	return average


def find_theta_two(data): #linear curve so x and y actual have the same average
	x_ave = average_x(data)
	y_ave = average_y(data)
	theta_one = find_theta_one(data)
	print x_ave
	print y_ave
	theta_two = y_ave - (theta_one * x_ave)
	#print y_ave
	return theta_two


def perform_linear_regression(data_points):
	theta_one = find_theta_one(data_points)
	theta_two = find_theta_two(data_points)
	print "Theta 1 value is " + str(theta_one)
	print "Theta 2 value is " + str(theta_two)
	
def compute_regression_equation_output(theta1, theta2, xi):
	return (theta1 * xi) + theta2

def compute_total_error(test_data, theta_one, theta_two):
	error_sum = 0
	for x in test_data:
		y_hat = compute_regression_equation_output(theta_one, theta_two, x)
		y_actual = (x*gradient) + c_value
		#print "y_actual = " + str(y_actual) + " y_hat = " + str(y_hat)
		error = abs(y_hat - y_actual)
		error_sum = error_sum + error
	return error_sum

def main():
	experiment_data = generate_data(0, 100)
	perform_linear_regression(experiment_data)
	theta_one = find_theta_one(experiment_data)
	theta_two = find_theta_two(experiment_data)
	test_data_x_values = set_x_distribution_test()
	reg_error = compute_total_error(test_data_x_values, theta_one, theta_two)
	print "The total error after regression is: " + str(reg_error)
	print "Average error after regression is: " + str(reg_error/500)

if __name__ == '__main__':
	main()
