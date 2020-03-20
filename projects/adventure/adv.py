from room import Room
from player import Player
from world import World
from util import Queue, Stack


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# reverse_direction = {
#     'n': 's',
#     's': 'n',
#     'e': 'w',
#     'w': 'e'
# }
# go_back = lambda x: list(map(lambda y: reverse_direction[y], x))[::-1]

def go_back(dirs):
    '''
    Takes a list/set of directions {'n', 's', 'e', 'w'}
    Returns a list/set with the directions in reverse order
    and replaced with the opposite direction
    eg ['n', 's', 'e', 'w'] => ['e', 'w', 'n', 's']
    '''
    reverse_direction = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }
    if str(type(dirs)) == "<class 'list'>":
        return [reverse_direction[dir] for dir in dirs[::-1]]
    elif str(type(dirs)) == "<class 'set'>":
        return {reverse_direction[dir] for dir in dirs[::-1]}
    else:
        raise TypeError

traversal_path = []
num_rooms = len(world.rooms)
visited = [{} for num in range(num_rooms)]
print(visited)

# Stores directions back to any room visited from the current room
room_map = {num: [] for num in range(num_rooms)}

reverse_direction = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
}

def unexplored(visited):
    if {} in visited:
        return True
    for r in visited:
        for d in r:
            if r[d] == '?':
                return True
    return False

s = Stack()

curr = player.current_room
for dir in curr.get_exits():
    # s.push([dir])

    visited[curr.id][dir] = '?'
    print(visited[curr.id][dir])

move = None
print(visited)
print(f"Condition: {len(list(filter(lambda x: x != {}, visited)))}")
# while s.size() > 0:
# while len(list(filter(lambda x: x != {}, visited))) > 0:

# while unexplored(visited):
count = -1
while count < 20:
    count += 1
    # v = s.pop()
    print(f"Path: {traversal_path}")
    old_move = move
    move = None
    print(f"Current Room: {curr.id}")
    print(f"Visited: {visited}")

    # GET NEXT MOVE
    for dir in curr.get_exits():
        print(f"Available Direction: {dir}")
        print(f"Checking new move condition: {visited[curr.id][dir]}")
        if visited[curr.id][dir] == '?':
            print(f"Great! A new move to make! Let's go {dir}")
            move = dir
            break
    
    # MAKE NEXT MOVE
    if move is not None:
        traversal_path.append(move)
        player.travel(move)
    else:
        move = reverse_direction[old_move]
        traversal_path.append(move)
        player.travel(reverse_direction[move])
    # print(f"Current Room: {curr.id}")
    # print(visited[curr.id])
    
    prev = curr
    curr = player.current_room
    print(f"New Current: {curr.id}")
    visited[prev.id][move] = curr.id
    visited[curr.id][reverse_direction[move]] = prev.id
    print(f"Visited for {prev.id}: {visited[prev.id]}")
    exits = curr.get_exits()
    print(f"Exits: {exits}")
    if not visited[curr.id]:
        print(f"Ooh a new room: {curr.id}")
        visited[curr.id] = {e: '?' for e in exits}
        # print(f"Visited: {visited}")
        # print(f"Update to visited: {visited[curr.id]}")
    # if not exits or all([visited[curr.id][dir] != '?' for dir in exits]):
    #     # print("Going back")
    #     player.travel(reverse_direction[move])
        
        # # BFS
        # q = Queue()
        # q.enqueue([curr])

    # else: 
        # for e in exits:
            # player.travel(e)
            # curr = player.current_room
            # new_exits = curr.get_exits()
            # visited[curr.id] = {e: '?' for e in new_exits}
            # room_map[curr.id].append(e)
            # s.push([*v, e])

            # e_exits = e.get_exits()
            # if not e_exits:
                # e_exits 










# DFT
# s = Stack()
# s.push([player.current_room])
# vis = set()
# while s.size() > 0:
#     v = s.pop()
#     # if not visited[v]:
#     if v[-1] not in vis:
#         exits = v[-1]
#         vis.add(exits)
#         for move in self.get_exits():
#             player.travel()
        
#         visited[v] = {ex: '?' for ex in player.current_room.get_exits()}


# q = Queue()
# q.enqueue([player.current_room])
# visited = {player.current_room}
# while q.size() > 0:
# for r in player.current_room.get_exits():
    


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
