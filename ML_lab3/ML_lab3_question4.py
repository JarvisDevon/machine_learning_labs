import csv
import random

with open("data/smalldigits.csv") as f:
    images = []
    reader = csv.reader(f)
    for row in reader:
        images.append(row)

pixels = []

training_images = []
training_images_indexes = []
test_images = []

for i in range(0, len(images)):
    training_images_indexes.append(0)

for i in range(0, 64):
    count_vector = []
    for j in range(0,10):
        count_vector.append(0.0)
    pixels.append(count_vector)

for i in range(0, int(0.8 * len(images))):
    random_index = random.randint(0,len(images)-1)
    training_images.append(images[random_index])
    training_images_indexes[random_index] = 1

for i in range(0, len(images)):
    if not training_images_indexes[i] == 1:
        test_images.append(images[i])

totals_vector = []
priors_vector = []
for i in range(0,10):
    totals_vector.append(0.0)
    priors_vector.append(0.0)

for image in training_images:
    current_image_category = int(image[64])
    totals_vector[current_image_category] = totals_vector[current_image_category] + 1
    for index in range(0, len(image)-1):
        if image[index] == "1":
            pixels[index][current_image_category] = pixels[index][current_image_category] + 1

for index in range(0, len(totals_vector)):
    priors_vector[index] = totals_vector[index]/len(images)

def probability_of_image_given_category(image, category):
    probability = 1.0
    for index in range(0, len(image) - 1):
        if image[index] == "1":
            probability = probability * (pixels[index][category]/totals_vector[category])
        else:
            probability = probability * (1 - (pixels[index][category] / totals_vector[category]))

    return probability

def normalization_term(image):
    probability = 0.0
    for category in range(0, 10):
        probability = probability + (probability_of_image_given_category(image, category)*priors_vector[category])
    return probability

def calc_posterior(image, category):
    probability = ((probability_of_image_given_category(image, category) * priors_vector[category]) + 1.0)/(normalization_term(image) + 10.0)
    return probability

def classify(image):
    index_of_arg_max = 0
    probailities_vector = []
    for i in range(0, 10):
        probailities_vector.append(0)

    for category in range(0, 10):
        probailities_vector[category] = calc_posterior(image, category)
        if probailities_vector[category] > probailities_vector[index_of_arg_max]:
            index_of_arg_max = category
    return index_of_arg_max

def compute_accuracy():
    confusion_matrix = []
    for i in range(0, 10):
        guess_vector = []
        for j in range(0, 10):
            guess_vector.append(0)
        confusion_matrix.append(guess_vector)

    for image in test_images:
        classification = classify(image)
        confusion_matrix[int(image[64])][classification] = confusion_matrix[int(image[64])][classification] + 1

    for row in confusion_matrix:
        print row


def main():
    compute_accuracy()

if __name__ == '__main__':
    main()
