# comp598-2021-project

## Usage
Detailed usage instructions are contained in the help menus for each script. Overall outline:

 To collect tweets, `collect_tweets.py` is invoked as follows:

`python src/collect_tweets.py -o <output_file>`

 It produces a JSON file containing 1000 tweets curated from a 3 day window using the tweepy API (twitter API v2, paginated). Note that in order to use this script, you will need a developer account with authentication to access this API, as well as .env environment variables containing your access credentials (so the scripts won't work out of the box, you need to set up your environment, but will work otherwise).

 To create .tsv files for manual annotation, `scripts/extract_to_tsv.py` is invoked with the following command:

`python scripts/extract_to_tsv.py -o <out_file> -i <json_file>`

 To collect a random 200 tweet sample for open coding, `scripts/sample_200_tweets.sh` is invoked as follows:

`scripts/sample_200_tweets.sh <tweet-json-file>` 

 The .json results are printed to stdout, which can be redirected to a .json file using a shell redirect

 Once manual annotation is complete, we can use `scripts/sanitize_annotations.sh` to automatically check that our coding and sentiment annotations do not have typos or noncompliant topics with those we defined. This script is invoked as follows:

 `scripts/sanitize_annotations.sh`

 Once manual annotation is verified, we can use `src/compile_word_counts.py` to produce our inital word frequency per topic .json counts file. This script also performs basic NLP preprocessing (stop word, punctuation, insignificant word removal):

`python src/compile_word_counts -o <word_counts_json> -i <annotated_by_topic_tsv>`

 Note that per the project requirements, *annotated_by_topic_tsv needs to include all 1000 tweets sampled, not just the 800 remaining after open coding*. In our experiment, we combined these .tsv files using standard shell tools (awk and cat). The resultant 1000 tweet file is contained in the data/analysis directory.

 Finally, we can compute the top 10 tf-idf words for each topic using the `compute_topic_top_n_tf-idf.py` script:

`python src/compute_topic_top_n_tf-idf.py -c <word_counts_json> -n 10`

 From here the .json results are printed to stdout, which can be redirected to a json file using a shell redirect.
