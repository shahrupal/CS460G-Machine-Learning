# NOTES FOR DOCUMENTATION WRITE-UP:
# Assumptions:
#   943 users
#   1682 movies
#   column 1 - user, 2 - movie, 3 - rating
#   if user has not seen one of the movies, I set a default rating of 0
# Slow runtime

import math
import time
import copy
import numpy as np
from tqdm import tqdm

np.set_printoptions(suppress=True)

# --------------------------------------- FUNCTIONS --------------------------------------- #

def store_user_ratings(training_data):

    person_ratings_data = []  # create list for each user and their rating for each movie
    person_ratings_data = np.zeros((943, 1682))  # fill with zeroes

    for row in training_data:

        person_ratings_data[row[0] - 1][row[1] - 1] = float(row[2])

    return person_ratings_data


# output list of cosine similarities for each piece of data
def cosine_similarity(user_id, movie_id, user_ratings):

    # store given user's data (number and ratings)
    # print(user_id)
    given_info = user_ratings[user_id - 1]

    # print(given_info)

    iteration = 0
    similarity_ratios = []

    # go through list of each user and their ratings
    for info in user_ratings:
        iteration += 1

        # don't calculate cosine similarity between given person and themself
        # don't calculate cosine similarity if user has not seen given movie (keep it set at 0)
        if iteration != user_id and info[movie_id - 1] != 0:

                # print(info, given_info)

                dot_product = np.sum(info * given_info)
                # print(iteration)
                # print(dot_product)

                current_magnitude = np.sum(info * info)
                given_magnitude = np.sum(given_info * given_info)

                # calculate magnitude of current person and given person
                magnitude = math.sqrt(current_magnitude * given_magnitude)

                if magnitude != 0:
                    sim = (dot_product / magnitude)
                else:
                    sim = 0
                similarity_ratios.append([iteration, sim])

        # USE 0 AS PLACEHOLDER
        else:
            similarity_ratios.append([iteration, 0])

    # print(similarity_ratios)
    return similarity_ratios


# output list of 'k' highest similarities (data of user with highest similarities)
def top_similarities(k, cosine_similarities):

    top = (sorted(cosine_similarities, key=lambda x: (x[1]))[-k:])
    return top


# find ratings of movies associated with top 3 similarities
# if no similarities (no one has watched the given movie), make a prediction of 0
def associated_ratings(user_ratings, k_similarities, movie_id):

    ratings = []

    for similarity in k_similarities:

        ratings.append(user_ratings[similarity[0] - 1][movie_id - 1])

    return ratings


def predict_rating(similarities, ratings):

    prediction = 0
    numerator = 0
    denominator = 0

    for i in range(len(similarities)):

        numerator += similarities[i][1] * ratings[i]
        denominator += similarities[i][1]

    if denominator != 0:
        prediction = numerator / denominator

    return prediction


# return error squared for individual test point
def find_error_squared(prediction, actual):

    error = (prediction - actual) ** 2
    return error


# return mean squared average error
def find_overall_error(errors, total):

    overall_error = 0

    for i in range(len(errors)):
        overall_error += errors[i]

    overall_error = overall_error / total
    return overall_error

# ----------------------------------------- MAIN ----------------------------------------- #

def main():

    # CROSS VALIDATE FOR EACH K VALUE
    # k=2, k=4, k=6, k=8, k=10
    for k in range(2, 12, 2):

        print('k =', k)

        # open training data file
        training_file = open("data/u1-base.base", "r")
        training_file_contents = training_file.read()

        # store each row in a list
        training_rows = []
        for line in training_file_contents.splitlines():
            training_rows.append([int(x) for x in line.split()])

        training_rows = np.array(training_rows)

        # shuffle training rows
        np.random.shuffle(training_rows)

        fold1 = training_rows[0:16000]
        fold2 = training_rows[16000:32000]
        fold3 = training_rows[32000:48000]
        fold4 = training_rows[48000:64000]
        fold5 = training_rows[64000:80000]

        folds = []
        folds.append(fold1)
        folds.append(fold2)
        folds.append(fold3)
        folds.append(fold4)
        folds.append(fold5)

        # for each fold
        for i in range(5):

            training = copy.copy(folds)
            testing = training[i]  # test on one fold

            training.pop(i)
            training = np.concatenate((training[0],training[1],training[2],training[3]), axis=0)

            # print(len(training))

            # store ratings for given movie for each user
            user_ratings = store_user_ratings(training)
            user_ratings = np.array(user_ratings)

            individual_error = []

            # TEST ALL DATA
            for test in tqdm(testing):

                similarities = cosine_similarity(test[0], test[1], user_ratings)
                nearest_similarities = top_similarities(k, similarities)
                nearest_ratings = associated_ratings(user_ratings, nearest_similarities, int(test[1]))
                prediction = predict_rating(nearest_similarities, nearest_ratings)
                individual_error.append(find_error_squared(prediction, int(test[2])))

            print(find_overall_error(individual_error, len(testing)))

main()