from flask import Flask, jsonify
import os
import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle

app = Flask(__name__)
tfidf_model_pickle_file_path = 'pickle_jar/tfidf_model.dat'
people_names_pickle_file_path = 'pickle_jar/people_names.dat'

def get_people_names():
    if os.path.exists(people_names_pickle_file_path):
        people_names_pickle_file = open(people_names_pickle_file_path, 'r')
        people_names = pickle.load(people_names_pickle_file)
    else:
        people = pd.read_csv('people.csv')
        people_names = people.name
        people_names_pickle_file = open(people_names_pickle_file_path, 'wb')
        pickle.dump(people_names, people_names_pickle_file)
    return people_names

def get_or_make_tfidf_model():
    if os.path.exists(tfidf_model_pickle_file_path):
        tfidf_file = open(tfidf_model_pickle_file_path, 'r')
        tfidf_model = pickle.load(tfidf_file)
        features = tfidf_model['features']
        tfidf = tfidf_model['tfidf']
    else:
        people = pd.read_csv('people.csv')
        documents = people.text
        model = TfidfVectorizer(stop_words='english', norm=None, smooth_idf=False).fit(documents)
        tfidf = model.transform(documents)
        features = model.get_feature_names()
        tfidf_model = {'features': features, 'tfidf': tfidf}
        tfidf_file = open(tfidf_model_pickle_file_path, 'wb')
        pickle.dump(tfidf_model, tfidf_file)
    return tfidf, features

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/top10words/')
@app.route('/top10words/<name>')
def top10words(name='random'): #'''Barack Obama'):
    people_names = get_people_names()
    if name == 'random':
        idx = random.randint(0, len(people_names))
    else:
        idx = np.where(people_names == name)[0][0]
    name = people_names[idx]
    tfidf, features = get_or_make_tfidf_model()
    # return jsonify([[features[x[0]], x[1]] for x in
    #  zip(tfidf[idx].indices[tfidf[idx].data.argsort()[::-1]], tfidf[idx].data[tfidf[idx].data.argsort()[::-1]])])
    return jsonify({'name': name, 'top 10 words': [features[x] for x in tfidf[idx].indices[tfidf[idx].data.argsort()[::-1][0:10]]]})

@app.route('/top10relationships/')
@app.route('/top10relationships/<name>')
def top10relationships(name='random'): #'''Barack Obama'):
    people_names = get_people_names()
    if name == 'random':
        idx = random.randint(0, len(people_names))
    else:
        idx = np.where(people_names == name)[0][0]
    name = people_names[idx]
    tfidf, features = get_or_make_tfidf_model()
    cosine_similarities = linear_kernel(tfidf[idx], tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    return jsonify({'name': name,
                    'top 10 relationships': [str(this_name) for this_name in people_names.iloc[related_docs_indices].values]})

if __name__ == "__main__":
    import sframe
    people = sframe.SFrame('people_wiki.gl/')
    people.export_csv('people.csv')
    app.run()