import numpy as np
from tqdm import tqdm
import math


def one_hot_lists(name):
    one_hot = []
    if name == "data/mnist_train_0_1.csv":
        one_hot.append([1, 0])
        one_hot.append([0,1])
    elif name == "data/mnist_train_0_4.csv":
        one_hot.append([1, 0, 0, 0, 0])
        one_hot.append([0, 1, 0, 0, 0])
        one_hot.append([0, 0, 1, 0, 0])
        one_hot.append([0, 0, 0, 1, 0])
        one_hot.append([0, 0, 0, 0, 1])
    return one_hot


# find activation value of each node in given layer
def sigmoid(nodes, epsilon):

    activations = []
    for i in range(len(nodes)):
        try:
            sig = 1 / (1 + math.exp(-1 * nodes[i]))
        except:
            sig = 0

        if sig == 0:
            sig = 0 + epsilon
        if sig == 1:
            sig = 1 - epsilon

        activations.append(sig)

    return activations


def feed_forward_training(data, testing_data, one_hot_list):

    alpha = 0.005
    epsilon = 0.0001
    hidden_layer_nodes = 8
    epoch = 0

    # 1. initialize weights in network to small random numbers
    input_weights = np.random.uniform(low=-1, high=1, size=(784, hidden_layer_nodes))
    hidden_weights = np.random.uniform(low=-1, high=1, size=(hidden_layer_nodes, 2))

    while epoch < 5:
        for row in tqdm(data):

            # 2. given an example, run the network
            input_layer = row[1:]
            one_hot = one_hot_list[int(row[0])]

            hidden_layer = np.dot(np.transpose(input_weights), input_layer)
            hidden_activations = np.array(sigmoid(hidden_layer, epsilon))

            output_layer = (np.dot(np.transpose(hidden_weights), hidden_activations))
            output_activations = np.array(sigmoid(output_layer, epsilon))

            # 3. propagate backwards
            # for each node j in output layer
            updated_output_nodes = []
            for j in range(len(output_layer)):
                updated_output_nodes.append(output_activations[j] * (1 - output_activations[j]) * (one_hot[j] - output_activations[j]))

            # for each node i in hidden layer
            updated_hidden_nodes = []
            for i in range(len(hidden_layer)):
                summation = (hidden_weights[i][0] * updated_output_nodes[0]) + (hidden_weights[i][1] * updated_output_nodes[1])
                updated_hidden_nodes.append(hidden_activations[i] * (1 - hidden_activations[i]) * summation)

            # update hidden layer weights
            for m in range(len(hidden_weights)):
                for n in range(len(hidden_weights[m])):
                    hidden_weights[m][n] = hidden_weights[m][n] + (alpha * hidden_activations[m] * updated_output_nodes[n])

            # update input layer weights
            for r in range(len(input_weights)):
                for s in range(len(input_weights[r])):
                    input_weights[r][s] = input_weights[r][s] + (alpha * input_layer[r] * updated_hidden_nodes[s])


        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  TESTING  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        correct = 0
        for row in testing_data:

            # 2. given an example, run the network
            input_layer = row[1:]

            hidden_layer = np.dot(np.transpose(input_weights), input_layer)
            hidden_activations = np.array(sigmoid(hidden_layer, epsilon))
            # print("hidden activations", hidden_activations)

            output_layer = (np.dot(np.transpose(hidden_weights), hidden_activations))
            output_activations = np.array(sigmoid(output_layer, epsilon))
            # print("output activations", output_activations)

            actual = int(row[0])
            guess = np.argmax(output_activations)

            if int(actual) == int(guess):
                correct += 1

        error = correct / len(testing_data)
        tqdm.write("\nPercent Error:")
        print(error)
        epoch += 1


def main():

    print("Loading...")
    filename = "data/mnist_train_0_1.csv"
    training_data = np.loadtxt(filename, delimiter=',')

    if filename == "data/mnist_train_0_1.csv":
        testing_file = "data/mnist_test_0_1.csv"
    elif filename == "data/mnist_train_0_4.csv":
        testing_file = "data/mnist_test_0_4.csv"

    testing_data = np.loadtxt(testing_file, delimiter=',')

    one_hot = one_hot_lists(filename)
    feed_forward_training(training_data, testing_data, one_hot)

main()
