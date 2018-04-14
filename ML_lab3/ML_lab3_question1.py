import numpy as np
import random

laplace_smoothing = 1.0       #add in Laplace smoothing, 1 means it's included, 0 means it's not

f = open("data/simple-food-reviews.txt", 'r')
data = []
line = f.readline()
while line:
    data.append(line)
    line = f.readline()


num_total_data = len(data)
num_total_train_data = 12.0
num_total_test_data = 6.0
training_data_indices = []
training_data = []
test_data = []

# for i in range(0,2):                          #Receives test data input from the console
#     input_test_data = raw_input("Please provide your restaurant review")
#     test_data.append(input_test_data)

for i in range(0, len(data)):
    training_data_indices.append(0)

i = 0
while i < num_total_train_data:
    random_index = random.randint(0,len(data)-1)
    if not training_data_indices[random_index] == 1:
        training_data_indices[random_index] = 1
        training_data.append(data[random_index])
        i = i + 1

for i in range(0, len(data)):
    if training_data_indices[i] == 0:
        test_data.append(data[i])

training_data.sort()

index_of_split = 0
found_split = 0

num_positives_used_to_train = 0
num_negatives_used_to_train = 0
num_positives_used_to_test = 0
num_negatives_used_to_test = 0

for k in range(0, len(training_data)):
    if not found_split:
        index_of_split = k
    if not training_data[k][0] == "-":
        num_positives_used_to_train = num_positives_used_to_train + 1
        found_split = 1

num_negatives_used_to_train = num_total_train_data - num_positives_used_to_train
num_positives_used_to_test = (num_total_train_data/2) - num_positives_used_to_train
num_negatives_used_to_test = (num_total_train_data/2) - num_negatives_used_to_train

words_list = {}

for i in range(index_of_split, len(training_data)):  #Add the positive review's words into the word list
    review = training_data[i][1:].split()
    for word in review:
        if word in words_list:
            if not words_list[word][5] == 1:
                words_list[word][0] = words_list[word][0] + 1
                words_list[word][1] = words_list[word][1] + 1
                words_list[word][5] = 1
        elif len(word) > 0:                 #Add word if it is not a stop word
            words_list[word] = [1,1,0,0,0,1]
    for word in words_list:
        words_list[word][5] = 0
#[total count, positive count, negative count, positives fracton, negatives fraction, seen already]

for i in range(0, index_of_split):   #Add the negative review's words into the word list
    review = training_data[i][2:].split()      #Begins where above loop left of: index_of_split
    for word in review:
        if word in words_list:
            if not words_list[word][5] == 1:
                words_list[word][0] = words_list[word][0] + 1
                words_list[word][2] = words_list[word][2] + 1
                words_list[word][5] = 1
        elif len(word) > 2:                 #Add word if it is not a stop word
            words_list[word] = [1,0,1,0,0,1]
    for word in words_list:
        words_list[word][5] = 0
# [total count, positive count, negative count, positives fracton, negatives fraction, seen already]

for word in words_list:
    positive_numerator = float(words_list[word][1]) + laplace_smoothing
    negative_numerator = float(words_list[word][2]) + laplace_smoothing
    positivie_fraction = positive_numerator/(num_positives_used_to_train + (2*laplace_smoothing))
    negative_fraction = negative_numerator/(num_negatives_used_to_train + (2*laplace_smoothing))
    words_list[word][3] = positivie_fraction
    words_list[word][4] = negative_fraction

training_prior_prob_positive = num_positives_used_to_train/float(num_total_train_data)
training_prior_prob_negative = num_negatives_used_to_train/float(num_total_train_data)

remove_vector = []

for word in words_list:
    if abs(words_list[word][3] - words_list[word][4]) < 0.1:
        remove_vector.append(word)

for word in remove_vector:
    del words_list[word]

words_vector = []

for word in words_list:
    words_vector.append(word)

def convert_review_to_input_vector(split_review):
    input_vector = []
    for i in range(0, len(words_vector)):
        input_vector.append(0)
    for entry in range(0, len(words_vector)):
        for word in split_review[1:]:
            if words_vector[entry] == word:
                input_vector[entry] = 1
    return input_vector

def prob_input_given_positive(split_review):
    likelihood = 1
    input_vector = convert_review_to_input_vector(split_review)
    for index in range(1, len(input_vector)):
        if input_vector[index] == 1:
            likelihood = likelihood * words_list[words_vector[index]][3]
        else:
            likelihood = likelihood * (1 - words_list[words_vector[index]][3])
    return likelihood

def prob_input_given_negative(split_review):
    likelihood = 1
    input_vector = convert_review_to_input_vector(split_review)
    for index in range(2, len(input_vector)):
        if input_vector[index] == 1:
            likelihood = likelihood * words_list[words_vector[index]][4]
        else:
            likelihood = likelihood * (1 - words_list[words_vector[index]][4])
    return likelihood

def prob_input_across_all_condition(split_review):
    probability = (prob_input_given_positive(split_review) * training_prior_prob_positive) + (prob_input_given_negative(split_review) * training_prior_prob_negative)
    return probability



def classify(split_review):
    positive_posterior_probability = ((prob_input_given_positive(split_review) * training_prior_prob_positive))/(prob_input_across_all_condition(split_review))
    negative_posterior_probability = ((prob_input_given_negative(split_review) * training_prior_prob_negative))/(prob_input_across_all_condition(split_review))
    if positive_posterior_probability > negative_posterior_probability:
        return 1
    else:
        return 0

def compare_result(split_review):
    actual_connotation = 1
    if split_review[0] == "-":
        actual_connotation = 0
    classification = classify(split_review)
    if classification == actual_connotation:
        return 1
    else:
        return 0

def make_confusion_matrix(correct_pos, correct_neg, miss_pos, miss_neg):
    print "--------"
    print "|" + str(correct_pos) + " | " + str(miss_neg) + "|"
    print "|" + str(miss_pos) + " | " + str(correct_neg) + "|"
    print "--------"

def main():
    correct_pos = 0
    correct_neg = 0
    miss_pos = 0
    miss_neg = 0
    for review in test_data:
        splited_review = review.split()
        if splited_review[0] == "1" and  compare_result(splited_review) == 1:
            correct_pos = correct_pos + 1
        elif splited_review[0] == "-1" and  compare_result(splited_review) == 1:
            correct_neg = correct_neg + 1
        elif splited_review[0] == "1" and  compare_result(splited_review) == 0:
            miss_pos = miss_pos + 1
        else:
            miss_neg = miss_neg + 1

    make_confusion_matrix(correct_pos, correct_neg, miss_pos, miss_neg)

if __name__ == '__main__':
    main()
