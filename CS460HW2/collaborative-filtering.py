# NOTES FOR DOCUMENTATION WRITE-UP:
# Assumptions:
#   943 users
#   1682 movies
#   column 1 - user, 2 - movie, 3 - rating
#   if user has not seen one of the movies, I set a default rating of 2.5 (half on the 1-5 rating scale)

# --------------------------------------- FUNCTIONS --------------------------------------- #


# output list of cosine similarities for each piece of data
def cosine_similarity(person_num, movie_num, training_data):

    person_movie_data = []  # create list for each user and their rating for each movie
    similarity_ratios = []

    # for each user
    for i in range(1, 944):

        temp = [2.5]*1683  # index 0 = user, 1-1682 = rating of each movie (default value = 2.5)
        temp[0] = i

        # create a list with a rating for each movie
        for row in training_data:
            if int(row[0]) == i:
                 temp[int(row[1])] = int(row[2])

        print(temp)
        person_movie_data.append(temp)


    # for user in person_movie_data:
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
similarities = cosine_similarity(person, movie, training_rows)

# for now k = 3
# find 3 highest cosine similarity to given person & movie

# k = 3
# k_nearest_neighbors(k, similarities)