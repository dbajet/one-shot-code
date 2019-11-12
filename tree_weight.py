"""
A tree is defined in a list as 
       1
    |    \
  10      5
 /  \    /
1    0  6

compute the weight of the left and the right side, 
the weight being the sum of the values  (-1 means no value)
"""


def tree_weight(arr):
    level = 0
    right = 0
    left = 0
    start = 1
    length = len(arr) - 1

    while start < length:
        level += 1
        count = 2 ** (level - 1)
        for value in arr[start:start + count]:
            if value > -1:
                left += value
        for value in arr[start + count:start + 2 * count]:
            if value > -1:
                right += value
        start += 2 * count
    return left, right


arr = [1, 10, 5, 1, 0, 6]
left, right = tree_weight(arr)  # 11, 11
