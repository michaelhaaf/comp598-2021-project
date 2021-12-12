import os, sys
import argparse
import json
import math


def idf(word, topic_counts):
    topics_that_used_word_count = sum([1 for topic in topic_counts if word in topic_counts[topic]])
    return math.log10( len(topic_counts.keys()) / topics_that_used_word_count )


def top_n_tf_idf(topic, topic_counts, n):
    tf_idf_scores = { word: count * idf(word, topic_counts) for word, count in topic_counts[topic].items() }
    return sorted(tf_idf_scores, key=tf_idf_scores.get, reverse=True)[0:n]


def compute_topic_top_n_tf_idf(topic_counts, num_words): 
    return {topic: top_n_tf_idf(topic, topic_counts, num_words) for topic in topic_counts.keys()}


def main(args):
    in_file = open(args.topic_counts, "r")
    topic_counts = json.load(in_file)
    in_file.close()

    results = compute_topic_top_n_tf_idf(topic_counts, args.num_words)

    print(json.dumps(results, indent=4))


# USAGE:
# python compute_topic_top_n_tf_id.py -c <word_counts_json> -n <num_words>
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='compute top N tf-idf words per topic')
    parser.add_argument('-c', 
                        dest='topic_counts',
                        required=True,
                        help='input file name. Should be a .json with word count dicts for each topic',
                        type=str
                        )
    parser.add_argument('-n',
                        dest='num_words',
                        required=True,
                        help='the top n words to report tf-idf for each topic',
                        type=int
                        )
    args = parser.parse_args()
    main(args)

