# Description: This code is a Python implementation of the fightin' words algorithm
# Original author: Monroe et al. (2008)
# Python implementation author: Jack Hessel

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer as CV
import string
from collections import defaultdict
exclude = set([i for i in string.punctuation if i not in ['-',"'"]]) 



def basic_sanitize(in_string):
    '''Returns a very roughly sanitized version of the input string.'''  
    in_string = ''.join([ch for ch in in_string if ch not in exclude])
    in_string = in_string.replace('\n', ' ').replace('\t', ' ')
    # replace 'll with will, 're with are, 've with have, 'd with would,
    in_string = in_string.replace("'ll", " will").replace("'re", " are").replace("'ve", " have").replace("'d", " would")
    # remove numbers
    in_string = ''.join([i for i in in_string if not i.isdigit() or int(i) > 1900])
    in_string = ' '.join(in_string.split())
    return in_string

def get_term_frequency(l, ngram = 1, stop_words = None):
    l = [basic_sanitize(l) for l in l]
    cv = CV(decode_error = 'ignore', ngram_range=(1,ngram),
            binary = False,
            max_features = 5000,
            stop_words = stop_words)
    counts_mat = cv.fit_transform(l).toarray()
    word_to_count = defaultdict(int)
    for word, index in cv.vocabulary_.items():
        word_to_count[word] = counts_mat[0, index]
    return word_to_count

def bayes_compare_language(l1, l2, ngram = 1, prior=.01, cv = None, stop_words = None):
    '''
    Arguments:
    - l1, l2; a list of strings from each language sample
    - ngram; an int describing up to what n gram you want to consider (1 is unigrams,
    2 is bigrams + unigrams, etc). Ignored if a custom CountVectorizer is passed.
    - prior; either a float describing a uniform prior, or a vector describing a prior
    over vocabulary items. If you're using a predefined vocabulary, make sure to specify that
    when you make your CountVectorizer object.
    - cv; a sklearn.feature_extraction.text.CountVectorizer object, if desired.

    Returns:
    - A list of length |Vocab| where each entry is a (n-gram, zscore) tuple.'''
    if cv is None and type(prior) is not float:
        print("If using a non-uniform prior:")
        print("Please also pass a count vectorizer with the vocabulary parameter set.")
        quit()
    l1 = [basic_sanitize(l) for l in l1]
    l2 = [basic_sanitize(l) for l in l2]
    if cv is None:
        cv = CV(decode_error = 'ignore', ngram_range=(1,ngram),
                binary = False,
                max_features = 5000,
                stop_words = stop_words)
    counts_mat = cv.fit_transform(l1+l2).toarray()
    # Now sum over languages...
    vocab_size = len(cv.vocabulary_)
    print("Vocab size is {}".format(vocab_size))
    if type(prior) is float:
        priors = np.array([prior for i in range(vocab_size)])
    else:
        priors = prior
    z_scores = np.empty(priors.shape[0])
    count_matrix = np.empty([2, vocab_size], dtype=np.float32)
    count_matrix[0, :] = np.sum(counts_mat[:len(l1), :], axis = 0)
    count_matrix[1, :] = np.sum(counts_mat[len(l1):, :], axis = 0)
    a0 = np.sum(priors)
    n1 = 1.*np.sum(count_matrix[0,:])
    n2 = 1.*np.sum(count_matrix[1,:])
    print("Comparing language...")
    for i in range(vocab_size):
        #compute delta
        term1 = np.log((count_matrix[0,i] + priors[i])/(n1 + a0 - count_matrix[0,i] - priors[i]))
        term2 = np.log((count_matrix[1,i] + priors[i])/(n2 + a0 - count_matrix[1,i] - priors[i]))        
        delta = term1 - term2
        #compute variance on delta
        var = 1./(count_matrix[0,i] + priors[i]) + 1./(count_matrix[1,i] + priors[i])
        #store final score
        z_scores[i] = delta/np.sqrt(var)
    index_to_term = {v:k for k,v in cv.vocabulary_.items()}
    sorted_indices = np.argsort(z_scores)
    return_list = []
    for i in sorted_indices:
        return_list.append((index_to_term[i], z_scores[i]))
    return return_list