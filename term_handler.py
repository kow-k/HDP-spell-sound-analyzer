# -*- coding: utf-8 -*-
## implementation of term superposition generated by HDP-based term extraction
## developed by Kow Kuroda (kow.kuroda@gmail.com)
## created 2024/08/04
## modified 2024/08/09
## 2024/08/10: separated list_superpose() and made externally accessible

## imports
import numpy as np
import re
#import string2string.alignment

##
def derive_terms_by_superposition(T: list, align_globally: bool = True, expansive: bool = True, greedy: bool = True, gap_mark: str = "…", with_score_matrix: bool = False, base_is_min: bool = True, check: bool = False, **params_dict):
	"""
	returns a list of terms derived by pairwise superpostion over a given list T of terms.
	"""
	remains = T.copy()
	O = [ ]
	while len(remains) > 0:
		seen = [ ]
		for one in remains:
			seen.append(one)
			unseen = [ x for x in remains if not x in seen ]
			for another in unseen:
				if another != one:
					if align_globally:
						superposed = NW_superpose(one, another,
										gap_char = gap_mark, with_score_matrix = with_score_matrix,
										base_is_min = base_is_min, greedy = greedy, check = check, **params_dict)
					else:
						superposed = SW_superpose(one, another,
										gap_char = gap_mark, with_score_matrix = with_score_matrix,
										base_is_min = base_is_min, greedy = greedy, check = check, **params_dict)
					## evaluate result
					if superposed == None or len(superposed) == 0:
						pass
					else:
						if not superposed in O:
							O.append(superposed)
						if not superposed in remains:
							if expansive:
								for loc in [ m.start() for m in re.finditer(gap_mark, superposed) ]:
									if check:
										print(f"superposed: {superposed}")
									if 0 < loc and loc < (len(superposed) - 1): # Crucially (end -1)
										ex1 = superposed[:loc]
										if check:
											print(f"exp1: {ex1}")
										ex2 = superposed[loc+1:]
										if check:
											print(f"exp2: {ex2}")
										ex = ex1 + ex2
										if check:
											print(f"added: {ex}")
										if len(ex) > 0 and not ex in remains:
											remains.append(ex)
							else:
								remains.append(superposed)
			## take out the processed one
			remains.remove(one)
	## return result
	return O

## string2string based
def NW_superpose(s: list, t: list, gap_char = "-", with_score_matrix: bool = False, base_is_min: bool = True, greedy: bool = False, check = False, **params):
	"""
	perform global alignment of a pair of sequence lists using
	Needleman-Wunsch method and return their superposition.
	"""
	##
	from string2string.alignment import NeedlemanWunsch
	nw = NeedlemanWunsch(
		##gap_weight = -0, mismatch_weight = -2, match_weight = 2, # refrence values
		gap_weight = params['gap_weight'],
		match_weight = params['match_weight'],
		mismatch_weight = params['mismatch_weight'],
		gap_char = gap_char)
	#
	s_aligned, t_aligned, score_matrix = nw.get_alignment(s, t, return_score_matrix = True)
	## set base
	if base_is_min:
		size = min(len(s), len(t))
		score = np.sum(score_matrix)/size
	else:
		size = max(len(s), len(t))
		score = np.sum(score_matrix)/size
	## filter by score
	outcome = [ ]
	if score >= params['theta']:
		if check:
			nw.print_alignment(s_aligned, t_aligned)
			print(f"score:{score}")
		if check and with_score_matrix:
			print(score_matrix)
		superposed = aligned2superpose(s_aligned, t_aligned, align_sep = "|", greedy = greedy, check = False)
		if check:
			print(f"superposed: {superposed}")
		outcome = superposed
	else:
		outcome = None
	## return result
	return outcome

##
def SW_superpose(s: list, t: list, gap_char: str = "-", with_score_matrix: bool = False, base_is_min: bool = True, greedy: bool = False, check: bool = False, **params):
	"""
	perform local alignment of a pair of sequences using Needleman-Wunsch method
	and return their superpostion.
	"""
	from string2string.alignment import SmithWaterman
	sw = SmithWaterman(
		##gap_weight = -0, match_weight = 2, mismatch_weight = -2, # reference values
		gap_weight = params['gap_weight'],
		match_weight = params['match_weight'],
		mismatch_weight = params['mismatch_weight'],
		gap_char = gap_char)
	#
	s_aligned, t_aligned, score_matrix = sw.get_alignment(s, t, return_score_matrix = True)
	## set score
	if base_is_min:
		size = min(len(s), len(t))
		score = np.sum(score_matrix)/size
	else:
		size = max(len(s), len(t))
		score = np.sum(score_matrix)/size
	## filter by score
	outcome = [ ]
	if score >= params['theta']:
		if check:
			sw.print_alignment(s_aligned, t_aligned)
			print(f"score:{score}")
		if check and with_score_matrix:
				print(score_matrix)
		superposed = aligned2superpose(s_aligned, t_aligned, align_sep = "|", greedy = greedy, check = False)
		if check:
			print(f"superposed: {superposed}")
		outcome = superposed
	else:
		outcome = None
	## return result
	return outcome

## convertor of alignment string to superposed string
def aligned2superpose(s: str, t: str, align_sep: str = "|", joint: str = "",
	unit_sep: str = ",", greedy: bool = False, mismatch_mark: str = "?", check: bool = False):
	"""
	convert string2string encoding for alignment to superposition.
	"""
	s_split = [ x for x in re.split(f"\s*{align_sep}\s*", s) if len(x) > 0 and x != align_sep ]
	t_split = [ x for x in re.split(f"\s*{align_sep}\s*", t) if len(x) > 0 and x != align_sep ]
	if check:
		print(f"s_split: {s_split}")
		print(f"t_split: {t_split}")
	assert len(s_split) == len(t_split)
	## main
	list_superposed = list_superpose(s_split, t_split, check = check)
	##
	str_superposed = ""
	for i, unit in enumerate(list_superposed):
		if check:
			print(f"unit {i}: {unit}")
		if len(unit) == 1:
			str_superposed = str_superposed + unit[0]
		else:
			if not greedy: # This acts like output-filter to mask mismatches
				str_superposed = str_superposed + mismatch_mark
			else:
				u = [ x for subunit in unit for x in subunit ] # Queer notation!
				str_superposed = str_superposed + f"[{unit_sep.join(u)}]"
	##
	return str_superposed

##
def list_superpose(X: list, Y: list, gap_mark: str = "…", check: bool = False):
	"""
	takes two lists of the same length and returns their superposition, i.e., unit-wise merger.
	"""
	assert len(X) == len(Y)
	S = [ ]
	for pair in zip(X, Y):
		x = pair[0]; y = pair[1]
		try: # acceptable cases
			assert len(x) > 0 and len(x) > 0
			if x == y:
				S.append([x])
			elif x == gap_mark:
				if len(y) > 1:
					S.append(y)
				else:
					S.append([y])
			elif y == gap_mark:
				if len(x) > 1:
					S.append(x)
				else:
					S.append([x])
			else: ## handles mismatch case
				z = sorted(list(set([ *x, *y ])))
				z = [ x for x in z if len(x) > 0 and x != "["  and x != "]" and x != "," ]
				z = [ a for b in z for a in b ]
				#print(z)
				S.append(z)
		except AssertionError: # unacceptable cases
			S.append([])
	## return result
	return S

### end of script