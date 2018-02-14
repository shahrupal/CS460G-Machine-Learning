# NOTES FOR DOCUMENTATION WRITE-UP:
# Assumptions:
#   943 users
#   1682 movies
#   column 1 - user, 2 - movie, 3 - rating
#   if user has not seen one of the movies, I set a default rating of 2.5 (half on the 1-5 rating scale)
# Slow runtime

import math

# --------------------------------------- FUNCTIONS --------------------------------------- #


# output list of cosine similarities for each piece of data
def cosine_similarity(person_num, movie_num, training_data):

    person_ratings_data = []  # create list for each user and their rating for each movie
    similarity_ratios = []

    # for each user
    for i in range(1, 944):

        temp = [2.5]*1683  # index 0 = user, 1-1682 = rating of each movie (default value = 2.5)
        temp[0] = i

        # create a list with a rating for each movie
        for row in training_data:
            if int(row[0]) == i:
                 temp[int(row[1])] = int(row[2])

        # print(temp)
        person_ratings_data.append(temp)

    # store given user's data (number and ratings)
    given_info = person_ratings_data[person_num - 1]
    print(given_info)

    # go through list of each user and their ratings
    for info in person_ratings_data:

        dot_product = 0  # numerator
        magnitude = 0   # denominator
        current_magnitude = 0
        given_magintude = 0

        # don't calculate cosine similarity between given person and themself
        if info[0] != person_num:

            # for each movie rating
            for index in range(1, 1683):

                # can't calculate similarity of movie user is trying to find rating of
                if index != movie_num:

                    dot_product += info[index] * given_info[index]
                    current_magnitude += info[index] * info[index]
                    given_magintude += given_info[index] * given_info[index]

            # calculate magnitude of current person and given person
            magnitude = math.sqrt(current_magnitude) * math.sqrt(given_magintude)

            similarity_ratios.append(dot_product / magnitude)

        # USE 0 AS PLACEHOLDER
        else:
            similarity_ratios.append(0)

    #     print(user)

    return similarity_ratios


# ----------------------------------------- MAIN ----------------------------------------- #


# open training data file
training_file = open("data/u1-base.base", "r")
training_file_contents = training_file.read()

# store each row in a list
training_rows = []
for line in training_file_contents.splitlines():
    training_rows.append(line.split())


# ask user for the person number & movie number they would like to use to predict the rating
person = input("Please input the number of the person you are interested in: ")
movie = input("Please input the number of the movie you are interested in: ")

# calculate cosine similarity for each piece of data in training
similarities = cosine_similarity(int(person), int(movie), training_rows)
print(similarities)
print(len(similarities))

# TODO:

# for now k = 3

# create function k_nearest_neighbors(k, similarities)
# find highest 3 cosine similarities and their info - person & ratings (person = index + 1)

# create function predicted_rating(highest_similarities, highest_info)