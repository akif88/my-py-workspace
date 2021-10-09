import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

path_emotion_file = "isear.csv"

# read csv
df_file = pd.read_csv(path_emotion_file, error_bad_lines=False, sep='|', encoding='latin1')

df = df_file[['Field1', 'SIT']]  # Field1 target, SIT feature
# print(df.shape) ==> (7503, 2)

# print fist five rows
#asd=df.iloc[:5]
# df.Field1.unique() # distinct row
emotion_groups = df.groupby('Field1').size()

train, test = train_test_split(df, test_size=0.3, shuffle=True)

vectorizers = TfidfVectorizer(smooth_idf=False)
#vectorizers = TfidfVectorizer()
vectors = vectorizers.fit_transform(train.SIT)
#print(vectors.shape)
MultinomialNB()
vectors_test = vectorizers.transform(test.SIT)
clf = LogisticRegression()
clf.fit(vectors, train.Field1)

predict = clf.predict(vectors_test)
#result = metrics.f1_score(test.Field1, predict, average='macro')
#print(result)

accuracy = np.mean(predict == test.Field1)
print(accuracy)


def show_top10(classifier, vectorizer, categories):
    feature_names = np.asarray(vectorizer.get_feature_names())
    for i, category in enumerate(categories):
        top10 = np.argsort(classifier.coef_[i])[-10:]
        #print(top10, classifier.coef_[i])
        print("%s: %s" % (category, " ".join(feature_names[top10])))

show_top10(clf, vectorizers, df.Field1.unique())

