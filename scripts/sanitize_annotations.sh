#!/bin/bash

## About 
# Quick shell script to double check typos/correctness of annotations. YMMV, this is a simple script

## Usage
# ./sanitize_annotations.sh <annotated .tsv file>

## Output
#   if there are no mistakes: "Annotations are well formed! Nothing to correct" to stdout
#   if there are: the line number followed by the mistake for each line to stdout


annot_file=$1
# Use awk to find columns which do not match our topic definitions exactly
coding_errors="$(awk -F '\t' '{print NR, $3}' "$annot_file" | grep -vE "(provaccine|antivaccine|neutral) (commentary|analysis)" | grep -vE "news|coding")"
sentiment_errors="$(awk -F '\t' '{print NR, $4}' "$annot_file" | grep -vE "(positive|negative|neutral)" | grep -vE "sentiment")"

[[ -z "$coding_errors" ]] && [[ -z "$sentiment_errors" ]] \
    && echo "Annotations are well formed! Nothing to correct" \
    || printf "%s\n%s" "$coding_errors" "$sentiment_errors" 
