import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer


# Importing the dataset
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter='\t', quoting=3)

dataset.head()

dataset['Liked'].value_counts().plot(kind='bar')


corpus = []
ps = PorterStemmer()
for i in range(0, dataset['Review'].size):
    # get review and remove non alpha chars
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    # to lower-case
    review = review.lower()
    # split into tokens, apply stemming and remove stop words
    review = ' '.join([ps.stem(w) for w in review.split() if not w in set(stopwords.words('english'))])
    corpus.append(review)


wordcloud = WordCloud().generate(" ".join(corpus))


plt.figure()
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus).toarray()
vectorizer.get_feature_names()
print(X[124])
