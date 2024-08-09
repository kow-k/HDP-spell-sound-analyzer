# -*- coding: utf-8 -*-

## implementation of term superposition
## developed by Kow Kuroda (kow.kuroda@gmail.com)
## created 2024/08/04
## modified 2024/08/09

## imports
import numpy as np
import re
#import string2string.alignment

## string2string based
def NW_superpose(s: list, t: list, gap_char = "-", with_score_matrix = False, base_is_min = True, check = False, **params):
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
		superposed = align2superpose(s_aligned, t_aligned, gap_mark = gap_char, check = False)
		if check:
			print(f"superposed: {superposed}")
		outcome = superposed
	else:
		outcome = None
	## return result
	return outcome
#
def str_NW_superpose(s: str, t: str, gap_char = "-", with_score_matrix = False, base_is_min = True, check = False, **params):
	"""
	perform global alignment of a pair of sequences as strings using
	Needleman-Wunsch method and return their superposition.
	"""
	outcome = [ ]
	from string2string.alignment import NeedlemanWunsch
	nw = NeedlemanWunsch(
		##gap_weight = -0, mismatch_weight = -2, match_weight = 2, # reference values
		gap_weight = params['gap_weight'],
		match_weight = params['match_weight'],
		mismatch_weight = params['mismatch_weight'],
		gap_char = gap_char)
	#
	s_aligned, t_aligned, score_matrix = nw.get_alignment(s, t, return_score_matrix = True)
	#
	if base_is_min:
		size = min(len(s), len(t))
		score = np.sum(score_matrix)/size
	else:
		size = max(len(s), len(t))
		score = np.sum(score_matrix)/size
	#
	if score >= params['theta']:
		if check:
			nw.print_alignment(s_aligned, t_aligned)
			print(f"score:{score}")
		if check and with_score_matrix:
			print(score_matrix)
		#
		superposed = align2superpose(s_aligned, t_aligned, gap_mark = gap_char, check = False)
		if check:
			print(f"superposed: {superposed}")
		outcome = superposed
	else:
		outcome = None
	## return result
	return outcome
##
def SW_superpose(s: list, t: list, gap_char: str = "-", with_score_matrix: bool = False, base_is_min: bool = True, check: bool = False, **params):
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
		superposed = align2superpose(s_aligned, t_aligned, gap_mark = gap_char, check = False)
		if check:
			print(f"superposed: {superposed}")
		outcome = superposed
	else:
		outcome = None
	## return result
	return outcome

## convertor of alignment string to superposed string
def align2superpose(s_raw: str, t_raw: str, sep: str = "|", joint: str = "",
	gap_mark: str = "…", reduce: bool = True, greedy: bool = False, check: bool = False):
	"""
	convert string2string encoding for alignment to superposition.
	"""
	s_split = [ x for x in re.split(f"\s*{sep}\s*", s_raw) if len(x) > 0 and x != sep ]
	t_split = [ x for x in re.split(f"\s*{sep}\s*", t_raw) if len(x) > 0 and x != sep ]
	if check:
		print(f"s_split: {s_split}")
		print(f"t_split: {t_split}")
	assert len(s_split) == len(t_split)
	## main
	S = [ ]
	for pair in zip(s_split, t_split):
		x = pair[0]; y = pair[1]
		if x == y:
			S.append(x)
		elif x == gap_mark:
			S.append(y)
		elif y == gap_mark:
			S.append(x)
		else:
			## handles mismatch case
			if greedy:
				S.append(f"[{x},{y}]")
			else:
				return None
	result = joint.join(S)
	if reduce:
		result = re.sub(f"{gap_mark}+", f"{gap_mark}", result)
	## return result
	return result
##
def derive_terms_by_superposition(T: list, align_globally: bool = True, expansive = True, gap_mark: str = "…", with_score_matrix: bool = False, base_is_min: bool = True, check: bool = False, **params_dict):
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
										gap_char = gap_mark, with_score_matrix = False,
										base_is_min = False, check = check, **params_dict)
					else:
						superposed = SW_superpose(one, another,
										gap_char = gap_mark, with_score_matrix = False,
										base_is_min = False, check = check, **params_dict)
					## evaluate result
					if superposed == None:
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
											print(f"ex2: {ex2}")
										ex = ex1 + ex2
										if check:
											print(f"added: {ex}")
										if ex not in remains:
											remains.append(ex)
			## take out the processed one
			remains.remove(one)
	## return result
	return O

### end of script