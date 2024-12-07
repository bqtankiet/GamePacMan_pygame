from src.utils.constant import MAZE_DATA
import src.entities.maze as maze


class AStarPathfinding:
    # def __init__(self, grid):
    #     self.__grid = grid

    def execute(self, start, dest):
        pq = PriorityQueue()
        node = Node(start)
        node.hCost = abs(dest[0]-start[0]) + abs(dest[1]-start[1])
        node.gCost = 0
        pq.push(node.get_fCost(), node)
        while not pq.is_empty():
            current_node = pq.pop()
            print(current_node.position)
            if current_node.hCost == 0: return self.build_path(current_node)
            for n in current_node.get_neighbors():
                n.parent = current_node
                n.gCost = current_node.gCost+1
                n.hCost = abs(dest[0]-n.position[0]) + abs(dest[1]-n.position[1])
                if not pq.__contains__(n): pq.push(n.get_fCost(), n)
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
        x, y = self.position
        vectors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in vectors:
            nx = x + dx
            ny = y + dy

            if 0 <= ny < len(MAZE_DATA) and 0 <= nx < len(MAZE_DATA[0]) and MAZE_DATA[ny][nx] != maze.Maze.WALL:
                neighbors.append(Node((nx, ny)))

        return neighbors

    def __lt__(self, other):
        return self.get_fCost() < other.get_fCost()

    def __gt__(self, other):
        return self.get_fCost() > other.get_fCost()

    def __eq__(self, other):
        return self.position == other.position

import heapq
class PriorityQueue:
    def __init__(self):
        self.heap = []  # Danh sách dùng làm heap

    def push(self, priority, item):
        heapq.heappush(self.heap, (priority, item))

    def pop(self):
        if not self.is_empty():
            return heapq.heappop(self.heap)[1]
        raise IndexError("pop from an empty priority queue")

    def peek(self):
        if not self.is_empty():
            return self.heap[0]
        raise IndexError("peek from an empty priority queue")

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def __contains__(self, item):
        return any(entry[1] == item for entry in self.heap)

if __name__ == '__main__':
    pq = PriorityQueue()
    pq.push(1, Node((1,1)))
    pq.push(2, Node((2,1)))

