import numpy as np
import math


# find activation value of each node in given layer
def sigmoid(nodes):

    activations = []
    for i in range(len(nodes)):
        try:
            sig = 1 / (1 + math.exp(-1 * nodes[i]))
        except:
            sig = 0
        activations.append(sig)

    return activations


def feed_forward_training(data):

    alpha = 0.05
    hidden_layer_nodes = 10

    # 1. initialize weights in network to small random numbers
    input_weights = np.random.uniform(low=0, high=1, size=(hidden_layer_nodes,784))
    hidden_weights = np.random.uniform(low=0, high=1, size=(2,hidden_layer_nodes))

    for row in data:

        # 2. given an example, run the network
        input_layer = row[1:]

        hidden_layer = np.dot(input_weights, input_layer)
        hidden_activations = np.array(sigmoid(hidden_layer))

        output_layer = (np.dot(hidden_weights, hidden_activations))
        output_activations = np.array(sigmoid(output_layer))

        # 3. propagate backwards
        # for each node j in output layer
        updated_output_nodes = []
        for j in range(len(output_layer)):
            updated_output_nodes.append(output_activations[j] * (1 - output_activations[j]) * (j - output_activations[j]))

        # for each node i in hidden layer
        updated_hidden_nodes = []
        for i in range(len(hidden_layer)):

            summation = np.sum(np.transpose(hidden_weights)[i] * updated_output_nodes)
            updated_hidden_nodes.append(hidden_activations[i] * (1 - hidden_activations[i]) * summation)


        print(output_activations)
        print(updated_hidden_nodes)

        # update hidden layer weights
        print(hidden_weights)
        for m in range(len(hidden_weights)):
            for n in range(len(hidden_weights[m])):
                hidden_weights[m][n] = hidden_weights[m][n] + (alpha * output_activations[m] * updated_hidden_nodes[m])
        print(hidden_weights)

        # update input layer weights
        input("next")

def main():

    print("Loading...")
    filename = "data/mnist_train_0_1.csv"
    data = np.loadtxt(filename, delimiter=',')

    feed_forward_training(data)


main()
