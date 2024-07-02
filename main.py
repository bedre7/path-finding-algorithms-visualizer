import sys
from maze_solver import MazeSolver

choices = {
    1 : 'BFS',
    2 : 'DFS',
    3 : 'ASTAR',
    4 : 'GREEDY',
    5 : 'RANDOM',
    6 : 'EXIT',
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py <test_file>')
        sys.exit(1)

    filePath = sys.argv[1]
    mazeSolver = MazeSolver(filePath)
    print('***********************************************************************')
    print('*****              Path Finding Algorithms Visualizer             *****')
    print('***********************************************************************')
    
    while True:
        print('***********************************************************************')
        print('*****                [1] Breadth First Search (BFS)               *****')
        print('*****                [2] Depth First Search (DFS)                 *****')
        print('*****                [3] A* Search                                *****')
        print('*****                [4] Greedy Search                            *****')
        print('*****                [5] Random Search                            *****')
        print('*****                [6] Exit                                     *****')
        print('***********************************************************************')
        choice = int(input('Choose an Algorithm to Visualize: '))
        
        if choice == 6:
            break
        elif choice not in choices:
            print('\nInvalid choice. Please try again.')
            continue
        else:
            maze, nodesExpanded, pathLength = mazeSolver.solve(choices[choice].lower())
            mazeSolver.printMaze(maze)
            print('\n-------------------------\n')
            print('Solved with:     ', choices[choice], 'algorithm')
            print('Nodes expanded:  ', nodesExpanded)
            print('Path length:     ' ,pathLength)
            input('\nPress enter to continue...')
            print()
