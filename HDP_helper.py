## https://stackoverflow.com/questions/31543542/hierarchical-dirichlet-process-gensim-topic-number-independent-of-corpus-size

import pandas as pd

def extract_topic_probs (gensim_hdp, t = 20, w = 25, isSorted = True, check = False):
	"""
	Input the gensim model to get the rough topics' probabilities
	"""
	shown_topics = gensim_hdp.show_topics (num_topics = t, num_words = w, formatted = False)
	if check:
		print(shown_topics)
	topics_nos = [ x[0] for x in shown_topics ]
	weights = [ sum([item[1] for item in shown_topics[topicN][1]]) for topicN in topics_nos ]
	if ( isSorted ):
		return pd.DataFrame({'topic_id' : topics_nos, 'weight' : weights}).sort_values(by = "weight", ascending = False);
	else:
		return pd.DataFrame({'topic_id' : topics_nos, 'weight' : weights});

#
def reformat_topic (t: str, topn = 10):
	"given t as gensim.hdp.print_topic, returns topn terms with highest probabilities"
	X = [ x.strip() for x in t.split("+") ]
	Y = [ x.split("*") for x in X ]
	E = [ (float(y[0]), y[1].strip('"')) for y in Y ]
	E = sorted(E, key = lambda x: x[0], reverse = True)
	return " + ".join([ f"{x[0]} * {x[1]}" for x in E[:topn] ])

### end of script