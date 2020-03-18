def NestedDictValues(d):
	for v in d.values():
		if isinstance(v, dict):
			yield from NestedDictValues(v)
		else:
			yield v