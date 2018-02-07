import csv
import numpy as np
# take original data and convert decimals to categorical data
# divide into 10 equidistant bins
# output new 'rows' and 'columns' lists with decimals replaced with strings
def convert_to_categorical_data(rows, columns):

    # CONVERT ROW DATA

    index = 0
    for c in columns:

        index += 1

        if c[0] == 'NA_Sales' or c[0] == 'EU_Sales' or c[0] == 'JP_Sales' or c[0] == 'Other_Sales' or c[0] == 'Global_Sales':

            # SORT

            iteration = 0
            for r in rows:
                for i in range(len(r)):
                    if i == index:
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
                            
                # print(r[index - 1])

    # CONVERT COLUMN DATA

    return rows, columns

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

print(columns)

convert_to_categorical_data(rows, columns)
