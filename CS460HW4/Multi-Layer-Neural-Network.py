from tqdm import tqdm
import numpy as np
import math
import sys


# create one hot lists for each file
# puts 1 in index of digit that is being trained on, 0 for the rest
def one_hot_lists(name):

    one_hot = []

    if name == "data/mnist_train_0_1.csv":
        one_hot.append([1, 0])
        one_hot.append([0, 1])
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

    # for each node
    for i in range(len(nodes)):

        # use sigmoid activation function - if overflow, assign 0
        try:
            sig = 1 / (1 + math.exp(-1 * nodes[i]))
        except:
            sig = 0

        # add or subtract epsilon to avoid exact 0 or 1
        if sig == 0:
            sig = 0 + epsilon
        if sig == 1:
            sig = 1 - epsilon

        activations.append(sig)

    return activations


# prints out error of each epoch in a nice format
def print_errors(errors):

    for i in range(len(errors)):
        print("Epoch {}: {}% accuracy.".format(i+1, errors[i]*100))


# trains feed forward with back propagation
def training(input_weights, hidden_weights, data, alpha, bias, epsilon, one_hot_list):

    # for each example
    for row in tqdm(data):

        # add bias to example
        row = np.insert(row, len(row), 1)

        # 2. given an example, run the network
        input_layer = row[1:]
        one_hot = one_hot_list[int(row[0])]

        # find the activation values for each node in hidden layer (keep last entry as 1 for bias)
        hidden_layer = np.dot(np.transpose(input_weights), input_layer)
        hidden_activations = np.array(sigmoid(hidden_layer, epsilon))
        hidden_activations[-1] = bias

        # find the activation values for each node in output layer
        output_layer = (np.dot(np.transpose(hidden_weights), hidden_activations))
        output_activations = np.array(sigmoid(output_layer, epsilon))

        # 3. propagate backwards
        # for each node j in output layer, calculate delta j
        updated_output_nodes = []
        for j in range(len(output_layer)):
            updated_output_nodes.append(
                output_activations[j] * (1 - output_activations[j]) * (one_hot[j] - output_activations[j]))

        # for each node i in hidden layer, calculate delta i
        updated_hidden_nodes = []
        for i in range(len(hidden_layer)):
            summation = (hidden_weights[i][0] * updated_output_nodes[0]) + (
                        hidden_weights[i][1] * updated_output_nodes[1])
            updated_hidden_nodes.append(hidden_activations[i] * (1 - hidden_activations[i]) * summation)

        # update hidden layer weights
        for m in range(len(hidden_weights)):
            for n in range(len(hidden_weights[m])):
                hidden_weights[m][n] = hidden_weights[m][n] + (alpha * hidden_activations[m] * updated_output_nodes[n])

        # update input layer weights
        for r in range(len(input_weights)):
            for s in range(len(input_weights[r])):
                input_weights[r][s] = input_weights[r][s] + (alpha * input_layer[r] * updated_hidden_nodes[s])

    return input_weights, hidden_weights


# tests each row in given dataset and outputs error
def testing(input_weights, hidden_weights, testing_data, alpha, bias, epsilon):

    correct = 0

    for row in testing_data:

        # add bias to each image entry
        row = np.insert(row, len(row), 1)

        # 2. given an example, run the network
        input_layer = row[1:]

        # find the activations of each node in hidden layer
        hidden_layer = np.dot(np.transpose(input_weights), input_layer)
        hidden_activations = np.array(sigmoid(hidden_layer, epsilon))
        hidden_activations[-1] = bias

        # find activations of each node in output layer
        output_layer = (np.dot(np.transpose(hidden_weights), hidden_activations))
        output_activations = np.array(sigmoid(output_layer, epsilon))

        # find actual and guess values
        actual = int(row[0])
        guess = np.argmax(output_activations)

        # compare and store if correct
        if int(actual) == int(guess):
            correct += 1

    # calculate and return error
    error = correct / len(testing_data)
    return error


# create a neural network with feed forward method
# use back-propagation to train neural network
# test network
def neural_network(data, testing_data, one_hot_list, num_output_nodes):

    bias = 1
    alpha = 0.001
    epsilon = 0.0001
    hidden_layer_nodes = 6

    print("Alpha =", alpha)
    print("Hidden Nodes =", hidden_layer_nodes)

    # 1. initialize weights in network to small random numbers (include 1 as bias)
    input_weights = np.random.uniform(low=-1, high=1, size=(784+1, hidden_layer_nodes+1))
    hidden_weights = np.random.uniform(low=-1, high=1, size=(hidden_layer_nodes+1, num_output_nodes))

    errors = []

    # run 8 epochs
    for epoch in range(8):

        # TRAINING
        input_weights, hidden_weights = training(input_weights, hidden_weights, data, alpha, bias, epsilon, one_hot_list)

        # TESTING
        error = testing(input_weights, hidden_weights, testing_data, alpha, bias, epsilon)
        errors.append(error)

    print_errors(errors)


def main():

    # ask for user input regarding which MNIST set they would like to use
    choice = input("Enter Choice:\n1. MNIST for values 0-1\n2. MNIST for values 0-4\n")
    print("Loading...")

    # base training and testing file off user input
    if int(choice) == 1:
        filename = "data/mnist_train_0_1.csv"
        testing_file = "data/mnist_test_0_1.csv"
        num_outputs = 2
    elif int(choice) == 2:
        filename = "data/mnist_train_0_4.csv"
        testing_file = "data/mnist_test_0_4.csv"
        num_outputs = 5
    else:
        print("Invalid choice. Goodbye!")
        sys.exit()

    # read in training and testing data
    training_data = np.loadtxt(filename, delimiter=',')
    testing_data = np.loadtxt(testing_file, delimiter=',')

    # find one hot list according to training file selected
    one_hot = one_hot_lists(filename)

    # train and test neural net
    neural_network(training_data, testing_data, one_hot, num_outputs)

main()
