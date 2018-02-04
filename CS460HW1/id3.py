import csv
import math

# ~~~~~~~~ FUNCTIONS ~~~~~~~~~ #


def class_counter(col):

    count = []

    # prints each class
    classes = list(set(col))

    # prints number of times each class occurs
    for x in classes:
        counter = 0
        for y in col:
            if x == y:
                counter = counter + 1
        count.append(counter)

    # returns list of number of class occurrences
    return count


# given column of data and number of bins
# discretize data and calculate entropy
# return entropy value
def class_entropy(col, num_rows, bins):

    entropy = 0

    # prints number of times each class occurs
    count = class_counter(col)

    # calculate entropy
    for n in (0, bins - 1):
        entropy += -1 * (count[n] / num_rows) * ((math.log(count[n] / num_rows)) / math.log(2))
    return entropy


# calculate entropy of attribute
def attribute_entropy(col, boundary, col_num, num_rows, dataset, string_name):

    # convert list of strings to list of floats
    col = list(map(float, col))

    # create list of data in bins
    bin1 = []
    bin2 = []

    # split data into bins (discretize via equidistant bins)
    for row in dataset:

        # print(row[col_num])
        data_entry = float(row[col_num])

        # replace floats with strings for easier search
        # add data to bins
        if data_entry <= boundary:
            #bin1.append(data_entry)
            bin1.append(row)
            row[col_num] = string_name + '1'
        else:
            #bin2.append(data_entry)
            bin2.append(row)
            row[col_num] = string_name + '2'

    # bins = [[b1no, b1yes], [b2no, b2yes]]
    bins = [[0, 0], [0, 0]]

    # store class count for each bin
    for row in dataset:

        if row[col_num] == string_name + '1':
            if row[2] == '0':
                bins[0][0] += 1
            else:
                bins[0][1] += 1
        else:
            if row[2] == '0':
                bins[1][0] += 1
            else:
                bins[1][1] += 1

    # print(bins)
    final = 0

    # calculate entropy
    for i in range(2):

        entropy = 0
        total = 0

        for j in range(2):
            total += bins[i][j]

        probability = total / num_rows

        for k in range(2):
            if bins[i][k] != 0:
                entropy += -1 * (bins[i][k] / total) * ((math.log(bins[i][k] / total)) / math.log(2))

        entropy = probability * entropy
        final += entropy

    # store all data associated with bins

    # print(dataset)
    return dataset, final, bin1, bin2

# calculate information gain
def information_gain(class_entropy, attribute_entropy):
    return class_entropy - attribute_entropy

# ID3 algorithm
# examples --> set of data with specific attribute {depends}
# target --> target values {column c}
# attributes --> all attributes not used currently {a, b}
# boundary_ values --> list of boundary used on column1 and column2
def id3_algorithm(examples, target, attributes, boundary, all_data):

    print(examples)

    # calculate entropy for class
    class_e = class_entropy(examples[2], len(examples[0]), 2)

    attribute_e = []  # will store values of all entropy's of all attributes (index 0, corresponds with column 0)
    info_gain = []
    bins = []

    # calculate entropy and information gain of each column/bin
    for i in range(2):

        temp_bin = []

        if i == 0: bin_string = 'x'
        else: bin_string = 'y'

        new_data, entropy, b1, b2 = attribute_entropy(examples[i], boundary[i], i, len(examples[0]), all_data, bin_string)
        gain = information_gain(class_e, entropy)

        attribute_e.append(entropy)
        info_gain.append(gain)

        #temp_bin.append(b1)
        #temp_bin.append(b2)
        #bins.append(temp_bin)

        bins.append(b1)
        bins.append(b2)

    print(attribute_e)
    print(info_gain)
    print(bins[0])
    print(bins[1])

    # find which attribute to use based on highest information gain
    attribute_to_split = attribute_e.index(max(attribute_e))

    # split into bins
    #for i in range(len(bins[attribute_to_split])):
        #id3_algorithm(bins[attribute_to_split], 1, 1, boundary, all_data)


# ~~~~~~~~~~ MAIN ~~~~~~~~~~ #
columns = []
attribute = []

# read in .csv file
file_name = 'synthetic-1.csv'
file = open(file_name)

reader = csv.reader(file, delimiter=',')
data = list(reader)
# print(data)
num_rows = len(data)
num_cols = 3  # figure out how to determine number of cols

# store each column of data in 'columns' list (each column is stored in an index)
for i in range(0, num_cols):
    attribute = []
    for row in data:
        attribute.append(row[i])
    columns.append(attribute)

# # calculate entropy for class
# class_e = class_entropy(columns[num_cols - 1], num_rows, 2)
# print(class_e)

# create boundaries to discretize from - DONE MANUALLY (change for each .csv file)
boundary1 = 0
boundary2 = 0
boundaries = []
if file_name == 'synthetic-1.csv':
    boundary1 = 4.6121
    boundary2 = 2.91305
    boundaries.append(boundary1)
    boundaries.append(boundary2)
elif file_name == 'synthetic-2.csv':
    boundary1 = 0.0878
    boundary2 = 2.61845
    boundaries.append(boundary1)
    boundaries.append(boundary2)
elif file_name == 'synthetic-3.csv':
    boundary1 = 1.96091
    boundary2 = 0.6424
    boundaries.append(boundary1)
    boundaries.append(boundary2)
elif file_name == 'synthetic-4.csv':
    boundary1 = 4.05485
    boundary2 = 0.6385
    boundaries.append(boundary1)
    boundaries.append(boundary2)

# print(data)
id3_algorithm(columns, 1, 1, boundaries, data)

# # calculate entropy and information gain for first column
# new_data, attribute_e1 = attribute_entropy(columns[0], boundary1, 0, num_rows, data, 'x')
# info_gain1 = information_gain(class_e, attribute_e1)
# print(attribute_e1)
# print(info_gain1)
#
# # calculate entropy and information gain for second column
# new_data, attribute_e2 = attribute_entropy(columns[1], boundary2, 1, num_rows, data, 'y')
# info_gain2 = information_gain(class_e, attribute_e2)
# print(attribute_e2)
# print(info_gain2)
