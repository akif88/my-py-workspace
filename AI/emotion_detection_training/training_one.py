"""
Base Algorithm:
    - https://en.wikipedia.org/wiki/Tf-idf -(In information retrieval, tf–idf or TFIDF, short for term frequency–inverse
    document frequency, is a numerical statistic that is intended to reflect how important a word is to a document in a
     collection or corpus.) --


Reference:
    1) https://scikit-learn.org/stable/datasets/index.html#the-20-newsgroups-text-dataset
    2) https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
"""

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

from pprint import pprint

import numpy as np


newsgroups_train = fetch_20newsgroups(subset='train', shuffle=True)
pprint(list(newsgroups_train.target_names))
print(newsgroups_train.filenames.shape)
print(newsgroups_train.target.shape)

vect = CountVectorizer()
asd = vect.fit_transform(newsgroups_train.data)

vectorizer = TfidfVectorizer(lowercase=False)
asd = asd.astype('str')
vectors = vectorizer.fit_transform(asd)
print(vectors.shape)


newsgroups_test = fetch_20newsgroups(subset='test', shuffle=True)
vectors_test = vectorizer.transform(newsgroups_test.data)
clf = MultinomialNB(alpha=.01)
clf.fit(vectors, newsgroups_train.target)

predict = clf.predict(vectors_test)
result = metrics.f1_score(newsgroups_test.target, predict, average='macro')
print(result)


def show_top10(classifier, vectorizer, categories):
    feature_names = np.asarray(vectorizer.get_feature_names())
    for i, category in enumerate(categories):
        top10 = np.argsort(classifier.coef_[i])[-10:]
        print("%s: %s" % (category, " ".join(feature_names[top10])))

show_top10(clf, vectorizer, newsgroups_train.target_names)














""""# Train Dataset
# get 20 news group categories datasets 
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
#print(twenty_train.target_name) # to see all categories
print("\n".join(twenty_train.data[0].split("\n")[:3])) # to see first line of the first data

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
print(X_train_counts.shape)


clf = MultinomialNB().fit(X_train_counts, twenty_train.target)


# Test Dataset
twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
predict = clf.predict(twenty_test.data)
accuracy = np.mean(predict == twenty_test.target)
print(accuracy)"""
