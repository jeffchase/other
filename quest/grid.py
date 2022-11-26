import math

class KPoint(tuple):
    def __add__(self, o):
        return KPoint([a + b for a, b in zip(self, o)])
    def __sub__(self, o):
        return KPoint([a - b for a, b in zip(self, o)])
    def __mul__(self, o):
        return KPoint([a * b for a, b in zip(self, o)])
    def __neg__(self):
        return KPoint([-a for a in self])
    def __abs__(self):
        return math.sqrt(sum([x**2 for x in self]))
    def dist(self, o):
        return abs(self - o)

class KTreeNode:
    def __init__(self, point, value):
        if not isinstance(point, KPoint):
            point = KPoint(point)
        self.value = value
        self.point = point
        self.left = None
        self.right = None

    def __str__(self):
        return f'{self.value} @ {self.point}'

class KTree:
    def __init__(self, dim):
        self.head = None
        self.dim = dim

    def insert(self, p, v):
        assert len(p) == self.dim

        def _insert(current, node, depth):
            if not current:
                return node

            axis = depth % self.dim
            if node.point[axis] < current.point[axis]:
                current.left = _insert(current.left, node, depth + 1)
            else:
                current.right = _insert(current.right, node, depth + 1)

            return current

        self.head = _insert(self.head, KTreeNode(p, v), 0)


    def find(self, point, radius):
        assert len(point) == self.dim
        
        self._visited = 0

        def _find(current, depth, maxp, minp, nodes):
            if not current:
                return

            self._visited += 1

            if current.point.dist(point) <= radius:
                nodes.append(current)
                _find(current.left, depth + 1, nodes)
                _find(current.right, depth + 1, nodes)
                return

            axis = depth % self.dim

            # XXX This can miss some nodes
            # Think we need to keep track of min/max for each dimension
            # to be sure we can actually rule out half
            if point[axis] < current.point[axis]:
                # update maxp
                maxp_l = list(maxp)
                maxp_l[axis] = current.point[axis]
                # ...
                _find(current.left, depth + 1, nodes)
            else:
                # update minp
                _find(current.right, depth + 1, nodes)

        nodes = []
        maxp = KPoint([math.inf] * self.dim)
        minp = -maxp
        _find(self.head, 0, maxp, minp, nodes)
        print(f'visited = {self._visited}')
        return nodes

def test():
    import random

    t1 = KTree(1)
    
    for i in range(100):
        t1.insert((random.randint(-100, 100),), str(i))

    nodes = t1.find(KPoint((45,)), 10)
    print('t1')
    for n in nodes:
        print(n)

    t2 = KTree(2)
    l2 = []

    for i in range(1000):
        p = KPoint([random.randint(-100, 100) for _ in range(2)])
        t2.insert(p, str(i))
        l2.append(p)
    nodes = t2.find(KPoint((0, 0)), 5)
    nodesl = [x for x in l2 if x.dist((0, 0)) <= 5]
    print('t2')
    assert len(nodes) == len(nodesl)
    for n in nodes:
        print(n)

if __name__ == '__main__':
    test()
