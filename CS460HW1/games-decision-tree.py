import csv
import math


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

    classes = list(set(columns[col_num]))
    print(classes)



# -------------------------------- MAIN -------------------------------- #
file_name = 'Video_Games_Sales.csv'
file = open(file_name)

# store each row of data in 'rows' list (each row is stored in an index of 'rows')
reader = csv.reader(file, delimiter=',')
rows = list(reader)

num_rows = len(rows)
num_cols = len(rows[0])

# store each column of data in 'columns' list (each column is stored in an index or 'columns')
columns = []
for i in range(num_cols):
    attribute = []
    for row in rows:
        attribute.append(row[i])
    columns.append(attribute)

categorical_rows, categorical_columns = convert_to_categorical_data(rows, columns)
class_entropy(categorical_columns)
attribute_entropy(categorical_rows, categorical_columns, 6)