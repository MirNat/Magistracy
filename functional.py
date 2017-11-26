import collections
import os
import unittest

# lab 3
def convert_value(value):
    if not isinstance(value, (int, long, float)):
        if value.startswith('0b'):
            value = int(value, 2)
        elif value.startswith('0o'):
            value = int(value, 8)
        elif value.startswith('0x'):
            value = int(value, 16)
        else:
            value = int(value)
    return value

def multiply_operator(value1, value2):
    return convert_value(value1) * convert_value(value2)

def scalar_product(iterable1, iterable2):
    try:
        return sum(map(multiply_operator, iterable1, iterable2))
    except valueError:
        return None

# lab 4
def flatten(iterable):
    for element in iterable:
        if isinstance(element, collections.Iterable) and not isinstance(element, basestring):
            for sub in flatten(element): # do recursively
                yield sub
        else:
            yield element
            
def dictionary_values(files_tree):
    items = set()
    for directory_name, directory_inner_element in files_tree.iteritems():
        if isinstance(directory_inner_element, dict):
            items.update(dictionary_values(directory_inner_element))
        else:
            items.update(directory_name + os.sep + filename for filename in directory_inner_element)
    return items

# lab 5
def walk_files(path):
    map = {}
    for root, sub_directories, files in os.walk(path):
        if root not in map:
            map[root] = []
        for file_name in files:
            map[root].append(file_name)
        for sub_directory in sub_directories:
            map[root].append(walk_files(root + os.sep + sub_directory))
    return map

print list(flatten(dictionary_values(walk_files('/bin'))))
