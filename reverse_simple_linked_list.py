class Node:
    def __init__(self, data: int, point_to: 'Node'):
        self.data = data
        self.point_to = point_to

    @staticmethod
    def print_it(head: 'Node'):
        while head:
            print(head.data)
            head = head.point_to
        print('\n')

    @staticmethod
    def reverse(head: 'Node') -> 'Node':
        if head.point_to is None:
            return head
        current = head
        previous = None
        while current.point_to:
            future = current.point_to
            current.point_to = previous
            previous = current
            current = future
        current.point_to = previous
        return current


node = Node(6, None)
for i in range(5, 0, -1):
    node = Node(i, node)

Node.print_it(node)
node = Node.reverse(node)
Node.print_it(node)
node = Node.reverse(node)
Node.print_it(node)
