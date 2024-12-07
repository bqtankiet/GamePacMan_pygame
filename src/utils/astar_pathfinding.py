from src.utils.constant import MAZE_DATA


class AStarPathfinding:
    # def __init__(self, grid):
    #     self.__grid = grid

    def execute(self, start, dest):
        pq = PriorityQueue()
        node = Node(start)
        node.hCost = abs(dest[0]-start[0]) + abs(dest[1]-start[1])
        node.gCost = 0
        pq.insert(node)
        while not pq.is_empty():
            current_node = pq.get()
            if current_node.hCost == 0: return self.build_path(current_node)
            for n in current_node.get_neighbors():
                n.parent = current_node
                n.gCost = current_node.gCost+1
                n.hCost = abs(dest[0]-n.position[0]) + abs(dest[1]-n.position[1])
                pq.insert(n)
        return None

    def build_path(self, node):
        path = []
        current = node
        while current.parent is not None:
            path.insert(0, current)
            current = current.parent
        return path

class Node:
    def __init__(self, position):
        self.position = position
        self.gCost = 0
        self.hCost = 0
        self.parent = None

    def get_fCost (self):
        return self.gCost + self.hCost

    def get_neighbors(self):
        neighbors = []
        r = self.position[0]
        c = self.position[1]
        # left
        if 0 <= c-1 < len(MAZE_DATA[0]) and MAZE_DATA[r][c-1] != 1:
            neighbors.append(Node((r,c-1)))

        # right
        if 0 <= c+1 < len(MAZE_DATA[0]) and MAZE_DATA[r][c+1] != 1:
            neighbors.append(Node((r,c+1)))

        # top
        if 0 <= r-1 < len(MAZE_DATA) and MAZE_DATA[r-1][c] != 1:
            neighbors.append(Node((r-1,c)))

        # bottom
        if 0 <= r+1 < len(MAZE_DATA) and MAZE_DATA[r+1][c] != 1:
            neighbors.append(Node((r+1,c)))

        return neighbors

    def __lt__(self, other):
        return self.get_fCost() < other.get_fCost()

    def __gt__(self, other):
        return self.get_fCost() > other.get_fCost()

import queue
class PriorityQueue:

    def __init__(self):
        self.pq = queue.PriorityQueue()

    def insert(self, node):
        self.pq.put((node.get_fCost(), node))

    def get(self):
        return self.pq.get()[1]

    def is_empty(self):
        return self.pq.empty()

if __name__ == '__main__':
    start = (1, 1)
    dest = (1, 15)
    path = AStarPathfinding().execute(start, dest)
    for n in path:
        print(n.position)

