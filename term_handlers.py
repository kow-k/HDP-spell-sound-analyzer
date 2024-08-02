#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
def get_overlap(s1: str, s2: str):
	# Find the longest overlap
	max_overlap = min(len(s1), len(s2))
	overlap = 0
	for i in range(1, max_overlap + 1):
		if s1[-i: ] == s2[ :i]:
			overlap = i
	return overlap

#
def merge_with_overlap(s1: str, s2: str, min_overlap, check: bool = False):
	#
	overlap = get_overlap(s1, s2)
	if check:
		print(f"#overlap: {overlap}")
	# Merge the strings based on the overlap
	if overlap >= min_overlap:
		merged_string = s1 + s2[overlap: ]
		return merged_string
	else:
		None

#
def merge_with_overlap_under_gap(s1: str, s2: str, min_overlap, gap_marker: str, check: bool = False):
	#
	# Find the longest overlap
	max_overlap = min(len(s1), len(s2))
	overlap = 0
	for i in range(1, max_overlap + 1):
		#if s1[-i: ] == s2[ :i]:
		s1_raw = list(s1[-i: ])
		s2_raw = list(s2[ :i])
		assert len(s1_raw) == len(s2_raw)
		shared = [ ]
		for j in range(len(s1_raw)):
			if s1_raw[j] == s2_raw[j]:
				shared.append(s1_raw[j])
			elif s1_raw[j] == gap_marker:
				shared.append(s1_raw[j])
			elif s2_raw[j] == gap_marker:
				shared.append(s2_raw[j])
			else:
				shared.append(None)
			overlap = i
	if check:
		print(f"#overlap: {overlap}")
	shared = [ x for x in shared if not x == None ]
	if check:
		print(f"#shared: {shared}")
	# Merge the strings based on the overlap
	if overlap >= min_overlap:
		#merged_string = s1 + s2[overlap: ]
		if len(shared) == overlap:
			merged_string = "".join(shared)
			return merged_string
	else:
		None

#
def reduce_by_superposition(L: list, min_overlap, check: bool = False):
	"""
	given a list of strings, perform a pairwise merge by superposition and returns the result
	"""
	reduced = [ ]
	processed = [ ]
	for x in L:
		processed.append(x)
		unprocessed = [ z for z in L if not z in processed ]
		for y in unprocessed:
			merged = merge_with_overlap(x, y, min_overlap, check = check)
			if check:
				print(f"#merged: {merged}")
			if merged:
				reduced.append(merged)
	return reduced

def reduce_by_superposition_under_gap(L: list, min_overlap, gap_marker: str = "…", check: bool = False):
	"""
	given a list of strings with gaps, perform a pairwise merge by superposition and returns the result
	"""
	reduced = [ ]
	processed = [ ]
	for x in L:
		processed.append(x)
		unprocessed = [ z for z in L if not z in processed ]
		for y in unprocessed:
			merged = merge_with_overlap_under_gap(x, y, min_overlap, gap_marker, check = check)
			if check:
				print(f"#merged: {merged}")
			if merged:
				reduced.append(merged)
	return reduced

# Example usage
if __name__ == "__main__":
	s1 = "abc"
	s2 = "bcde"
	s3 = "cde"
	s4 = "def"
	print(merge_with_overlap(s1, s2))
	print(merge_with_overlap(s1, s3))
	print(merge_with_overlap(s1, s4))
