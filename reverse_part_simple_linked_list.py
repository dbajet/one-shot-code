from __future__ import annotations


class Node:
    def __init__(self, value):
        self.next_node = None
        self.value = value

    def print_it(self):
        current = self
        while current:
            print(current.value)
            current = current.next_node

    def switch_all(self, node: Node) -> Node:
        current = node
        previous = None
        while current:
            following = current.next_node
            current.next_node = previous
            previous = current
            current = following
        return previous or node

    def switch_it(self, start: int, end: int) -> None:
        current = self

        for _ in range(start - 1):
            current = current.next_node

        sub_root_previous = current
        sub_root_start = current.next_node
        for _ in range(end - start):
            current = current.next_node
        sub_root_end = current.next_node
        current.next_node = None

        sub_root_previous.next_node = self.switch_all(sub_root_start)
        while sub_root_previous.next_node:
            sub_root_previous = sub_root_previous.next_node
        sub_root_previous.next_node = sub_root_end


# create the list
root = Node(-1)
tmp = root
for i in range(10):
    tmp.next_node = Node(i)
    tmp = tmp.next_node
root.print_it()
print('*****')
root.switch_it(2, 6)
root.print_it()
