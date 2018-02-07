import csv
import math
import time


# take original data and convert decimals to categorical data
# divide into 9 bins of the same amount of exampls
# output new 'rows' and 'columns' lists with decimals replaced with strings
def convert_to_categorical_data(rows, columns):

    # CONVERT ROW DATA
    index = 0
    for c in columns:

        index += 1

        # for columns with data of floats, convert to categorical data
        if index <= 9 and index >= 5:

            # SORT
            rows = sorted(rows, key=lambda x:x[index-1])

            # convert float to string based on index
            iteration = 0
            for row in rows:
                iteration += 1
                for i in range(len(row)):
                    if i == index - 1:
                        if iteration <= 1000:
                            row[i] = 'bin1'
                        elif iteration <= 2000:
                            row[i] = 'bin2'
                        elif iteration <= 3000:
                            row[i] = 'bin3'
                        elif iteration <= 4000:
                            row[i] = 'bin4'
                        elif iteration <= 5000:
                            row[i] = 'bin5'
                        elif iteration <= 6000:
                            row[i] = 'bin6'
                        elif iteration <= 7000:
                            row[i] = 'bin7'
                        elif iteration <= 8000:
                            row[i] = 'bin8'
                        elif iteration <= 9000:
                            row[i] = 'bin9'

    # CONVERT COLUMN DATA
    cols = []
    for n in range(len(rows[0])):
        attribute = []
        for r in rows:
            attribute.append(r[n])
        cols.append(attribute)

    return rows, cols


# calculate times each class appears and output list of counts
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


# calculate entropy of class column (Critic_Score)
def class_entropy(columns):

    counts = class_counter(columns[11])
    total = len(columns[11])

    entropy = 0

    for n in range(len(counts)):
        if counts[n] != 0:
            entropy += -1 * (counts[n] / total) * (math.log(counts[n] / total) / math.log(2))

    return entropy


# calculate entropy of given attribute (specified by column number of attribute)
def attribute_entropy(rows, columns, col_num):

    unique_attributes = list(set(columns[col_num]))

    classes = []
    all_counts = []

    # for each unique attribute in specified column, creates array of count for each class label
    for i in range(len(unique_attributes)):
        classes = []
        for r in rows:
            if r[col_num] == unique_attributes[i]:
                classes.append(r[11])
        c = class_counter(classes)
        all_counts.append(c)

    # calculate total (should add up to 8134 in this case)
    total = 0
    for x in range(len(all_counts)):
        for y in range(len(all_counts[x])):
            total += all_counts[x][y]

    probability = 0
    entropy = 0

    # iterate through each attribute's class labels in order to calculate entropy
    for m in range(len(all_counts)):
        subtotal = 0

        for n in range(len(all_counts[m])):
            subtotal += all_counts[m][n]

        probability = subtotal / total
        for p in range(len(all_counts[m])):
            entropy -= (all_counts[m][p] / subtotal) * (math.log(all_counts[m][p] / subtotal) / (math.log(2)))
        entropy = probability * entropy

    return entropy


# calculate information gain
def information_gain(rows, columns, col_num):
    class_e = class_entropy(columns)
    attribute_e = attribute_entropy(rows, columns, col_num)
    return class_e - attribute_e


# return class with highest probability (to be used when no attributes left)
def highest_probability(columns):

    return max(columns[11],key=columns[i].count)

depth = 0
tree = []
# create id3 algorithm to make a decision tree
def id3_algorithm(rows, columns, attributes_count):

    # input("continue...")

    # return if all class labels are the same
    classes = []
    for r in rows:
        classes.append(r[11])
        print(r)

    if len(class_counter(classes)) < 2:
        print('dats it bois')
        return

    if attributes_count == 0:
        return highest_probability(columns)

    # will store information gain of column 0 in index 0, and so on
    info_gain = []

    # find information gain of each column (A, B)
    for i in range(11):
        gain = information_gain(rows, columns, i)
        info_gain.append(gain)

    # find number of column with largest information gain
    highest_info_gain = info_gain.index(max(info_gain))
    print(highest_info_gain)

    bins = list(set(columns[highest_info_gain]))
    print('bins: ', bins)

    # call function recursively for each bin
    for k in range(len(bins)):

        new_rows = []
        new_cols = []

        it = 0
        for r in rows:
            it += 1
            if r[highest_info_gain] == bins[k]:
                new_rows.append(r)

        for i in range(12):
            cols = []
            for row in new_rows:
                cols.append(row[i])
            new_cols.append(cols)

        id3_algorithm(new_rows, new_cols, attributes_count - 1)

# -------------------------------- MAIN -------------------------------- #


file_name = 'Video_Games_Sales.csv'
file = open(file_name)

# eliminates and stores first row from data (attribute titles)
first = file.readline()

# store each row of data in 'rows' list (each row is stored in an index of 'rows')
reader = csv.reader(file, delimiter=',')
all_rows = list(reader)

rows = []
x = 0

for row in all_rows:
    empty_count = 0
    for i in range(len(row)):
        if row[i] == '':
            empty_count += 1
    if empty_count == 0:
        rows.append(row)

num_rows = len(rows)
num_cols = len(rows[0])

# store each column of data in 'columns' list (each column is stored in an index or 'columns')
columns = []

for i in range(num_cols):
    attribute = []
    for row in rows:
        attribute.append(row[i])
    columns.append(attribute)

start = time.time()

categorical_rows, categorical_columns = convert_to_categorical_data(rows, columns)
class_entropy(categorical_columns)
attribute_entropy(categorical_rows, categorical_columns, 0)
print(information_gain(categorical_rows, categorical_columns, 0))
id3_algorithm(categorical_rows, categorical_columns, 11)

print("Runtime is: ", time.time() - start)
