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


def attribute_entropy(col, col_num, num_rows, bins, dataset):

    # convert list of strings to list of floats
    col = list(map(float, col))

    # find min and max values
    minimum = min(col)
    maximum = max(col)

    # divide range by 5 bins
    r = maximum - minimum
    div = r / 5

    # create ranges for each bin
    max1 = minimum + (div * 1)
    max2 = minimum + (div * 2)
    max3 = minimum + (div * 3)
    max4 = minimum + (div * 4)

    # split data into bins (discretize via equidistant bins)
    for row in dataset:

        first_entry = float(row[col_num])

        # replace floats with strings for easier search
        if (first_entry >= minimum) & (first_entry < max1):
            row[col_num] = 'bin1'
        elif (first_entry >= max1) & (first_entry < max2):
            row[col_num] = 'bin2'
        elif (first_entry >= max2) & (first_entry < max3):
            row[col_num] = 'bin3'
        elif (first_entry >= max3) & (first_entry < max4):
            row[col_num] = 'bin4'
        else:
            row[col_num] = 'bin5'

    # [[b1no, b1yes], [b2no, b2yes], ...]
    bins = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    # store class count for each bin
    for row in dataset:
        if row[col_num] == 'bin1':
            if row[2] == '0': bins[0][0] += 1
            else: bins[0][1] += 1
        elif row[col_num] == 'bin2':
            if row[2] == '0': bins[1][0] += 1
            else: bins[1][1] += 1
        elif row[col_num] == 'bin3':
            if row[2] == '0': bins[2][0] += 1
            else: bins[2][1] += 1
        elif row[col_num] == 'bin4':
            if row[2] == '0': bins[3][0] += 1
            else: bins[3][1] += 1
        elif row[col_num] == 'bin5':
            if row[2] == '0': bins[4][0] += 1
            else: bins[4][1] += 1

    final = 0

    # calculate entropy
    for i in range(4):

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

    print(dataset)
    return final


# ~~~~~~~~~~ MAIN ~~~~~~~~~~ #
columns = []
attribute = []

# read in .csv file
file = open('synthetic-2.csv')

reader = csv.reader(file, delimiter=',')
data = list(reader)
print(data)
num_rows = len(data)
num_cols = 3  # figure out how to determine number of cols

# store each column of data in 'columns' list (each column is stored in an index)
for i in range(0, num_cols):
    attribute = []
    for row in data:
        attribute.append(row[i])
    columns.append(attribute)

# calculate entropy for class
class_e = class_entropy(columns[num_cols - 1], num_rows, 2)
print(class_e)

# calculate entropy for attributes
attribute_e1 = attribute_entropy(columns[0], 0, num_rows, 5, data)
print(attribute_e1)

