import heapq
import random
from utils import Utils
from constants import *
from colors import Colors
from collections import defaultdict, deque
from queue import PriorityQueue

class MazeSolver:
    def __init__(self, filePath):
        self.filePath = filePath
        self.maze = []
        self.pathLength = 0
        self.nodesExpanded = 0
        self.x0 = self.y0 = self.x1 = self.y1 = None
        self.path = defaultdict(lambda: (-1, -1))
        self.methods = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'astar': self.astar,
            'greedy': self.greedy,
            'random': self.random,
        }
        self.cols = self.rows = 0
        self.createMaze()
        
    def solve(self, method):
        if method not in self.methods:
            print('Invalid method!')
            return
        
        self.path.clear()
        self.nodesExpanded = 0
        return self.methods[method]()
        
    def createMaze(self):
        testFile = open(self.filePath, 'r')
        
        for line in testFile:
            if line.lower().startswith('start'):
                words = line.split(',')
                self.y0 = int(words[0].split()[1])
                self.x0 = int(words[1].strip())
            elif line.lower().startswith('end'):
                words = line.split(',')
                self.y1 = int(words[0].split()[1])
                self.x1 = int(words[1].strip())
            else:
                self.maze.append([char for char in line if char != '\n'])
        
        self.cols = len(self.maze[0])
        self.rows = len(self.maze)

        testFile.close()
    
    def reconstructPath(self, maze, x, y):
        trace = [(x, y)]
        self.pathLength = 0
        while self.path[(x, y)] != (-1, -1):
            x, y = self.path[(x, y)]
            trace.append((x, y))
            self.pathLength += 1

        for x, y in reversed(trace):
            maze[x][y] = PATH

        maze[self.x0][self.y0] = START
        maze[self.x1][self.y1] = END

        return [maze, self.nodesExpanded, self.pathLength]

    def printMaze(self, maze):
        Utils.clearScreen()

        for row in maze:
            for cell in row:
                if cell == PATH:
                    print(Colors.RED + Colors.BOLD + cell + Colors.ENDC, end='')
                elif cell == START or cell == END:
                    print(Colors.CYAN + cell + Colors.ENDC, end='')
                elif cell == OPENED:
                    print(Colors.YELLOW + cell + Colors.ENDC, end='')
                elif cell == POINT:
                    print(Colors.RED + Colors.BOLD + cell + Colors.ENDC, end='')
                else:
                    print(cell, end='')
            print()
        
    def isValid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def bfs(self):
        maze = [row[:] for row in self.maze]
        if self.x0 == self.x1 and self.y0 == self.y1:
            maze[self.x0][self.y0] = POINT
            return [maze, self.nodesExpanded, self.pathLength]
        
        queue = deque([(self.x0, self.y0)])
        visited = set([(self.x0, self.y0)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            x, y = queue.popleft()
            maze[x][y] = OPENED
            self.nodesExpanded += 1

            self.printMaze(maze)
            if x == self.x1 and y == self.y1:
                return self.reconstructPath(maze, x, y)
            
            for dx, dy in directions:
                a, b = x + dx, y + dy
                if self.isValid(a, b) and maze[a][b] != WALL and (a, b) not in visited:
                    queue.append((a, b))
                    visited.add((a, b))
                    self.path[(a, b)] = (x, y)
            
        return None

    def dfs(self):
        maze = [row[:] for row in self.maze]
        if self.x0 == self.x1 and self.y0 == self.y1:
            maze[self.x0][self.y0] = POINT
            return [maze, self.nodesExpanded, self.pathLength]
        
        stack = [(self.x0, self.y0)]
        visited = set([(self.x0, self.y0)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while stack:
            x, y = stack.pop()
            maze[x][y] = OPENED
            self.nodesExpanded += 1

            self.printMaze(maze)
            if x == self.x1 and y == self.y1:
                return self.reconstructPath(maze, x, y)
            for dx, dy in directions:
                a, b = x + dx, y + dy
                if self.isValid(a, b) and maze[a][b] != WALL and (a, b) not in visited:
                    stack.append((a, b))
                    visited.add((a, b))
                    self.path[(a, b)] = (x, y)
        
        return maze

    def random(self):
        maze = [row[:] for row in self.maze]
        if self.x0 == self.x1 and self.y0 == self.y1:
            maze[self.x0][self.y0] = POINT
            return [maze, self.nodesExpanded, self.pathLength]
        
        frontier = [(self.x0, self.y0)]
        visited = set([(self.x0, self.y0)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while frontier:
            x, y = random.choice(frontier)
            frontier.remove((x, y))
            maze[x][y] = OPENED
            self.nodesExpanded += 1

            self.printMaze(maze)
            if x == self.x1 and y == self.y1:
                return self.reconstructPath(maze, x, y)
            for dx, dy in directions:
                a, b = x + dx, y + dy
                if self.isValid(a, b) and maze[a][b] != WALL and (a, b) not in visited:
                    frontier.append((a, b))
                    visited.add((a, b))
                    self.path[(a, b)] = (x, y)
        
    def getManhattanDistance(self, x, y):
        return abs(self.x1 - x) + abs(self.y1 - y)
    
    def heuristic(self, x, y):
        return self.getManhattanDistance(x, y)

    def greedy(self):
        maze = [row[:] for row in self.maze]
        if self.x0 == self.x1 and self.y0 == self.y1:
            maze[self.x0][self.y0] = POINT
            return [maze, self.nodesExpanded, self.pathLength]

        priorityQueue = PriorityQueue()
        priorityQueue.put((self.heuristic(self.x0, self.y0), (self.x0, self.y0)))
        visited = set([(self.x0, self.y0)])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while priorityQueue:
            _, (x, y) = priorityQueue.get()
            maze[x][y] = OPENED
            self.nodesExpanded += 1

            self.printMaze(maze)
            if x == self.x1 and y == self.y1:
                return self.reconstructPath(maze, x, y)
            
            for dx, dy in directions:
                a, b = x + dx, y + dy
                if self.isValid(a, b) and maze[a][b] != WALL and (a, b) not in visited:
                    priorityQueue.put((self.heuristic(a, b), (a, b)))
                    visited.add((a, b))
                    self.path[(a, b)] = (x, y)

    
    def astar(self):
        maze = [row[:] for row in self.maze]
        if self.x0 == self.x1 and self.y0 == self.y1:
            maze[self.x0][self.y0] = POINT
            return [maze, self.nodesExpanded, self.pathLength]
        
        frontier = []
        heapq.heappush(frontier, (self.heuristic(self.x0, self.y0), (self.x0, self.y0)))
        costs = defaultdict(int, {(self.x0, self.y0): 0})
        closed = set()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while frontier:
            _, (x, y) = heapq.heappop(frontier)
            maze[x][y] = OPENED
            self.nodesExpanded += 1

            self.printMaze(maze)
            if x == self.x1 and y == self.y1:
                return self.reconstructPath(maze, x, y)
            
            for dx, dy in directions:
                a, b = x + dx, y + dy
                currentCost = self.heuristic(a, b) + costs[(x, y)] + 1

                if not self.isValid(a, b) or maze[a][b] == WALL: continue
                if (a, b) in closed: continue
                if (a, b) not in costs or costs[(x, y)] + 1 < costs[(a, b)]:
                    if (a, b) not in costs:
                        heapq.heappush(frontier, (currentCost, (a, b)))
                    elif costs[(x, y)] + 1 < costs[(a, b)]:
                        frontier.remove((costs[(a, b)] + self.heuristic(a, b), (a, b)))
                        heapq.heapify(frontier)
                        heapq.heappush(frontier, (currentCost, (a, b)))
                    
                    costs[(a, b)] = costs[(x, y)] + 1
                    self.path[(a, b)] = (x, y)
            
            closed.add((x, y))