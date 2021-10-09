import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
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

vectorizers = TfidfVectorizer()
#vectorizers = TfidfVectorizer()
vectors = vectorizers.fit_transform(train.SIT)
#print(vectors.shape)

vectors_test = vectorizers.transform(test.SIT)
lr = LinearSVC()

algorithms_estimator = Pipeline([
    ('vect', TfidfVectorizer()),
    ('lr', LinearSVC()),
])

parameters = {
    'lr__random_state': [None, np.random.randint(10000)],

}
"""
    'vect__tokenizer': [None, LemmaTokenizer()],
    'vect__ngram_range': [(1,1), (1,2), (1,3)],
    'vect__stop_words': [None, 'english'],
    'vect__smooth_idf': [True, False],
    'lr__random_state': [None, np.random.randint(100)],
    'vect__ngram_range': [(1,1), (1,2)],
"""
clf = GridSearchCV(algorithms_estimator, parameters, cv=3, n_jobs=8)
clf.fit(train.SIT, train.Field1)


result=clf.cv_results_
asd = pd.DataFrame(result)
asd.plot()
plt.show()

"""
print(metrics.classification_report(test.Field1, clf.predict(test.SIT), target_names=df.Field1.unique()))

from IPython.display import display
asdd = metrics.confusion_matrix(test.Field1, clf.predict(test.SIT))
for predicted in category_id_df.category_id:
  for actual in category_id_df.category_id:
    if predicted != actual and conf_mat[actual, predicted] >= 10:
      print("'{}' predicted as '{}' : {} examples.".format(id_to_category[actual], id_to_category[predicted], conf_mat[actual, predicted]))
      display(df.loc[indices_test[(y_test == actual) & (y_pred == predicted)]][['Product', 'Consumer_complaint_narrative']])
      print('')

"""
#predict = clf.predict(vectors_test)
#accuracy = np.mean(predict == test.Field1)

#print(accuracy)

