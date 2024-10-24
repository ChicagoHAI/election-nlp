import csv
import os 
import pandas as pd
from pathlib import Path
import spacy
from utils import load_file
from fightin_words_utils import bayes_compare_language, get_term_frequency

nlp = spacy.load("en_core_web_sm")

def filter_by_pos(text,pos):
    doc = nlp(text,disable=['ner'])
    pos_map = {}
    pos_map['noun'] = ['NOUN','PROPN']
    pos_map['verb'] = ['VERB']
    pos_map['adjective'] = ['ADJ']
    filtered_list = [token.lemma_ for token in doc if token.pos_ in pos_map[pos]]
    return ' '.join(filtered_list) 



# Temporary convenience function to load all corpora
def load_all_corpora():
    corpus = {}
    for year in ['2016','2020','2024']:
        for party in ['democrat','republican']:
            filename = f'../data/party_platforms/federal/{party}/{year}.txt'
            if os.path.exists(filename):
                corpus[f'{party}_{year}'] = load_file(filename)
        for candidate in ['trump','harris']:
            filename = f'../data/candidate_positions/president/{candidate}/{year}.txt'
            if os.path.exists(filename):
                corpus[f'{candidate}_{year}'] = load_file(filename)
    return corpus

def run_log_odds(corpus1,corpus2,corpus_name1,corpus_name2,ngram=1,stop_words=None):
    log_odds = bayes_compare_language(corpus1,corpus2,ngram=ngram,prior=.05,stop_words=stop_words)
    word_to_count1 = get_term_frequency(corpus1,ngram=ngram,stop_words=stop_words)
    word_to_count2 = get_term_frequency(corpus2,ngram=ngram,stop_words=stop_words)
    results = pd.DataFrame(log_odds,columns=['term','log_odds'])
    results['corpus 1'] = corpus_name1
    results['corpus 2'] = corpus_name2
    results['count 1'] = results['term'].apply(lambda x: word_to_count1[x])
    results['count 2'] = results['term'].apply(lambda x: word_to_count2[x])
    return results
       
def main():
    
    corpus = load_all_corpora()
    corpus_pairs = [('democrat_2024','democrat_2020'),('republican_2024','republican_2016'),
                    ('trump_2024','trump_2016'),('harris_2024','harris_2020'),
                    ('harris_2024','trump_2024'),('democrat_2024','republican_2024')]
    # for corpus_pair in corpus_pairs:
    #     corpus_name1,corpus_name2 = corpus_pair
    #     for ngram in [1,2]:
    #         for stop_words in [None,'english']:
    #             out_dir = f'../results/log_odds/platforms/ngram_{ngram}/stopwords_{str(stop_words)}'
    #             Path(out_dir).mkdir(parents=True,exist_ok=True)
    #             corpus1 = [corpus[corpus_name1]]
    #             corpus2 = [corpus[corpus_name2]]
    #             results = run_log_odds(corpus1,corpus2,corpus_name1,corpus_name2,ngram=ngram,stop_words=stop_words)
    #             out_file = f'{out_dir}/{corpus_name1}_{corpus_name2}.csv'
    #             results.to_csv(out_file,index=False)

    for corpus_pair in corpus_pairs:
        corpus_name1,corpus_name2 = corpus_pair
        for pos in ['noun','verb','adjective']:
            corpus1 = [filter_by_pos(corpus[corpus_name1],pos)]
            corpus2 = [filter_by_pos(corpus[corpus_name2],pos)]
            out_dir = f'../results/log_odds/platforms/{pos}'
            Path(out_dir).mkdir(parents=True,exist_ok=True)
            results = run_log_odds(corpus1,corpus2,corpus_name1,corpus_name2,ngram=1,stop_words=None)
            out_file = f'{out_dir}/{corpus_name1}_{corpus_name2}.csv'
            results.to_csv(out_file,index=False)
            

        
            

if __name__ == "__main__":
    main()