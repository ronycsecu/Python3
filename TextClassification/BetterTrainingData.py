import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votes = votes.count(mode(votes))
        conf = choice_votes/len(votes)
        return conf

short_pos = open("short_reviews/positive.txt", "r").read()
short_neg = open("short_reviews/negative.txt", "r").read()

documents = []

for review in short_pos.split('\n'):
    documents.append((review, "pos"))

for review in short_neg.split('\n'):
    documents.append((review, "neg"))

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

#adding positive and negative words in the all word list

for w in short_pos:
    all_words.append(w.lower())
for w in short_neg:
    all_words.append(w.lower())


all_words = nltk.FreqDist(all_words)
# print(all_words.most_common(15))
# print(all_words["nice"])

word_features = list(all_words.keys())[:5000] #Top 5000 words
# #print(word_features)

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))
featurests = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featurests)

training_set = featurests[:10000]
testing_set = featurests[10000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Original Naive bayes Algo accuracy: ", (nltk.classify.accuracy(classifier, testing_set))*100)

#classifier.show_most_informative_features(15)

# save_classifier = open("naivebayes.pickle", "wb")
# pickle.dump(classifier, save_classifier)
# save_classifier.close()

#Multinomial Naive Bayes
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("Multinomial Naive bayes Algo accuracy: ", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

#Bernouli Naive Bayes
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("Bernouli Naive bayes Algo accuracy: ", (nltk.classify.accuracy(BNB_classifier, testing_set))*100)

#LogisticRegression
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression Algo accuracy: ", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

#SGDClassifier
SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier Algo accuracy: ", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

#SVC
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC classification Algo accuracy: ", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

#LinearSVC
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC Algo accuracy: ", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

#NuSVC
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC Algo accuracy: ", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

voted_classifier = VoteClassifier(classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BNB_classifier,
                                  LogisticRegression_classifier)
print("Voted Classifier Accuracy:  ", ((nltk.classify.accuracy(voted_classifier, testing_set))*100))

print("Classification :", voted_classifier.classify(testing_set[0][0]), "confidence %: ", voted_classifier.confidence(testing_set[0][0])*100)
print("Classification :", voted_classifier.classify(testing_set[1][0]), "confidence %: ", voted_classifier.confidence(testing_set[1][0])*100)
print("Classification :", voted_classifier.classify(testing_set[2][0]), "confidence %: ", voted_classifier.confidence(testing_set[2][0])*100)
print("Classification :", voted_classifier.classify(testing_set[3][0]), "confidence %: ", voted_classifier.confidence(testing_set[3][0])*100)
print("Classification :", voted_classifier.classify(testing_set[4][0]), "confidence %: ", voted_classifier.confidence(testing_set[4][0])*100)