import math


# output dictionary, which includes:
# each unique token as key
# and the number of occurrences as well as the probability (utilizes log) of each token as values
def count_tokens(tokens):

    token_dictionary = {}

    for i in range(len(tokens)):

        if tokens[i] not in token_dictionary:
            token_count = tokens.count(tokens[i])
            token_probability = math.log(token_count / len(tokens))
            token_dictionary[tokens[i]] = [token_count, token_probability]

    return token_dictionary


# pass index of probability that should be highest
# 0-hamlet, 1-juliet, 2-macbeth, 3-romeo
def testing(correct_index, test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary):

    correct_lines = 0
    total_lines = 0
    hamlet_probability = 0
    juliet_probability = 0
    macbeth_probability = 0
    romeo_probability = 0
    probabilities = []

    # iterate through test file
    for i in range(len(test_tokens)):

        # compare with all test files

        # HAMLET
        # if test token is in dictionary, add appropriate probability
        if test_tokens[i] in hamlet_dictionary:
            hamlet_probability += hamlet_dictionary[test_tokens[i]][1]
        # otherwise, add pseudo count
        else:
            hamlet_probability += math.log(1 / len(hamlet_train_tokens))

        # JULIET
        if test_tokens[i] in juliet_dictionary:
            juliet_probability += juliet_dictionary[test_tokens[i]][1]
        else:
            juliet_probability += math.log(1 / len(juliet_train_tokens))

        # MACBETH
        if test_tokens[i] in macbeth_dictionary:
            macbeth_probability += macbeth_dictionary[test_tokens[i]][1]
        else:
            macbeth_probability += math.log(1 / len(macbeth_train_tokens))

        # ROMEO
        if test_tokens[i] in romeo_dictionary:
            romeo_probability += romeo_dictionary[test_tokens[i]][1]
        else:
            romeo_probability += math.log(1 / len(romeo_train_tokens))

        if test_tokens[i] == '<eol>':

            probabilities.append(hamlet_probability)
            probabilities.append(juliet_probability)
            probabilities.append(macbeth_probability)
            probabilities.append(romeo_probability)

            print(probabilities)
            if probabilities.index(max(probabilities)) == correct_index:
                correct_lines += 1
                print('yes')

            total_lines += 1
            hamlet_probability = 0
            juliet_probability = 0
            macbeth_probability = 0
            romeo_probability = 0
            probabilities = []

    print(correct_lines, total_lines)

def main():

    # open training files
    hamlet_training_content = open("Training Files/hamlet_train.txt").read()
    juliet_training_content = open("Training Files/juliet_train.txt").read()
    macbeth_training_content = open("Training Files/macbeth_train.txt").read()
    romeo_training_content = open("Training Files/romeo_train.txt").read()

    # tokenize files
    hamlet_train_tokens = hamlet_training_content.split()
    juliet_train_tokens = juliet_training_content.split()
    macbeth_train_tokens = macbeth_training_content.split()
    romeo_train_tokens = romeo_training_content.split()

    # dictionary for each character with tokens and respective counts + probabilities
    hamlet_dictionary = count_tokens(hamlet_train_tokens)
    juliet_dictionary = count_tokens(juliet_train_tokens)
    macbeth_dictionary = count_tokens(macbeth_train_tokens)
    romeo_dictionary = count_tokens(romeo_train_tokens)

    print(hamlet_dictionary)

    # TEST
    # open testing files
    hamlet_testing_content = open("Testing Files/hamlet_test.txt").read()
    juliet_testing_content = open("Testing Files/juliet_test.txt").read()
    macbeth_testing_content = open("Testing Files/macbeth_test.txt").read()
    romeo_testing_content = open("Testing Files/romeo_test.txt").read()

    # tokenize testing files
    hamlet_test_tokens = hamlet_testing_content.split()
    juliet_test_tokens = juliet_testing_content.split()
    macbeth_test_tokens = macbeth_testing_content.split()
    romeo_test_tokens = romeo_testing_content.split()

    testing(0, hamlet_test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary)
    # testing(1, juliet_test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary)
    # testing(2, macbeth_test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary)
    # testing(3, romeo_test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary)


main()