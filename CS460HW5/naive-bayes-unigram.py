import nltk
nltk.download('punkt')


# insert each unique token and the number of occurrences into dictionary
def count_tokens(tokens):

    token_dictionary = {}

    for i in range(len(tokens)):

        if tokens[i] not in token_dictionary:
            token_count = tokens.count(tokens[i])
            token_dictionary.update({tokens[i]: token_count})

    return token_dictionary


def main():

    # open files
    hamlet_file_content = open("Training Files/hamlet_train.txt").read()
    juliet_file_content = open("Training Files/juliet_train.txt").read()
    macbeth_file_content = open("Training Files/macbeth_train.txt").read()
    romeo_file_content = open("Training Files/romeo_train.txt").read()

    # tokenize files
    hamlet_tokens = hamlet_file_content.split()
    juliet_tokens = juliet_file_content.split()
    macbeth_tokens = macbeth_file_content.split()
    romeo_tokens = romeo_file_content.split()

    # dictionary for each character with tokens and respective counts
    hamlet_dictionary = count_tokens(hamlet_tokens)
    juliet_dictionary = count_tokens(juliet_tokens)
    macbeth_dictionary = count_tokens(macbeth_tokens)
    romeo_dictionary = count_tokens(romeo_tokens)





main()