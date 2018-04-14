import numpy as np
import numdifftools as nd
import numdifftools.nd_algopy as nda


num_dimensions = 2					####################################
function = lambda c: c[0]**10 + c[1] - 5		####################################
jacobian = nda.Jacobian(function, method='reverse')
inverse_jacobian = np.zeros((num_dimensions-1, 1))

def generate_inverse_jac(jac):
	inverse_jac = np.zeros((num_dimensions, 1))
	for i in range(len(jac)):
		if not(jac[i] == 0):
			#print "Changing " + str(jac[i]) + " to " + str(1/jac[i])
			inverse_jac[i] = 1/jac[i]
		else:
			inverse_jac[i] = 0
	return inverse_jac

def vector_scaler_mult(in_vector, scaler_value):
	out_vector = np.zeros((num_dimensions, 1))
	for i in range(len(in_vector)):
		out_vector[i] = in_vector[i]*scaler_value
	return out_vector

def vector_add(vector_one, vector_two):
	out_vector = np.zeros((num_dimensions, 1))
	for i in range(len(vector_one)):
		out_vector[i] = vector_one[i]+vector_two[i]
	return out_vector

def newton_raphson_iterative():
	start_vector = np.array([1.75,1.75])				###############################
	carry_vector = start_vector
	function_output = function([1.75,1.75])			###############################
	output_jacobian = jacobian([1.75,1.75])			###############################
	vector_jacobian = output_jacobian[0]
	print vector_jacobian
	output_inverse_jacobian = generate_inverse_jac(vector_jacobian)
	inverse_jacobian =np.zeros((num_dimensions))
	inverse_jacobian[0] = output_inverse_jacobian[0][0]
	inverse_jacobian[1] = output_inverse_jacobian[1][0]	##################################
	param_shift_vector = np.multiply(inverse_jacobian, function_output)
	param_shift_vector = np.multiply(param_shift_vector, -1/2)
	param_shift_sum = 0
	for i in range(len(param_shift_vector)):
		param_shift_sum = param_shift_sum + abs(param_shift_vector[i])

	#while(param_shift_sum >= 0.000000000000000000000000000000000000001):
	while(param_shift_sum >= 0.0000000000001):
		output_carry_vector = vector_add(carry_vector, param_shift_vector)
		carry_vector = np.zeros(num_dimensions)
		carry_vector[0] = output_carry_vector[0][0]
		carry_vector[1] = output_carry_vector[1][0] ######################################
		function_output = function([carry_vector[0],carry_vector[1]]) ############ ############################
		output_jacobian = jacobian([carry_vector[0],carry_vector[1]]) #############################
		vector_jacobian = output_jacobian[0]
		output_inverse_jacobian = generate_inverse_jac(vector_jacobian)
		inverse_jacobian =np.zeros((num_dimensions))
		inverse_jacobian[0] = output_inverse_jacobian[0][0]
		inverse_jacobian[1] = output_inverse_jacobian[1][0]
		param_shift_vector = np.multiply(inverse_jacobian, function_output)
		param_shift_vector = np.multiply(param_shift_vector, -0.5)     #Note learning rate was added
		print "param shift vector is: " + str(param_shift_vector)
		param_shift_sum = 0
		for i in range(len(param_shift_vector)):
			param_shift_sum = param_shift_sum + abs(param_shift_vector[i])
		print "param shift sum is: " + str(param_shift_sum)
		print "***********************************************************************************************************"

	return(carry_vector)
	

def main():
	optimal_coords_approx = newton_raphson_iterative()
	print "Optimal parameters are: " + str(optimal_coords_approx[0]) + ":" + str(optimal_coords_approx[1])

if __name__ == '__main__':
	main()
