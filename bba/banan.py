# -*- coding: utf-8 -*-



import re
from ftfy import fix_text
from tqdm import tqdm
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors




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

def findpartner(values_unique, data):

    # Vectorizer
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False) # ngrams

    # Sample values
    tfidf = vectorizer.fit_transform(values_unique)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)

    # Compare to data
    queryTFIDF_ = vectorizer.transform(data)
    distances, indices = nbrs.kneighbors(queryTFIDF_)
    
    return distances, indices