import itertools


# lab 2
def transpose(iterable):
    return list(itertools.izip_longest(*iterable))


# lab 1
def unique(iterable):
    visited = set()
    for element in iterable:
        if element not in visited:
            yield element
            visited.add(element)