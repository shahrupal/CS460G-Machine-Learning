# input = X = column 1
# actual output = Y = column 2

import csv
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patch

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
    return intercept, slopes


# output plot of regression line and original data
# i1 = intercept value of 1st polynomial
# s1 = slope values of 1st polynomial
def create_graph(i1, s1, i2, s2, i4, s4, i9, s9, rows, file_name):

    x = numpy.arange(-2.5, 2.5, step=0.01)

    y1 = i1
    for i in range(len(s1)):
        y1 += s1[i] * (x ** (i + 1))

    y2 = i2
    for i in range(len(s2)):
        y2 += s2[i] * (x ** (i + 1))

    y4 = i4
    for i in range(len(s4)):
        y4 += s4[i] * (x ** (i + 1))

    y9 = i9
    for i in range(len(s9)):
        y9 += s9[i] * (x ** (i + 1))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.tick_params(axis='x', pad=15)

    # change y-axis for each file to include all data points
    if file_name == "synthetic-1.csv":
        ax.set_ylim(-2, 12)
    elif file_name == "synthetic-2.csv":
        ax.set_ylim(-20, 15)
    elif file_name == "synthetic-3.csv":
        ax.set_ylim(-2, 2)

    # graph scatter plot
    for i in range(len(rows)):
        ax.scatter(float(rows[i][0]), float(rows[i][1]), color="#2484f2")

    # plot polynomial equations on graph
    ax.plot(x, y1, color="#f16823")
    ax.plot(x, y2, color="#9822e8")
    ax.plot(x, y4, color="#e82222")
    ax.plot(x, y9, color="#2ab50a")

    # create legend
    orange_key = patch.Patch(color='#f16823', label='1st Order')
    purple_key = patch.Patch(color='#9822e8', label='2nd Order')
    red_key = patch.Patch(color='#e82222', label='4th Order')
    green_key = patch.Patch(color='#2ab50a', label='9th Order')
    plt.legend(handles=[orange_key, purple_key, red_key, green_key])

    # set title and axes labels
    fig.suptitle(file_name, fontsize=20)

    plt.show()


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
    intercept1, slopes1 = gradient_descent(rows, 1)
    print('========================')
    intercept2, slopes2 = gradient_descent(rows, 2)
    print('========================')
    intercept4, slopes4 = gradient_descent(rows,4)
    print('========================')
    intercept9, slopes9 = gradient_descent(rows, 9)
    print('========================')

    create_graph(intercept1, slopes1, intercept2, slopes2, intercept4, slopes4, intercept9, slopes9, rows, "synthetic-"+file_name+".csv")

main()