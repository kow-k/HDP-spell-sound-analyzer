## The following defs are wrong. You can't use cython.ATTR in
##
cpdef cy_gen_ngrams_X (S: cython.list, n: cython.int, check: cython.bint = False):
	"""
	take a string and returns the list of character n-grams generated out of it.
	"""
	##
	if check:
		print(f"#S: {S}; n: {n}")
	##
	if len(S) < n:
		return S
	## variables
	i:    cython.int
	seg:  cython.str
	b:    cython.str
	c:    cython.str
	segs: cython.list
	R:    cython.list
	g:    cython.list
	## main
	segs = [ seg for seg in S if len(seg) > 0 ]
	if check:
		print(f"#segs: {segs}")
	##
	R = [ ]
	for i in range(len(segs)):
		try:
			g = segs[ i : i + n ]
			if check:
				print(f"#g: {g}")
			if len(g) == n:
				R.append(g)
		except IndexError:
			pass
	## return
	return R
