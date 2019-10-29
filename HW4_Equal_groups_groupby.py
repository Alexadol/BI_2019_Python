# version using itertools module
import itertools


def equal_groups(data):
    final = []
    for elem, group in itertools.groupby(data):
        final.append(list(group))
    return final
