import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn import svm


from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

"""
    reference:
        1) https://scikit-learn.org/stable/modules/feature_extraction.html#customizing-the-vectorizer-classes
"""
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]



stem_words = WordNetLemmatizer()


path_emotion_file = "isear.csv"

# read csv
df_file = pd.read_csv(path_emotion_file, error_bad_lines=False, sep='|', encoding='latin1')

df = df_file[['Field1', 'SIT']]  # Field1 target, SIT feature
#print(df.dtypes)
# print(df.shape) ==> (7503, 2)

# print fist five rows
#asd=df.iloc[:5]
# df.Field1.unique() # distinct row
emotion_groups = df.groupby('Field1').size()

count_vector = TfidfVectorizer(ngram_range=(1,2)) # bag of words

accuracy = list()

for i in range(20):
    train, test = train_test_split(df, test_size=0.3, shuffle=True)



    vectors = count_vector.fit_transform(train.SIT)


    vectors_test = count_vector.transform(test.SIT)
    clf = svm.LinearSVC()
    clf.fit(vectors, train.Field1)

    predict = clf.predict(vectors_test)

    accuracy.append(np.mean(predict == test.Field1))
    print(np.mean(predict == test.Field1))


for i in range(20):
    train, test = train_test_split(df, test_size=0.3, shuffle=True)



    vectors = count_vector.fit_transform(train.SIT)


    vectors_test = count_vector.transform(test.SIT)
    clf = LogisticRegression()
    clf.fit(vectors, train.Field1)

    predict = clf.predict(vectors_test)

    accuracy.append(np.mean(predict == test.Field1))



plt.subplot()
plt.plot(accuracy[:20], color='red', label='Naive Bayes')

print(np.mean(accuracy[:20]))


plt.subplot()
plt.plot(accuracy[20:], color='blue', label='Logistic Regression')
print(np.mean(accuracy[20:]))
# ref: https://matplotlib.org/tutorials/intermediate/legend_guide.html#legend-location
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()

