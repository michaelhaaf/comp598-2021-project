#!/usr/bin/env python3

import pandas as pd
import json
import argparse
import string
import re
from collections import Counter


def load_stop_words():
    words = open("../data/stopwords.txt", "r").read().split("\n")
    r = re.compile(r'^#')
    return {word for word in words if not bool(r.match(word))}


TOPICS = ["topic1", "topic2", "etc."]
PUNCTUATION = '()[],-.?!;:#&'
MIN_COUNT = 5
STOP_WORDS = load_stop_words()  


def load_data(path):
    df = pd.read_csv(path, sep="\t")
    df['tweet'] = df['tweet'].str.lower() 
    return df 


def compile_word_counts(df): 
    return {topic: word_counts(df[df.topic == topic]) for topic in TOPICS}

    
def word_counts(df):
    word_counter = Counter()
    df['tweet'].apply(lambda tweet: word_counter.update(preprocess(tweet)))
    return {word: count for (word, count) in word_counter.items()}


def keep(word):
    return word.isalpha() and word not in STOP_WORDS


def preprocess(dialog):
    punctuation_table = str.maketrans(PUNCTUATION, ' ' * len(PUNCTUATION))
    return filter(keep, dialog.lower().translate(punctuation_table).split(' '))


# ensure each word has occurred at least MIN_COUNT times to be included in analysis 
def postprocess(preprocessed_counts):
    overall_counter = Counter()
    for topic_dict in preprocessed_counts.values():
        overall_counter += Counter(topic_dict) 
    words_to_remove = [word for word, count in overall_counter.items() if count < MIN_COUNT]

    return { topic: {word: count for (word, count) in topic_dict.items() if word not in words_to_remove} 
            for topic, topic_dict in preprocessed_counts.items() }
        

def main(args):
    # read input csv and preprocess topic names
    df = load_data(args.tweetFile)

    # make word counts for each topic
    counts = compile_word_counts(df)
    postprocessed_counts = postprocess(counts)

    out_file = open(args.outputFile, "w") 
    json.dump(postprocessed_counts, out_file, indent=4)
    out_file.close() 


# USAGE:
# python compile_word_counts.py -o <word_counts_json> -i <dialog_csv>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tweet word counter script')
    parser.add_argument('-o', 
                        dest='outputFile',
                        required=True,
                        help='output file name. Should be a .json file',
                        type=str
                        )
    parser.add_argument('-i',
                        dest='tweetFile',
                        required=True,
                        help='tweet file name. Should be a .tsv file',
                        type=str
                        )
    args = parser.parse_args()
    main(args)

