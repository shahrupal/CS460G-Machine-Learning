import random
import tqdm
import copy
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
            for index in range(len(user_ratings)):

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

    ratings = []
    iteration = 0

    for similarity in k_similarities:

        ratings.append(user_ratings[similarity[0] - 1][movie_id])
        iteration += 1

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

# open training data file
training_file = open("data/u1-base.base", "r")
training_file_contents = training_file.read()

# store each row in a list
data = []
for line in training_file_contents.splitlines():
    data.append(line.split())

# shuffle the training rows
random.shuffle(data, random.random)

# split data into 5 folds
folds = []
fold1 = data[0:16000]
fold2 = data[16000:32000]
fold3 = data[32000:48000]
fold4 = data[48000:54000]
fold5 = data[54000:60000]

folds.append(fold1)
folds.append(fold2)
folds.append(fold3)
folds.append(fold4)
folds.append(fold5)

print("LOL LOADING...")

k = 2
for i in range(5):

    training_rows = copy.copy(folds)

    test_rows = training_rows[i]
    training_rows.pop(i)

    print('temp', len(training_rows))
    print(len(folds))

    user_ratings = store_user_ratings(data)
    individual_error = []

    # TEST ALL DATA
    for test in tqdm(test_rows):

        similarities = cosine_similarity(int(test[0]), int(test[1]), user_ratings)
        nearest_similarities = top_similarities(k, similarities)
        nearest_ratings = associated_ratings(user_ratings, nearest_similarities, int(test[1]))
        prediction = predict_rating(nearest_similarities, nearest_ratings)
        individual_error.append(find_error_squared(prediction, int(test[2])))

    k += 2

# FIND OVERALL ERROR
print(find_overall_error(individual_error, len(test_rows)))




