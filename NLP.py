# Natural Language Processing for Predict and Map Honeypot Logs to MITRE

# Importing the libraries
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Importing the dataset
dataset = pd.read_csv('data.tsv', delimiter = '\t', quoting = 3)

# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 1203):
    log = re.sub('[^a-zA-Z0-9]', ' ', dataset['logs'][i])
    log = log.lower()
    log = log.split()
    ps = PorterStemmer()
    log = [ps.stem(word) for word in log if not word in set(stopwords.words('english'))]
    log = ' '.join(log)
    corpus.append(log)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 400)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

# Training the Random Forest Regression model on the whole dataset
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X, y)

# Saving the trained model
joblib.dump(regressor, 'random_forest_model.joblib')

# Dumping the CountVectorizer
joblib.dump(cv, 'count_vectorizer.joblib')