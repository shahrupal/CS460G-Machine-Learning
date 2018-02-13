import csv

# read in training data
# separate columns and store
    # 1st = user
    # 2nd = movie
    # 3rd = rating
    # 4th = ???
# ask for user input for person & movie? do we ask for a rating guess? output rating for movie? email brent


# open training data file
training_file = open("data/u1-base.base", "r")
training_file_contents = training_file.read()

# store each row in a list
training_rows = []
for line in training_file_contents.splitlines():
    training_rows.append(line.split())


# open item data file (specifies the genres of each movie)
item_file = open("data/u-item.item", "r")

# store each row in a list
item_reader = csv.reader(item_file, delimiter='|')
item_rows = list(item_reader)

# ask user for the person number & movie number they would like to use to predict the rating
person = input("Please input the number of the person you are interested in: ")
movie = input("Please input the number of the movie you are interested in: ")

