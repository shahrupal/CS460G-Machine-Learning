# input = X = column 1
# actual output = Y = column 2

import csv


def gradient_descent(data, polynomial):

    cost = 0
    intercept_sum = 0
    slopes_sums = [0] * polynomial

    # set alpha to 1/10
    learning_rate = 0.10

    # initialize all thetas to zero (guess zero as initial value)
    intercept = 0  # theta sub zero
    slopes = [0] * polynomial  # theta sub 1 - polynomial

    for n in range(1000):

        # for each point in the data set
        for point in data:

            # store x and y coordinates
            x = float(point[0])
            y = float(point[1])

            # sum error of each data point for theta sub zero (y-intercept)
            hypothesis = intercept
            for i in range(len(slopes)):
                hypothesis += slopes[i] * (x ** (i + 1))

            error = hypothesis - y
            intercept_sum += error
            cost += error ** 2

            # sum error of each data point for theta sub one to polynomial (slopes)
            for j in range(len(slopes)):  # for each theta

                hypothesis = intercept
                for k in range(len(slopes)):
                    hypothesis += slopes[j] * (x ** (k + 1))

                error = hypothesis - y
                slopes_sums[j] += (error * x)
                cost += error ** 2

        # adjust theta values
        intercept = intercept - (learning_rate * (1 / len(data)) * intercept_sum)
        print("intercept: ", intercept)
        for m in range(len(slopes)):
            slopes[m] = slopes[m] - (learning_rate * (1 / len(data)) * slopes_sums[m])
            print("slope", m, ": ",slopes[m])

        cost = (1 / len(data)) * cost
        print(cost)
        print("You are on interation: ", n)
        input("next")

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