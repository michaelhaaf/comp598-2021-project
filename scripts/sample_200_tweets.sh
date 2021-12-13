#!/bin/bash
# Usage: ./sample_200_tweets.sh <tweet-json-file>

# this script makes a lot of assumptions about the structure of the json file
# Removes the first and last json braces, as well as the comma-less last line. Shuffles then selects 200. Adds json braces again, then prints to stdout

input=$1
cat "$input" | sed '1,1d' | sed '$d' | sed '$d' | shuf -n 200 | sed '$s/,$//' | cat <(echo "{") - <(echo "}") 
