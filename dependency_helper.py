import copy

class DependencyHelper(object):
    def __init__(self):
        self.container = {}

    def add(self, from_element, to_element):
        if self.container.__contains__(from_element):
            self.container[from_element].append(to_element)
        else:
            self.container[from_element] = [to_element]

    def __add__(self, other):
        dh = copy.deepcopy(self)
        dh.add(other[0], other[1])
        return dh

    def __iadd__(self, other):
        self.add(other[0], other[1])
        return self

    def remove(self, removable_element):
        self.container[removable_element[0]].remove(removable_element[1])

    def __sub__(self, other):
        dh = copy.deepcopy(self)
        dh.remove(other)
        return dh

    def __isub__(self, other):
        self.remove(other)
        return self

    def copy(self):
        return copy.deepcopy(self)

    def get_dependent(self, element):
        return self.container[element]

    def __dfs(self, vertex, visited):
        visited[vertex] = 1
        if self.container.__contains__(vertex):
            for neighbor in self.container[vertex]:
                if not visited.__contains__(neighbor):
                    if self.__dfs(neighbor, visited):
                        return True
                elif visited[neighbor] == 1:
                    return True
        visited[vertex] = 2
        return False

    def has_dependencies(self):
        visited = {}
        for key in self.container.keys():
            if self.__dfs(key, visited):
                return True
        return False

    def __bool__(self):
        return self.has_dependencies()

    def __nonzero__(self):
        return self.has_dependencies()
