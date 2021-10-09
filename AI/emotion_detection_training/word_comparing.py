import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import metrics

from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]



path_emotion_file = "isear.csv"

# read csv
df_file = pd.read_csv(path_emotion_file, error_bad_lines=False, sep='|', encoding='latin1')

df = df_file[['Field1', 'SIT']]  # Field1 target, SIT feature


emotion_groups = df.groupby('Field1').size()

train, test = train_test_split(df, test_size=0.3, shuffle=True)


vectorizers = TfidfVectorizer(stop_words='english')
vectors = vectorizers.fit_transform(train.SIT)

vectors_test = vectorizers.transform(test.SIT)
clf = MultinomialNB()
clf.fit(vectors, train.Field1)

predict = clf.predict(vectors_test)

accuracy = np.mean(predict == test.Field1)
print(accuracy)

# ref: https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a

def show_top10(classifier, vectorizer, categories):
    feature_names = np.asarray(vectorizer.get_feature_names())
    for i, category in enumerate(categories):
        top10 = np.argsort(classifier.coef_[i])[-10:]
        print("%s: %s" % (category, " ".join(feature_names[top10])))


show_top10(clf, vectorizers, df.groupby('Field1').groups)


from collections import Counter


df_anger = df[df['Field1'].str.contains('shame')]

stopwords = stopwords.words('english')
# RegEx for stopwords
RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
# replace '|'-->' ' and drop all stopwords
words = (df_anger.SIT.str.lower().replace([r'\|', RE_stopwords], [' ', ''], regex=True).str.cat(sep=' ').split())



# generate DF out of Counter
rslt = pd.DataFrame(Counter(words).most_common(14),
                    columns=['Word', 'Frequency']).set_index('Word')


print(rslt.drop('ã¡').drop('.'))

# plot
rslt.drop('ã¡').drop('.').drop('\'').drop(',').plot.bar(rot=0, figsize=(16,10), width=0.8)
plt.show()
