## generator fuctions for 2-gram, 3-gram
## developed by Kow Kuroda (kow.kuroda@gmail.com)
## 2024/02/20: added alises
## 2024/04/24: added gen_ngrams_from_str

def gen_ngrams_from_str (t: str, n: int, sep: str = r"", joint: str = "", check = False):
	'returns the list of character n-grams from a given string'
	import re
	segs = [ x for x in re.split(sep, t) if len(x) > 0 ]
	if check:
		print(segs)
	G = [ ]
	for i in range(len(segs)):
		try:
			b = segs[ i : i + n ]
			if check:
				print(b)
			c = joint.join(b)
			if check:
				print(c)
			if len(c) == n:
				G.append(c)
		except IndexError:
			pass
	return G

## functions applicable for string
def str_gen_unigrams (text: str, sep = r"", check = False):
	"""
	returns a list of unigrams from elements from a given string by splitting it by <sep>
	"""
	import re
	seg = [ x for x in re.split(sep, text) if len(x) > 0 ]
	return (seg)

## alises
str_gen1grams = str_gen_unigrams

def str_gen_bigrams (text: str, sep = r"", joint = "", check = False):
	"""
	returns a list of bigrams from elements from a given string by splitting it by <sep>
	"""
	import re
	n = 2
	if check:
		print(text)
	B = [ ]
	segs = [ seg for seg in re.split(sep, text) if len(seg) > 0 ]
	size = len(segs)
	if size < n:
		B.append(joint.join(segs))
	else:
		C = [ ]
		for i in range(size - n + 1):
			y = segs[ i : i + n ]
			if check:
				print(y)
			if len(y) == n:
				C.append(joint.join(y))
		B.append(C)
	#
	return (B[0]) # X[0] is in need. why?

## aliases
str_gen2grams = str_gen_bigrams
str_gen_2grams = str_gen_bigrams

## trigrams
def str_gen_trigrams (text: str, sep = r"", joint = "", check = False):
	import re
	n = 3
	T = [ ]
	if check:
		print(text)
	segs = [ seg for seg in re.split(sep, text) if len(seg) > 0 ]
	size = len(segs)
	if size < n:
		T.append(joint.join(segs))
	else:
		C = [ ]
		for i in range(size - n + 1):
			y = segs[ i : i + n ]
			if check:
				print(y)
			if len(y) == n:
				C.append(joint.join(y))
		T.append(C)
	return (T[0]) # X[0] is in need. why?

## aliases
str_gen3grams = str_gen_trigrams
str_gen_3grams = str_gen_trigrams

## functions applicable to list
def list_gen_ngrams (L: str, n: int, joint = "", check = False):
	"""
	returns a list of ngrams from elements from L from a given n
	"""
	if check:
		print(L)
	G = [ ]
	#segs = [ seg for seg in L if len(seg) > 0 ]
	segs = L
	size = len(segs)
	if size < n:
		G.append([joint.join(segs)])
	else:
		C = [ ]
		for i in range(size - n + 1):
			y = segs[ i : i + n ]
			if check:
				print(y)
			if len(y) == n:
				C.append(joint.join(y))
		G.append(C)
	#
	return (G[0]) # X[0] is in need. why?

## functions directly applicable to list
def bulk_gen_unigrams (L: list, sep = r"", check = False):
	"""
	returns the 1-gram of the items in list L with separator regex
	"""
	import re
	#U = [ list(filter(lambda x: len(x) > 0, y)) for y in [ re.split(sep, z) for z in L ] ]
	#U = [ y for y in [ re.split(sep, x) for x in L ] if len(y) > 0 ]
	U = [ ]
	for x in L:
		seg = [ y for y in re.split(sep, x) if len(y) > 0 ]
		if check:
			print(seg)
		U.append(seg)
	return (U)

## alises
bulk_gen1grams = bulk_gen_unigrams

## bigram
def bulk_gen_bigrams (L: list, sep = r"", joint = "", check = False):
	import re
	n = 2
	B = [ ]
	for x in L:
		if check:
			print(x)
		seg = [ s for s in re.split(sep, x) if len(s) > 0 ]
		size = len(seg)
		if size < n:
			B.append(joint.join(seg))
		else:
			C = [ ]
			for i in range(size - n + 1):
				y = seg[ i : i + n ]
				if check:
					print(y)
				if len(y) == n:
					C.append(joint.join(y))
			B.append(C)
	return (B)

## alises
bulk_gen2grams	= bulk_gen_bigrams
bulk_gen_2grams = bulk_gen_bigrams

### trigram
def bulk_gen_trigrams (L: list, sep = r"", joint = "", check = False):
	import re
	n = 3
	T = [ ]
	for x in L:
		if check:
			print(x)
		seg = [ s for s in re.split(sep, x) if len(s) > 0 ]
		size = len(seg)
		if size < n:
			T.append(joint.join(seg))
		else:
			C = [ ]
			for i in range(size - n + 1):
				y = seg[ i : i + n ]
				if check:
					print(y)
				if len(y) == n:
					C.append(joint.join(y))
			T.append(C)
	return (T)

## alises
bulk_gen3grams	= bulk_gen_trigrams
bulk_gen_3grams = bulk_gen_trigrams

### end of script
