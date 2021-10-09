import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

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

vectorizers = TfidfVectorizer()
#vectorizers = TfidfVectorizer()
vectors = vectorizers.fit_transform(train.SIT)
#print(vectors.shape)

vectors_test = vectorizers.transform(test.SIT)
lr = LogisticRegression()

algorithms_estimator = Pipeline([
    ('vect', TfidfVectorizer()),
    ('lr', LogisticRegression()),
])

parameters = {
    'vect__tokenizer': [None, LemmaTokenizer()],
    'lr__penalty': ['l1', 'l2'],

}
"""
'vect__stop_words': [None, 'english'],
'vect__smooth_idf': [True, False],
    'vect__ngram_range': [(1,1), (1,2)],
"""
clf = GridSearchCV(algorithms_estimator, parameters, cv=3, n_jobs=8)
clf.fit(train.SIT, train.Field1)

result=clf.cv_results_
print()
asd = pd.DataFrame(result)
asd.plot()
plt.show()


#predict = clf.predict(vectors_test)
#accuracy = np.mean(predict == test.Field1)

#print(accuracy)

