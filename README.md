# HDP spell-sound analysis

Data and scripts for analysis used for "Exploring structures of English sound and spelling using HDP" presented in JCSS41/2024

## Data
Text files

### Data
1. [English spell/sound pairs (.csv)](data/open-dict-ipa/data1/en_US.csv)

## Scripts for data analysis
Scripts for analysis (Jupyter notebooks)

2. [HDP analyzer (Jupyter notebook)](HDP-spell-sound-analyzer.ipynb)

Running was confirmed on Python 3.9, 3.10, and 3.11.

Important Parameters:

0. **source_sampling** [boolean]: a flag to perform sampling
1. **term_class** [string]: either "spell" or "sound"
2. **max_doc_size** [integer]: maximum character length for docs to process
3. **min_doc_size** [integer]: minimum character length for docs to process
4. **ngram_is_inclusive** [boolean]: a flag for making ngrams inclusive
5. **apply_term_filtering** [boolean]: 
7. **term_minfreq** [integer]: a filter against too infrequent terms (valued for gensim's "minfreq")
8. **term_abuse_threshold** [float: 0~1.0]: a filter against too frequent terms (valued for gensim's "abuse_theshold")

Other paramers used are not recommended to modify. Do so at your own risk.

## Prerequisites
Needed Python packages

1. pyLDAvis [recommended to install first of all]

## Results
