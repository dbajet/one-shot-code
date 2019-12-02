import time
from typing import Dict, List

# Find the unique items of a list of sorted items... better than O(n)

items = [1] * 107890 + [2] * 15880 + [3] * 127413 + [4] * 1012345 + [5] * 99988 + [6] * 99988 + [7] * 99988 + [9] * 99988


class DistinctCount:
    def __init__(self):
        self.iterations = 0

    def last_index_of(self, value, items: List, start: int, end: int) -> int:
        self.iterations += 1
        if value != items[start]:
            return -1
        if items[start] == items[end]:
            return end
        middle = start + int((end - start) / 2)
        right = self.last_index_of(value, items, middle + 1, end)
        if right != -1:
            return right
        return self.last_index_of(value, items, start, middle)

    def count_distinct(self, items: List) -> (Dict, int, int):
        last = len(items) - 1
        current = 0
        result: Dict = {}
        while current <= last:
            value = items[current]
            result[value] = current
            current = self.last_index_of(value, items, current, last) + 1
        return result, self.iterations, last


def count_unique(items: List) -> int:
    # the O(n) approach
    count = 1 if items else 0
    last = items[0] if items else None
    for i in items:
        if last != i:
            last = i
            count += 1
    return count


print('count of items', len(items))
time_start = time.monotonic()
print(DistinctCount().count_distinct(items))
print('time', time.monotonic() - time_start)

time_start = time.monotonic()
print(count_unique(items))
print('time', time.monotonic() - time_start)
