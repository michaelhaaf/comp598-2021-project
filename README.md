# comp598-2021-project

## Usage
Detailed usage instructions are contained in the help menus for each script. Overall outline:

 To collect tweets, `collect_tweets.py` is invoked as follows:

`python src/collect_tweets.py -o <output_file>`

 It produces a JSON file containing 1000 tweets curated from a 3 day window using the tweepy API (twitter API v2, paginated). 

 To create .tsv files for manual annotation, `scripts/extract_to_tsv.py` is invoked with the following command:

`python scripts/extract_to_tsv.py -o <out_file> -i <json_file>`

 To collect a random 200 tweet sample for open coding, `scripts/sample_200_tweets.sh` is invoked as follows:

`scripts/sample_200_tweets.sh <tweet-json-file>` 

 The .json results are printed to stdout, which can be redirected to a .json file using a shell redirect

 Once manual annotation is complete, we can use `compile_word_counts.py` to produce our inital word frequency per topic .json counts file. This script also performs basic NLP preprocessing (stop word, punctuation, insignificant word removal):

`python src/compile_word_counts -o <word_counts_json> -i <annotated_by_topic_tsv>`

 Finally, we can compute the top 10 tf-idf words for each topic using the `compute_topic_top_n_tf-idf.py` script:

`python src/compute_topic_top_n_tf-idf.py -c <word_counts_json> -n 10`

 From here the .json results are printed to stdout, which can be redirected to a json file using a shell redirect.
