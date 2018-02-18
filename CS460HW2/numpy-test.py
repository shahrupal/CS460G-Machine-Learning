# NOTES FOR DOCUMENTATION WRITE-UP:
# Assumptions:
#   943 users
#   1682 movies
#   column 1 - user, 2 - movie, 3 - rating
#   if user has not seen one of the movies, I set a default rating of 0
# Slow runtime

import math
import time
import numpy as np
from tqdm import tqdm

np.set_printoptions(suppress=True)

# --------------------------------------- FUNCTIONS --------------------------------------- #

def store_user_ratings(training_data):

    person_ratings_data = []  # create list for each user and their rating for each movie
    person_ratings_data = np.zeros((943, 1682))

    for row in training_data:

        person_ratings_data[row[0] - 1][row[1] - 1] = float(row[2])

    # # for each user
    # for i in range(1, 944):
    #
    #     temp = [0] * 1683  # index 0 = user, 1-1682 = rating of each movie (default value = 0)
    #     temp[0] = i
    #
    #     # create a list with a rating for each movie
    #     for row in training_data:
    #         if int(row[0]) == i:
    #             temp[int(row[1])] = int(row[2])
    #
    #     # print(temp)
    #     person_ratings_data.append(temp)

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

    # open training data file
    training_file = open("data/u1-base.base", "r")
    training_file_contents = training_file.read()

    # store each row in a list
    training_rows = []
    for line in training_file_contents.splitlines():
        training_rows.append([int(x) for x in line.split()])

    training_rows = np.array(training_rows)
    # print(training_rows)

    # open training data file
    test_file = open("data/u1-test.test", "r")
    test_file_contents = test_file.read()


    # store each row in a list
    test_rows = []
    for line in test_file_contents.splitlines():
        test_rows.append([int(x) for x in line.split()])
    test_rows = np.array(test_rows)

    print("LOL LOADING...")

    # store ratings for given movie for each user
    user_ratings = store_user_ratings(training_rows)
    user_ratings = np.array(user_ratings)

    individual_error = []

    # print(training_rows)
    # print(test_rows)
    # print(user_ratings)
    # print('======================================')

    # TEST ALL DATA
    for test in tqdm(test_rows):

        # calculate cosine similarity for each piece of data in training
        similarities = cosine_similarity(test[0], test[1], user_ratings)
        # print(similarities)

        # input('stop')

        # find the k nearest neighbors
        k = 3
        nearest_similarities = top_similarities(k, similarities)
        # print(nearest_similarities)

        # store ratings of movies associated with top 'k' similarities
        nearest_ratings = associated_ratings(user_ratings, nearest_similarities, int(test[1]))
        # print(nearest_ratings)

        # input('stop')

        prediction = predict_rating(nearest_similarities, nearest_ratings)

        individual_error.append(find_error_squared(prediction, int(test[2])))

    # FIND OVERALL ERROR
    print(find_overall_error(individual_error, len(test_rows)))

main()