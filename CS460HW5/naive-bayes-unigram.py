import math


# output dictionary, which includes:
# each unique token as key + the number of occurrences of the key as the value
def count_tokens(tokens):

    token_dictionary = {}

    for i in range(len(tokens)):

        if tokens[i] not in token_dictionary:
            token_count = tokens.count(tokens[i])
            token_dictionary[tokens[i]] = [token_count]

    return token_dictionary


# given the trainings files and a specific test file, this outputs the accuracy of classifying text from the test file
def testing(character, test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens):

    character_names = ['Hamlet', 'Juliet', 'Macbeth', 'Romeo']
    hamlet_probability = 0
    juliet_probability = 0
    macbeth_probability = 0
    romeo_probability = 0
    correct = 0
    total = 0
    p = []

    # iterate through each word in the given test file
    for i in range(len(test_tokens)):

        # calculate probability that the word is from each file -> (# of occurrences in file) / (total words in file)
        # if there are no occurrences, create pseudo count to avoid zero but less than 1 / largest_training_file_size
        if test_tokens[i] in hamlet_dictionary: hamlet_probability += math.log10(hamlet_dictionary[test_tokens[i]][0] / len(hamlet_train_tokens))
        else: hamlet_probability += math.log10(1 / len(hamlet_train_tokens))

        if test_tokens[i] in juliet_dictionary: juliet_probability += math.log10(juliet_dictionary[test_tokens[i]][0] / len(juliet_train_tokens))
        else: juliet_probability += math.log10(1 / len(hamlet_train_tokens))

        if test_tokens[i] in macbeth_dictionary: macbeth_probability += math.log10(macbeth_dictionary[test_tokens[i]][0] / len(macbeth_train_tokens))
        else: macbeth_probability += math.log10(1 / len(hamlet_train_tokens))

        if test_tokens[i] in romeo_dictionary: romeo_probability += math.log10(romeo_dictionary[test_tokens[i]][0] / len(romeo_train_tokens))
        else: romeo_probability += math.log10(1 / len(hamlet_train_tokens))

        # calculate the prior probabilities - the number of words in file divided total number of words in all files
        prior_hamlet = len(hamlet_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_juliet = len(juliet_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_macbeth = len(macbeth_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_romeo = len(romeo_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))

        # we are testing on each line individually
        if test_tokens[i] == '<eol>':

            # add prior probabilities to sum of probability character said each word in line
            p.append(math.log10(prior_hamlet) + hamlet_probability)
            p.append(math.log10(prior_juliet) + juliet_probability)
            p.append(math.log10(prior_macbeth) + macbeth_probability)
            p.append(math.log10(prior_romeo) + romeo_probability)

            # if the largest overall probability is the correct character, add to 'correct' variable
            if p.index(max(p)) == character:
                correct += 1

            # count total number of lines in file
            total += 1

            # reset variables after analyzing line
            hamlet_probability = 0
            juliet_probability = 0
            macbeth_probability = 0
            romeo_probability = 0
            p = []

    # calculate and output individual accuracies
    accuracy = correct / total
    print('{} Accuracy: {}'.format(character_names[character], round(accuracy*100, 4)))

def main():

    # open training files
    hamlet_training_content = open("Training Files/hamlet_train.txt").read()
    juliet_training_content = open("Training Files/juliet_train.txt").read()
    macbeth_training_content = open("Training Files/macbeth_train.txt").read()
    romeo_training_content = open("Training Files/romeo_train.txt").read()

    # create unigram tokens for training files
    hamlet_train_tokens = hamlet_training_content.split()
    juliet_train_tokens = juliet_training_content.split()
    macbeth_train_tokens = macbeth_training_content.split()
    romeo_train_tokens = romeo_training_content.split()

    # create dictionary for each character with tokens and respective counts + probabilities
    hamlet_dictionary = count_tokens(hamlet_train_tokens)
    juliet_dictionary = count_tokens(juliet_train_tokens)
    macbeth_dictionary = count_tokens(macbeth_train_tokens)
    romeo_dictionary = count_tokens(romeo_train_tokens)

    # open testing files
    hamlet_testing_content = open("Testing Files/hamlet_test.txt").read()
    juliet_testing_content = open("Testing Files/juliet_test.txt").read()
    macbeth_testing_content = open("Testing Files/macbeth_test.txt").read()
    romeo_testing_content = open("Testing Files/romeo_test.txt").read()

    # create unigram tokens for testing files
    hamlet_test_tokens = hamlet_testing_content.split()
    juliet_test_tokens = juliet_testing_content.split()
    macbeth_test_tokens = macbeth_testing_content.split()
    romeo_test_tokens = romeo_testing_content.split()

    # test on each file
    print("UNIGRAM CLASSIFICATION")
    testing(0, hamlet_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(1, juliet_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(2, macbeth_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(3, romeo_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)

main()