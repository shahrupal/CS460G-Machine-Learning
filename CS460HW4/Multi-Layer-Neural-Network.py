import numpy as np
import math


# find activation value of each node in given layer
def sigmoid(nodes):

    activations = []
    for i in range(len(nodes)):
        sig = 1 / (1 + math.exp(-1 * nodes[i]))
        activations.append(sig)

    return activations


def feed_forward_training(data):

    hidden_layer_nodes = 10

    # create random weights for each line between input nodes and hidden layer nodes
    input_weights = np.random.uniform(low=0, high=0.01, size=(hidden_layer_nodes,784))

    # create random weights for each line between hidden layer nodes and output nodes
    hidden_weights = np.random.uniform(low=0, high=0.01, size=(2,hidden_layer_nodes))

    # train on each row
    for row in data:

        input_layer = row[1:]
        
        hidden_layer = np.dot(input_weights, input_layer)
        hidden_activations = np.array(sigmoid(hidden_layer))

        output_layer = (np.dot(hidden_weights, hidden_activations))
        output_activations = np.array(sigmoid(output_layer))

        print(hidden_activations)
        print(output_activations)
        input("next")


def main():

    print("Loading...")
    filename = "data/mnist_train_0_1.csv"
    data = np.loadtxt(filename, delimiter=',')

    feed_forward_training(data)

main()
