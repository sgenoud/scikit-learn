"""
========================================================
Topics extraction with Non-Negative Matrix Factorization
========================================================

This is a proof of concept application of Non Negative Matrix
Factorization of the term frequency matrix of a corpus of documents so
as to extract an additive model of the topic structure of the corpus.

The default parameters (n_samples / n_features / n_topics) should make
the example runnable in a couple of tens of seconds. You can try to
increase the dimensions of the problem be ware than the time complexity
is polynomial.

Here are some sample extracted topics that look quite good:

Topic #0:
god people bible israel jesus christian true moral think christians
believe don say human israeli church life children jewish

Topic #1:
drive windows card drivers video scsi software pc thanks vga
graphics help disk uni dos file ide controller work

Topic #2:
game team nhl games ca hockey players buffalo edu cc year play
university teams baseball columbia league player toronto

Topic #3:
window manager application mit motif size display widget program
xlib windows user color event information use events x11r5 values

Topic #4:
pitt gordon banks cs science pittsburgh univ computer soon disease
edu reply pain health david article medical medicine 16
"""

from time import time
from scikits.learn.feature_extraction import text
from scikits.learn import decomposition
from scikits.learn import datasets

n_samples = 1000
n_features = 1000
n_topics = 10
n_top_words = 20

# Load the 20 newsgroups dataset and vectorizer it using the most common word
# frequency with TF-IDF weighting (without top 5% stop words)

t0 = time()
print "Loading dataset and extracting TF-IDF features..."
dataset = datasets.fetch_20newsgroups(shuffle=True, random_state=1)

vectorizer = text.CountVectorizer(max_df=0.95, max_features=n_features)
counts = vectorizer.fit_transform(dataset.data[:n_samples])
tfidf = text.TfidfTransformer().fit_transform(counts)
print "done in %0.3fs." % (time() - t0)

# Convert scipy.sparse.csr_matrix representation to dense numpy array
tfidf = tfidf.toarray()

# Remove negative values (they should not be there, is this a bug?)
tfidf[tfidf < 0] = 0.0

# Fit the NMF model
print "Fitting the NMF model on with n_samples=%d and n_features=%d..." % (
    n_samples, n_features)
nmf = decomposition.NMF(n_components=n_topics).fit(tfidf)
print "done in %0.3fs." % (time() - t0)

# Inverse the vectorizer vocabulary to be able
inverse_vocabulary = dict((v, k) for k, v in vectorizer.vocabulary.iteritems())

for topic_idx, topic in enumerate(nmf.components_):
    print "Topic #%d:" % topic_idx
    print " ".join([inverse_vocabulary[i]
                    for i in topic.argsort()[:-n_top_words:-1]])
    print