import copy
import pprint

class MidSkipQueue(object):
    prettyPrinter = pprint.PrettyPrinter()

    def __init__(self, k, iterable=[]):
        if not isinstance(k, (int, long)) or k <= 0:
            raise ValueError("k must be positive integer value")
        self.k = k
        self.container = []

        for element in iterable:
            self.__append__(element)

    def __str__(self):
        return self.prettyPrinter.pformat(" ".join((str(s) for s in self.container)))

    def __eq__(self, other):
        return self.k == other.k and self.container == other.container

    def __len__(self):
        return len(self.container)

    def __getslice__(self, start, end):
        return self.container.__getslice__(start, end)

    def __getitem__(self, item):
        assert isinstance(item, (int, long))
        if item > 0:
            assert abs(item) < len(self)
        else:
            assert abs(item) < len(self) + 1

        return self.container[item]

    def __contains__(self, item):
        if self.container.__contains__(item):
            return True
        return False

    def index(self, element):
        if self.container.__contains__(element):
            return self.container.index(element)
        return -1

    def __iadd__(self, iterable):
        return self + iterable

    def __add__(self, iterable):
        msq = copy.deepcopy(self)
        for element in iterable:
            msq.__append__(element)
        return msq

    def __append__(self, element):
        if len(self.container) == 2 * self.k:
            del self.container[self.k]
        self.container.append(element)

    def append(self, *arg):
        for element in arg:
            self.__append__(element)



class MidSkipPriorityQueue(MidSkipQueue):
    def __init__(self, k, iterable=[]):
        super(MidSkipPriorityQueue, self).__init__(k, iterable)
        self.k = k
        self.container = []

        elements = sorted(iterable)
        for element in elements[0: min(len(elements), self.k)]:
            self.__append__(element)

        if len(elements) > self.k:
            for element in elements[(len(elements) - self.k) * -1:]:
                self.__append__(element)

    def __append__(self, element):
        if len(self.container) == 2 * self.k:
            if element < min(self.container[0: self.k]):
                self.container[self.k - 1] = element
            else:
                min_second_part_element = min(self.container[self.k: 2 * self.k])
                min_second_part_element_index = self.k + self.container[self.k: 2 * self.k].index(min_second_part_element)
                self.container[min_second_part_element_index] = element
        else:
            self.container.append(element)

    def __iadd__(self, iterable):
        return self + iterable

    def __add__(self, iterable):
        return MidSkipPriorityQueue(self.k, self.container + list(iterable))
