# input = X = column 1
# actual output = Y = column 2

import csv


def gradient_descent(data, polynomial):

    cost = 0

    # set alpha
    learning_rate = 0.00001

    # initialize all thetas to zero (guess zero as initial value)
    intercept = 0  # theta sub zero
    slopes = [0] * polynomial  # theta sub 1 - polynomial

    for n in range(10000):

        # for each point in the data set
        for point in data:

            # store x and y coordinates
            x = float(point[0])
            y = float(point[1])

            # make a prediction of y
            prediction = intercept
            for i in range(len(slopes)):
                prediction += slopes[i] * (x ** (i + 1))

            error = prediction - y
            # print("error: ", error)

            # adjust theta values
            intercept = intercept - (learning_rate * error)
            for j in range(len(slopes)):
                slopes[j] = slopes[j] - (learning_rate * error * (x ** (j + 1)))

            # calculate cost
            prediction = intercept
            for k in range(len(slopes)):
                prediction += slopes[k] * (x ** (k + 1))

            error = prediction - y
            cost = error ** 2

    cost = cost / (len(data))
    print(intercept)
    print(slopes)
    print(cost)



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
    print('========================')
    gradient_descent(rows, 2)
    print('========================')
    gradient_descent(rows,4)
    print('========================')
    gradient_descent(rows, 9)
    print('========================')

main()