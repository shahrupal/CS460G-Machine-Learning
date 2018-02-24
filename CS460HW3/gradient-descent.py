# input = X = column 1
# actual output = Y = column 2

import csv


def gradient_descent(data, polynomial):

    # set alpha to 1/10
    learning_rate = 0.10

    # initialize all thetas to zero (guess zero as initial value)
    intercept = 0  # theta sub zero
    slopes = [0] * polynomial  # theta sub 1 - polynomial

    # for each point in the data set
    for point in data:

        # store x and y coordinates
        x = float(point[0])
        y = float(point[1])

        # make prediction for y value
        # prediction = x *

        # iterate through slope thetas (all thetas but theta sub zero - intercept)
        for i in range(len(slopes)):
            print(i)



def main():

    # request user to input file
    print("\nPlease select one of the following choices. \n1) synthetic-1.csv \n2) synthetic-2.csv \n3) synthetic-3.csv \n")
    file_name = input("Option: ")

    # open selected file
    file = open("data/synthetic-"+file_name+".csv", "r")

    # store each row in a list
    read = csv.reader(file, delimiter=',')
    rows = list(read)

    # call gradient descent on first-order polynomial
    gradient_descent(rows, 1)

main()