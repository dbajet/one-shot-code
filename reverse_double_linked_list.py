from __future__ import annotations


class Node:
    def __init__(self, value):
        self.next_node = None
        self.previous_node = None
        self.value = value

    def print_it(self):
        current = self
        while current:
            from_value = '-'
            to_value = '-'
            if current.previous_node:
                from_value = current.previous_node.value
            if current.next_node:
                to_value = current.next_node.value
            print(from_value, ' -> ', current.value, ' -> ', to_value)
            current = current.next_node

    @staticmethod
    def switch_all(node: Node) -> Node:
        current = node
        previous = None
        while current:
            following = current.next_node
            current.next_node = previous
            previous = current
            current = following
        if not previous:
            return node

        node = previous
        current = previous
        following = None
        while current:
            previous = current.previous_node
            current.previous_node = following
            following = current
            current = previous
        return node


# create the list
root = Node(0)
tmp = root
for i in range(1, 10):
    tmp.next_node = Node(i)
    tmp.next_node.previous_node = tmp
    tmp = tmp.next_node
root.print_it()
print('*****')
raat = Node.switch_all(root)
raat.print_it()
