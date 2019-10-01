def non_unique(x):
	list_with_non_unique = []
	unique_elements = []
	for el in x:
		if x.count(el) == 1:
			unique_elements.append(el)
	for el in x:
		if el not in unique_elements:
			list_with_non_unique.append(el)
	return list_with_non_unique
