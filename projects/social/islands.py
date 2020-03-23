# Write a function that takes a 2D binary array and returns the number of 1 islands. An island consists of 1s that are connected to the north, south, east or west. For example:



# 1. Translate the problem into terminology you've learned this week
# 2. Build your graph
# 3. Traverse your graph
from util import Stack

def island_counter(matrix):
    # Create a visited matrix
    visited = []
    for i in range (len(matrix)):
        visited.append([False] * len(matrix[0]))
    island_count = 0
    # for all nodes:
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            # if node is not visited
            if not visited[row][col]:
                # if we hit a 1 that has not been visited 
                if matrix[row][col] == 1:
                    # mark visited
                    visited = dft(row, col, matrix, visited)
                    # incremented visited count
                    island_count += 1
    return island_count


def dft(start_row, start_col, matrix, visited):
    s = Stack()
    s.push((start_row, start_col))
    while s.size() > 0:
        v = s.pop()
        row = v[0]
        col = v[1]
        if not visited[row][col]:
            visited[row][col] = True
            for neighbor in get_neighbors(row, col, matrix):
                s.push(neighbor)
    return visited

def get_neighbors(row, col, matrix):
    '''
    Return a list of neighboring 1 tuples in the form [(row, col)]
    '''
    neighbors = []
    # check north
    if row > 0 and matrix[row-1][col] == 1:
        neighbors.append((row-1, col))
    # check south
    if row < len(matrix) - 1 and matrix[row+1][col] == 1:
        neighbors.append((row+1, col))
    # check east
    if col < len(matrix[0]) - 1 and matrix[row][col+1] == 1:
        neighbors.append((row, col + 1))
    # check west
    if col > 0 and matrix[row][col-1] == 1:
        neighbors.append((row, col-1))
    return neighbors


islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]
count = island_counter(islands) # returns 4
print(count)