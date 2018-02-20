import math
from tqdm import tqdm

# --------------------------------------- FUNCTIONS --------------------------------------- #

# outputs a list that has a list for each user and their ratings for all movies
# defaults a rating of 0 if movie has not been seen by specific user
def store_user_ratings(training_data):

    # create list for each user and their rating for each movie
    person_ratings_data = []

    # for each user
    for i in range(1, 944):

        # index 0 = user, 1-1682 = rating of each movie (default value = 0)
        temp = [0] * 1683
        temp[0] = i

        # create a list with a rating for each movie
        for row in training_data:
            if int(row[0]) == i:
                temp[int(row[1])] = int(row[2])

        person_ratings_data.append(temp)

    return person_ratings_data


# output list of cosine similarities for each piece of data
def cosine_similarity(user_id, movie_id, user_ratings):

    # store given user's data (number and ratings)
    given_info = user_ratings[user_id - 1]

    iteration = 0
    similarity_ratios = []

    # go through list of each user and their ratings
    for info in user_ratings:

        dot_product = 0  # numerator
        magnitude = 0   # denominator
        current_magnitude = 0
        given_magnitude = 0
        iteration += 1

        # don't calculate cosine similarity between given person and themself
        # don't calculate cosine similarity if user has not seen given movie (keep it set at 0)
        if info[0] != user_id and info[movie_id] != 0:

            # for each movie rating
            for index in range(1, 1683):

                # do not calculate similarity of movie user is trying to find rating of
                if index != movie_id:

                    dot_product += info[index] * given_info[index]
                    current_magnitude += info[index] * info[index]
                    given_magnitude += given_info[index] * given_info[index]

            # calculate magnitude of current person and given person
            magnitude = math.sqrt(current_magnitude) * math.sqrt(given_magnitude)

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

    return similarity_ratios


# output list of 'k' highest similarities (data of user with highest similarities)
def top_similarities(k, cosine_similarities):

    top = (sorted(cosine_similarities, key=lambda x: (x[1]))[-k:])
    return top


# find ratings of movies associated with top 3 similarities
def associated_ratings(user_ratings, k_similarities, movie_id):

    ratings = []
    iteration = 0

    for similarity in k_similarities:

        ratings.append(user_ratings[similarity[0] - 1][movie_id])
        iteration += 1

    return ratings


# uses top three similarities and associated ratings to make a prediction of rating of given movie for given user
# if no similarities (no one has watched the given movie), make a prediction of 0
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


# return error squared for individual test set
def find_error_squared(prediction, actual):

    error = (prediction - actual) ** 2
    return error


# return mean squared error (overall error)
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
        training_rows.append(line.split())

    # open training data file
    test_file = open("data/u1-test.test", "r")
    test_file_contents = test_file.read()


    # store each row in a list
    test_rows = []
    for line in test_file_contents.splitlines():
        test_rows.append(line.split())

    print("LOADING...")

    # store ratings for given movie for each user
    user_ratings = store_user_ratings(training_rows)

    individual_error = []

    # iterate through all test data in .test file
    for test in tqdm(test_rows):

        # calculate cosine similarity for each piece of data in training
        similarities = cosine_similarity(int(test[0]), int(test[1]), user_ratings)

        # find the k nearest neighbors
        k = 3
        nearest_similarities = top_similarities(k, similarities)

        # store ratings of movies associated with top 'k' similarities
        nearest_ratings = associated_ratings(user_ratings, nearest_similarities, int(test[1]))

        # store prediction of rating
        prediction = predict_rating(nearest_similarities, nearest_ratings)

        # find error for individual test set
        individual_error.append(find_error_squared(prediction, int(test[2])))

    # FIND OVERALL ERROR
    print(find_overall_error(individual_error, len(test_rows)))


main()