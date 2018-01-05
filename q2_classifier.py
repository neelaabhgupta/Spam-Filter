import numpy as np
import sys
import math


def test(test_file, out_file, unique_words, log_probabilites_ham, log_probabilities_spam):
    test_fd = open(test_file, 'r')
    out_fd = open(out_file, 'w')
    # out_fd.write("<ID>,<spam/ham>\n")
    num_correct_classification = 0
    total_docs = 0
    for doc in test_fd:
        total_docs += 1
        list_of_words_doc = doc.strip().split()
        prob_ham = 0.0
        prob_spam = 0.0
        i = 2
        while (i < len(list_of_words_doc)):
            if list_of_words_doc[i] in unique_words:
                prob_ham += int(list_of_words_doc[i + 1]) * log_probabilites_ham[unique_words[list_of_words_doc[i]]]
                prob_spam += int(list_of_words_doc[i + 1]) * log_probabilities_spam[unique_words[list_of_words_doc[i]]]
                pass
            else:
                # what to be done for new words??
                print "new word ", list_of_words_doc[i]
            i += 2

        # classify ham/spam based on training data
        if prob_ham > prob_spam:
            # test_ham_count += 1
            out_fd.write(list_of_words_doc[0] + ' ' + "ham\n")
            if (list_of_words_doc[1] == 'ham'):
                num_correct_classification += 1
        elif prob_spam > prob_ham:
            # test_spam_count += 1
            out_fd.write(list_of_words_doc[0] + ' ' + "spam\n")
            if (list_of_words_doc[1] == 'spam'):
                num_correct_classification += 1
        else:
            print "equal probabilities, how to classify? :)"

    # print num_correct_classification, total_docs
    print "Accuracy Percentage : ", float(num_correct_classification) / total_docs * 100

    out_fd.close()
    test_fd.close()


def calculate_log_probabilities(count_unique_words_docs, ham_rows, spam_rows):
    # count occurences of each unique word in spam/ham
    unique_words_count_ham = np.sum(count_unique_words_docs[ham_rows], 0)

    # find out which all words have count zero and initialize them with a very less value
    # inorder to avoid zeros while taking log of probablities
    zero_count_words_indices_ham = np.where(unique_words_count_ham == 0)[0]
    # print len(zero_count_words_indices_ham)
    unique_words_count_ham[zero_count_words_indices_ham] += 0.00000001

    unique_words_count_spam = np.sum(count_unique_words_docs[spam_rows], 0)
    zero_count_words_indices_spam = np.where(unique_words_count_spam == 0)[0]
    # print len(zero_count_words_indices_spam)
    unique_words_count_spam[zero_count_words_indices_spam] += 0.00000001

    total_words_in_ham_docs = np.sum(unique_words_count_ham)
    total_words_in_spam_docs = np.sum(unique_words_count_spam)
    # print total_words_in_ham_docs, total_words_in_spam_docs

    probabilities_words_ham = unique_words_count_ham / total_words_in_ham_docs
    probabilities_words_spam = unique_words_count_spam / total_words_in_spam_docs

    # finding log2 is faster than natural log, log10 using numpy
    return np.log2(probabilities_words_ham), np.log2(probabilities_words_spam)


def count_unique_words_in_each_document(train_file, unique_words, ham_rows, spam_rows):
    train_fd = open(train_file, 'r')
    num_hams = len(ham_rows)
    num_spams = len(spam_rows)
    count_unique_words_docs = np.zeros((num_hams + num_spams, len(unique_words)))
    doc_num = 0
    for doc in train_fd:
        list_of_words_doc = doc.strip().split()
        i = 2
        while (i < len(list_of_words_doc)):
            count_unique_words_docs[doc_num][unique_words[list_of_words_doc[i]]] += int(list_of_words_doc[i + 1])
            i += 2
        doc_num += 1
    train_fd.close()
    return count_unique_words_docs


def find_unique_words_and_docs_rows(train_file):
    unique_words = dict()
    # unique_words_list = list()
    train_fd = open(train_file, 'r')
    count_of_unique_words = 0
    doc_num = 0
    # take note of row index of each ham/spam mail in the training data
    ham_rows = []
    spam_rows = []
    for doc in train_fd:
        list_of_words_doc = doc.strip().split()
        i = 2
        while (i < len(list_of_words_doc)):
            if list_of_words_doc[i] not in unique_words:
                unique_words[list_of_words_doc[i]] = count_of_unique_words
                count_of_unique_words += 1
            i += 2
        if list_of_words_doc[1] == 'ham':
            ham_rows.append(doc_num)
        elif list_of_words_doc[1] == 'spam':
            spam_rows.append(doc_num)
        else:
            print "unknown doc class"
        doc_num += 1

    train_fd.close()

    # print unique_words, len(ham_rows), len(spam_rows)
    return unique_words, ham_rows, spam_rows


def train(train_file):
    # find all unique words in training set and number of documents/mails of each class(ham/spam)
    unique_words, ham_rows, spam_rows = find_unique_words_and_docs_rows(train_file)
    # count the number of occurences of each unique word in every document/mail
    docs_words_count = count_unique_words_in_each_document(train_file, unique_words, ham_rows, spam_rows)
    # find out probabilities of each unique word in a particular class (ham/spam)
    log_probabilites_ham, log_probabilities_spam = calculate_log_probabilities(docs_words_count, ham_rows, spam_rows)
    return unique_words, log_probabilites_ham, log_probabilities_spam


def main():
    # print "This is the name of the script: ", sys.argv[0]
    # print "Number of arguments: ", len(sys.argv)
    # print "The arguments are: " , str(sys.argv)
    if len(sys.argv) < 7:
        print "too few arguments..."
        return
    elif len(sys.argv) > 7:
        print "too many arugments.."
        return
    if (sys.argv[1] == "-f1"):
        train_file = sys.argv[2]
    else:
        print "check options/arguments"
        return
    if (sys.argv[3] == "-f2"):
        test_file = sys.argv[4]
    else:
        print "check options/arguments"
        return
    if (sys.argv[5] == "-o"):
        out_file = sys.argv[6]
    else:
        print "check options/arguments"
        return

    print train_file, test_file, out_file

    # training involves finding probabilities of occurences of each of unique words per class (ham/spam)
    unique_words, log_probabilites_ham, log_probabilities_spam = train(train_file)
    # test our learning using test data and measure accuracy
    test(test_file, out_file, unique_words, log_probabilites_ham, log_probabilities_spam)


if __name__ == '__main__':
    main()