import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


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

train, test = train_test_split(df, test_size=0.3, shuffle=True)
asd = np.random
print(asd)
clf = Pipeline([
    ('vect', TfidfVectorizer(ngram_range=(1,2), tokenizer=LemmaTokenizer())),
    ('lr', LinearSVC()),
])



clf.fit(train.SIT, train.Field1)

predict = clf.predict(test.SIT)

accuracy = np.mean(predict == test.Field1)

print(accuracy)

# ref: https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html#evaluation-of-the-performance-on-the-test-set
print(metrics.classification_report(test.Field1, predict, target_names=df.Field1.unique()))

ddd=metrics.precision_score(test.Field1, predict, average=None)
plt.scatter(df.Field1.unique(), ddd)
plt.show()