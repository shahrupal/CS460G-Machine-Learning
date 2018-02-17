# NOTES FOR DOCUMENTATION WRITE-UP:
# Assumptions:
#   943 users
#   1682 movies
#   column 1 - user, 2 - movie, 3 - rating
#   if user has not seen one of the movies, I set a default rating of 0
# Slow runtime

import math
import time
from tqdm import tqdm


# --------------------------------------- FUNCTIONS --------------------------------------- #

def store_user_ratings(training_data):

    person_ratings_data = []  # create list for each user and their rating for each movie

    # for each user
    for i in range(1, 944):

        temp = [0] * 1683  # index 0 = user, 1-1682 = rating of each movie (default value = 0)
        temp[0] = i

        # create a list with a rating for each movie
        for row in training_data:
            if int(row[0]) == i:
                temp[int(row[1])] = int(row[2])

        # print(temp)
        person_ratings_data.append(temp)

    return person_ratings_data


# output list of cosine similarities for each piece of data
def cosine_similarity(user_id, movie_id, user_ratings):

    # store given user's data (number and ratings)
    given_info = user_ratings[user_id - 1]
    # print(given_info)

    iteration = 0
    similarity_ratios = []

    # go through list of each user and their ratings
    for info in user_ratings:

        dot_product = 0  # numerator
        magnitude = 0   # denominator
        current_magnitude = 0
        given_magintude = 0
        iteration += 1

        # don't calculate cosine similarity between given person and themself
        # don't calculate cosine similarity if user has not seen given movie (keep it set at 0)
        if info[0] != user_id and info[movie_id] != 0:

            # for each movie rating
            for index in range(1, 1683):

                # can't calculate similarity of movie user is trying to find rating of
                if index != movie_id:

                    dot_product += info[index] * given_info[index]
                    current_magnitude += info[index] * info[index]
                    given_magintude += given_info[index] * given_info[index]

            # calculate magnitude of current person and given person
            magnitude = math.sqrt(current_magnitude) * math.sqrt(given_magintude)

            t = []
            t.append(iteration)

            if magnitude != 0:
                t.append(dot_product / magnitude)
            else:
                t.append(0)
            similarity_ratios.append(t)

        # USE 0 AS PLACEHOLDER
        else:
            t = []
            t.append(iteration)
            t.append(0)
            similarity_ratios.append(t)

    # print(similarity_ratios)
    return similarity_ratios


# output list of 'k' highest similarities (data of user with highest similarities)
def top_similarities(k, cosine_similarities):

    top = (sorted(cosine_similarities, key=lambda x: (x[1]))[-k:])
    return top


# find ratings of movies associated with top 3 similarities
# if no similarities (no one has watched the given movie), make a prediction of 0
def associated_ratings(user_ratings, k_similarities, movie_id):

    ratings = [0] * 3
    iteration = 0

    for similarity in k_similarities:

        ratings[iteration] = (user_ratings[similarity[0] - 1][movie_id])
        iteration += 1

    print(ratings)







# ----------------------------------------- MAIN ----------------------------------------- #

# open training data file
training_file = open("data/u1-base.base", "r")
training_file_contents = training_file.read()

# store each row in a list
training_rows = []
for line in training_file_contents.splitlines():
    training_rows.append(line.split())

# open training data file
test_file = open("data/u1-test.test", "r")
test_file_contents = test_file.read()


# store each row in a list
test_rows = []
for line in test_file_contents.splitlines():
    test_rows.append(line.split())


# user = input("User: ")
# movie = input("Movie: ")

print("LOL LOADING...")

# store ratings for given movie for each user
user_ratings = store_user_ratings(training_rows)

# TEST ALL DATA
for test in (test_rows):

    # calculate cosine similarity for each piece of data in training
    similarities = cosine_similarity(int(test[0]), int(test[1]), user_ratings)
    print(similarities)

    # find the k nearest neighbors
    k = 3
    nearest_neighbors = top_similarities(k, similarities)
    print(nearest_neighbors)

    # store ratings of movies associated with top 'k' similarities
    neigbor_ratings = associated_ratings(user_ratings, nearest_neighbors, int(test[1]))

    input("stop")



