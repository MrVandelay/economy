# -*- coding: utf-8 -*-

import sys
import pandas as pd
import re
from ftfy import fix_text
from tqdm import tqdm
import os
from matplotlib import style
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.neighbors import NearestNeighbors
import time

pd.set_option('display.max_colwidth', -1)
style.use('fivethirtyeight')

def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def getNearestN(query):
  queryTFIDF_ = vectorizer.transform(query)
  distances, indices = nbrs.kneighbors(queryTFIDF_)
  return distances, indices

def getData(filename):
    data =  pd.read_csv(filename,sep=';',header = 3,index_col=False)
    
    # Replace empty meddelande
    for index, row in data.iterrows():
        if(pd.isnull(row['Meddelande'])):
            row['Meddelande'] = row['Transaktionstyp']

    unique_org = set(data['Meddelande'].values) # set used for increased performance
    return (data['Meddelande'].values)    

# =======================
#      MAIN PROGRAM
# =======================


def findpartner(category_unique, data):


    # Category data
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False) # ngrams

    #categories = pd.read_csv('categories.csv', sep=';')
    #categories_unique = categories[['value', 'fixedOrVariableCost', 'Category']].drop_duplicates()

    #value_unique = categories_unique['value'].values
    #category_unique = categories_unique['Category'].values

    tfidf = vectorizer.fit_transform(category_unique)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)

    #Other data
    #unique_data = getData(filename)
    #distances, indices = getNearestN(data)
    queryTFIDF_ = vectorizer.transform(data)
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    data = list(data) #need to convert back to a list

    matches = []

    for i,j in enumerate(indices):
        temp = [distances[i][0], category_unique[j], data[i]]
        matches.append(temp)

    matches = pd.DataFrame(matches, columns=['Match confidence (lower is better)','Value','From data'])

    print(matches)

    return