import math

# output dictionary, which includes:
# each unique token as key
# and the number of occurrences as well as the probability (utilizes log) of each token as values bni
def count_tokens(tokens):

    token_dictionary = {}

    for i in range(len(tokens)):

        if tokens[i] not in token_dictionary:
            token_count = tokens.count(tokens[i])
            token_dictionary[tokens[i]] = [token_count]

    return token_dictionary

def testing(character, test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens):

    character_names = ['Hamlet', 'Juliet', 'Macbeth', 'Romeo']
    hamlet_probability = 0
    juliet_probability = 0
    macbeth_probability = 0
    romeo_probability = 0
    correct = 0
    total = 0
    p = []

    for i in range(len(test_tokens)):

        # print('-----------------')
        # print(test_tokens[i])

        if test_tokens[i] in hamlet_dictionary:
            hamlet_probability += math.log10(hamlet_dictionary[test_tokens[i]][0] / len(hamlet_train_tokens))
            # print('hamlet')
        else:
            hamlet_probability += math.log10(1 / len(hamlet_train_tokens))

        if test_tokens[i] in juliet_dictionary:
            juliet_probability += math.log10(juliet_dictionary[test_tokens[i]][0] / len(juliet_train_tokens))
            # print('juliet')
        else:
            juliet_probability += math.log10(1 / len(hamlet_train_tokens)) # all are this so probability is not zero but also smaller than 1 / largest_training_file

        if test_tokens[i] in macbeth_dictionary:
            macbeth_probability += math.log10(macbeth_dictionary[test_tokens[i]][0] / len(macbeth_train_tokens))
            # print('macbeth')
        else:
            macbeth_probability += math.log10(1 / len(hamlet_train_tokens))

        if test_tokens[i] in romeo_dictionary:
            romeo_probability += math.log10(romeo_dictionary[test_tokens[i]][0] / len(romeo_train_tokens))
            # print('romeo')
        else:
            romeo_probability += math.log10(1 / len(hamlet_train_tokens))

        prior_hamlet = len(hamlet_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_juliet = len(juliet_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_macbeth = len(macbeth_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))
        prior_romeo = len(romeo_train_tokens) / (len(hamlet_train_tokens) + len(juliet_train_tokens) + len(macbeth_train_tokens) + len(romeo_train_tokens))


        if test_tokens[i] == '<eol>':

            p.append(math.log10(prior_hamlet) + hamlet_probability)
            p.append(math.log10(prior_juliet) + juliet_probability)
            p.append(math.log10(prior_macbeth) + macbeth_probability)
            p.append(math.log10(prior_romeo) + romeo_probability)

            if p.index(max(p)) == character:
                correct += 1

            total += 1

            hamlet_probability = 0
            juliet_probability = 0
            macbeth_probability = 0
            romeo_probability = 0
            p = []

    accuracy = correct / total
    print('{} Accuracy: {}'.format(character_names[character], round(accuracy*100, 4)))

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

    print("UNIGRAM CLASSIFICATION")

    # testing(0, hamlet_test_tokens, hamlet_train_tokens, hamlet_dictionary, juliet_train_tokens, juliet_dictionary, macbeth_train_tokens, macbeth_dictionary, romeo_train_tokens, romeo_dictionary)
    testing(0, hamlet_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(1, juliet_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(2, macbeth_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)
    testing(3, romeo_test_tokens, hamlet_dictionary, juliet_dictionary, macbeth_dictionary, romeo_dictionary, hamlet_train_tokens, juliet_train_tokens, macbeth_train_tokens, romeo_train_tokens)



main()