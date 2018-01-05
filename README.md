# Spam-Filter


Basic Approach of our solution:
-------------------------------
We followed the following explanation for our approach in Spam Filter:
Given set of class, C := {ham, spam}, and a document D consisting of words D := {W_1, ..., W_k}. We wish to ascertain the probability that the document belongs to some class C_j given some set of training data associating documents and classes.

By Bayes' Theorem, we have that P(C_j|D) = P(D|C_j)*P(C_j)/P(D).

The LHS is the probability that the document belongs to class C_j given the document itself (by which is meant, in practice, the word frequencies occurring in this document), and our program will calculate this probability for each j and spit out the most likely class for this document.

P(C_j) is referred to as the "prior" probability, or the probability that a document belongs to C_j in general, without seeing the document first. P(D|C_j) is the probability of seeing such a document, given that it belongs to C_j. Here, by assuming that words appear independently in documents (this being the "naive" assumption), we can estimate

P(D|C_j) ~= P(W_1|C_j)*...*P(W_k|C_j)

where P(W_i|C_j) is the probability of seeing the given word in a document of the given class. Finally, P(D) can be seen as merely a scaling factor and is not strictly relevant to classificiation, unless we want to normalize the resulting scores and actually see probabilities. In this case, note that

P(D) = SUM_j(P(D|C_j)*P(C_j))

One practical issue with performing these calculations is the possibility of float64 underflow when calculating P(D|C_j), as individual word probabilities can be arbitrarily small, and a document can have an arbitrarily large number of them. A typical method for dealing with this case is to transform the probability to the log domain and perform additions instead of multiplications:

log P(C_j|D) ~ log(P(C_j)) + SUM_i(log P(W_i|C_j))

where i = 1, ..., k. Note that by doing this, we are discarding the scaling factor P(D) and our scores are no longer probabilities; however, the monotonic relationship of the scores is preserved by the log function

Training:
==========
Using multinomial model, with unique words as features of documents, we identified, the total number of spam and total number of ham documents, unique words in all documents, count of occurences of each unique word in every document, from the training data set. Using that we estimated likelihoods(P(D|C_j)) of each word and the class priors P(ham), P (spam). Using all these, we estimated log P(C_j|D).

Laplace Smoothing:
--------------------
We have assigned a small probability to unique words with zero occurences in either document. This alleviates the problem of zero values while calculating log of probabilities.

Testing Phase:
=================
1. To classify an unlabeled document, we estimated log of posterior probability for each class, P(Ham|D) and P(Spam|D).
2. Class with higher posterior probability is assigned as label to the unlabeled test document.
3. When we saw new words that didn't occur in training data, we ignore such events as it wasn't making sense to use it add to either probabilities.

Result:
=========
With the given training data set and test data set, we got 90.6 percent accuracy.
