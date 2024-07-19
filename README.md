# HDP spell-sound (association) analysis

Data and scripts for analysis used for "Unsupervised extraction of sound and spelling patterns for English words using HDP" to be presented in JCSS41/2024

# Data

## English

1. [English spell/sound pairs (.csv) from open-dict-ipa](data/open-dict-ipa/data1/en_US.csv.gz)
2. [English noun spell/sound pairs (.csv) from wn3 x open-dict-ipa](data/wn3/en_N_only.csv)
3. [English verb spell/sound pairs (.csv) from wn3 x open-dict-ipa](data/wn3/en_V_only.csv)
4. [English adjective spell/sound pairs (.csv) from wn3 x open-dict-ipa](data/wn3/en_A_only.csv)
5. [English adverb spell/sound pairs (.csv) from wn3 x open-dict-ipa](data/wn3/en_R_only.csv)
6. [English noun spells (.csv) from wn3](data/wn3/en_N_only.csv)
7. [English verb spells (.csv) from wn3](data/wn3/en_V_only.csv)
8. [English adjective spells (.csv) from wn3](data/wn3/en_A_only.csv)
9. [English adverb spells (.csv) from wn3](data/wn3/en_R_only.csv)

Data 6, 7, 8 and 9 are class-wise extractions from [WordNet 3](http://wordnet.princeton.edu/).

Data 2, 3, 4 and 5 are the reduced/filtered versions of data 6, 7, 8 and 9, whereby spells are paired with IPA symbols in open-dict-ipa [en_US.csv](data/open-dict-ipa/data1/en_US.csv.gz).

The "data1" directory is a copy of the directory of the same name provided at [open-dict-ipa](https://github.com/open-dict-data/ipa-dict).

## German

1. [German words](data/open-dict-ipa/data1/de.csv.gz)
2. [German nouns](data/open-dict-ipa/data1a/de_N_only.csv.gz)
3. [German non-nouns](data/open-dict-ipa/data1a/de_non_N_only.csv.gz)

The classfication between nouns and non-nouns is made (too) simply in that nouns are those words that start with a capital letter and non-nouns are those that do not, without using any lexcial resources.

# Scripts for data analysis

Scripts for analysis. One for word-level analysis. Another for sentence-level analysis.

1. [HDP spell-sound analyzer (Jupyter notebook)](HDP-spell-sound-analyzer.ipynb)
2. [HDP text analyzer (Jupyter notebook)](HDP-text-analyzer.ipynb)
3. [HDP spell-sound association analyzer (Jupyter notebook)](HDP-spell-sound-association-analyzer.ipynb)

Running was confirmed on Python 3.9, 3.10, and 3.11.

## Important Parameters:

0. **target_lang_key** [string]: a selector for target language name
1. **term_class** [string]: either "spell" or "sound"
2. **source_sampling** [boolean]: a flag to perform sampling
3. **max_doc_size** [integer]: maximum character length for docs to process
4. **min_doc_size** [integer]: minimum character length for docs to process
5. **ngram_is_inclusive** [boolean]: a flag for making ngrams inclusive
6. **apply_term_filtering** [boolean]: 
7. **term_minfreq** [integer]: a filter against too infrequent terms (valued for gensim's "minfreq")
8. **term_abuse_threshold** [float: 0~1.0]: a filter against too frequent terms (valued for gensim's "abuse_theshold")

Other paramers used are not recommended to modify. Do so at your own risk.

## Prerequisites
Needed Python packages

1. pyLDAvis [recommended to install first of all]

# Results
