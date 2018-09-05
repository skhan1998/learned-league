#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 16:32:28 2018

@author: samirkhan
"""

#This file contains all functions for finding neighbors

import numpy as np
import sent2vec

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from sklearn.decomposition import PCA

def find_neighbors(df, new):
    qs = list(df["Question"])
    raw_qs = list(df["Raw Question"])
    y = np.array(df["Correct?"])


    embedder1 = sent2vec.Sent2vecModel()
    embedder1.load_model('wiki_unigrams.bin')
    X1 = embedder1.embed_sentences(qs)
    Xtest1 = embedder1.embed_sentences(new)

#    model = PCA(n_components=50)
#    X1 = model.fit_transform(X1)
#    Xtest1 = model.transform(Xtest1)

    embedder2 = TfidfVectorizer(stop_words = "english")
    X2 = embedder2.fit_transform(qs).todense()
    Xtest2 = embedder2.transform(new).todense()

#    model = PCA(n_components=50)
#    X2 = model.fit_transform(X2)
#    Xtest2 = model.transform(Xtest2)

# Code for random forests that was cut
#    print "Fitting random forest"
#    model = RandomForestClassifier(n_estimators=100)
#    model.fit(X1,y)
#
#    score = 100*np.mean(cross_val_score(model, X1, y))
#    print "Accuracy: %.2f%%" % score

#    print "Predicting on new questions"
#    yhat = 100*model.predict_proba(Xtest1)[:,1]

#    print "\nProbabilities of answering correctly:"
#    for j in range(1, len(yhat)+1):
#        print "Q%.0f %.1f%%" % (j, yhat[j-1])

#    influential = []
#    y_influential = []
#    train_leaves = model.apply(X1)
#    test_leaves = model.apply(Xtest1)
#    for j in range(6):
#        print "Rationale for question %.0f" % (j+1)
#        leaves = test_leaves[j,:]
#        matches = np.sum(leaves == train_leaves, axis =1)
#        top = matches.argsort()[-5:][::-1]
#        match_qs = list(np.array(raw_qs)[top])
#        match_ys = list(y[top])
#        influential.append(match_qs)
#        y_influential.append(match_ys)

    neigh1 = NearestNeighbors(5)
    neigh1.fit(X1)

    neigh2 = NearestNeighbors(5)
    neigh2.fit(X2)

    neighbors = []
    y_neighbors = []
    for j in range(6):
        testq1 = Xtest1[j,:].reshape(1,-1)
        testq2 = Xtest2[j,:].reshape(1,-1)

        neighbors1 = neigh1.kneighbors(testq1)[1]
        neighbors2 = neigh2.kneighbors(testq2)[1]

        both = np.union1d(neighbors1, neighbors2)
        matches = np.array(raw_qs)[both]
        ys = y[both]
        neighbors.append(matches)
        y_neighbors.append(ys)

    return [neighbors, y_neighbors]
