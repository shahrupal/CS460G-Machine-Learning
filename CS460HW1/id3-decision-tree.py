import csv
import math

# ---------------------------------------------------- Functions ---------------------------------------------------- #


# input --> synthetic csv file
# outputs an array --> index 0 = boundary for A column; index 1 = boundary for B column
def find_boundary(file_name):

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

    return boundaries


# take original data and convert decimals to categorical data
# first column --> if below boundary, convert to x1; if above boundary, convert to x2
# second column --> below, y1; above, y2
# output new 'rows' and 'columns' lists with decimals replaced with strings
def convert_to_categorical_data(rows, columns, file_name):

    boundaries = find_boundary(file_name)

    # CONVERT ROW DATA
    for row in rows:

        # create categorical data for column A
        if float(row[0]) <= boundaries[0]:
            row[0] = 'x1'
        else:
            row[0] = 'x2'

        # create categorical data for column B
        if float(row[1]) <= boundaries[1]:
            row[1] = 'y1'
        else:
            row[1] = 'y2'

    # CONVERT COLUMN DATA
    # create categorical data for column A
    for j in range(len(columns[0])):
        if float(columns[0][j]) <= boundaries[0]:
            columns[0][j] = 'x1'
        else:
            columns[0][j] = 'x2'

    # create categorical data for column B
    for k in range(len(columns[1])):
        if float(columns[1][k]) <= boundaries[1]:
            columns[1][k] = 'y1'
        else:
            columns[1][k] = 'y2'

    return rows, columns


# calculate entropy of class column (column C)
def class_entropy(columns):

    count0 = 0
    count1 = 0
    counts = []
    total = 0
    entropy = 0

    # count number of 0's and 1's in class column
    for i in range(len(columns[2])):
        total += 1
        if float(columns[2][i]) == 0:
            count0 += 1
        else:
            count1 += 1
    counts.append(count0)
    counts.append(count1)

    for n in range(len(counts)):
        entropy -= (counts[n] / total) * (math.log(counts[n] / total) / math.log(2))

    return entropy


# calculate entropy of each attribute column (columns A and B)
def attribute_entropy(rows, columns, column_num):

    final = 0

    if column_num == 0:
        bin_name = 'x'
    elif column_num == 1:
        bin_name = 'y'

    # bins = [[b1no, b1yes], [b2no, b2yes]]
    bins = [[0, 0], [0, 0]]

    # store class count for each bin
    for row in rows:

        if row[column_num] == bin_name + '1':
            if row[2] == '0':
                bins[0][0] += 1
            else:
                bins[0][1] += 1
        else:
            if row[2] == '0':
                bins[1][0] += 1
            else:
                bins[1][1] += 1

    print(bins)

    # calculate entropy
    for i in range(2):

        entropy = 0
        total = 0

        for j in range(2):
            total += bins[i][j]

        probability = total / len(rows)

        for k in range(2):
            if bins[i][k] != 0:
                entropy += -1 * (bins[i][k] / total) * ((math.log(bins[i][k] / total)) / math.log(2))

        entropy = probability * entropy
        final += entropy

    print(final)

# ---------------------------------------------------- Main ---------------------------------------------------- #


# read in .csv file
file_name = 'synthetic-1.csv'
file = open(file_name)

# store each row of data in 'rows' list (each row is stored in an index of 'rows')
reader = csv.reader(file, delimiter=',')
rows = list(reader)

num_rows = len(rows)
num_cols = 3

# store each column of data in 'columns' list (each column is stored in an index or 'columns')
columns = []
for i in range(num_cols):
    attribute = []
    for row in rows:
        attribute.append(row[i])
    columns.append(attribute)

categorical_rows, categorical_columns = convert_to_categorical_data(rows, columns, file_name)
class_entropy(categorical_columns)
attribute_entropy(categorical_rows, categorical_columns, 0)

