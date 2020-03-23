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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Get the number of rooms from the world object
num_rooms = len(world.rooms)

# Initialize our traversal path and visited lists
traversal_path = []
visited = [{} for num in range(num_rooms)]

# Allows us to translate directions we've traveled into a
#  path back to where we came from
reverse_direction = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
}

# We will use this function to tell us when we are done exploring
def unexplored(visited):
    """
    Takes visited list as input and returns
     True if there are rooms we haven't explored, or
     False if there are no rooms we haven't explored
    """
    if {} in visited:
        return True
    for r in visited:
        for d in r:
            if r[d] == '?':
                return True
    return False

# We will use this stack to keep track of the moves we make
#  so that we can go backwards when we hit a room with nowhere
#  new to go.
s = Stack()
# Set up visited for starting room
curr = player.current_room
for dir in curr.get_exits():
    visited[curr.id][dir] = '?'


move = None
# print(visited)
# print(f"Condition: {len(list(filter(lambda x: x != {}, visited)))}")

while unexplored(visited):
    # Set up our moves for this iteration    
    old_move = move
    move = None
    
    # GET NEXT MOVE
    # Go through current room's exits and find a
    #  room that hasn't been explored
    for dir in curr.get_exits():
        if visited[curr.id][dir] == '?':
            move = dir
            break
    
    # MAKE NEXT MOVE
    if move is not None:
        traversal_path.append(move)
        s.push(move)
        player.travel(move)
    # GO BACK
    # If there wasn't an exit for the current room that
    #  we haven't explored, go back the way we came
    else:
        old_move = s.pop()
        move = reverse_direction[old_move]
        traversal_path.append(move)
        player.travel(move)

    
    # MAKE UPDATES TO VISITED
    # Update prev and curr room variables
    prev = curr
    curr = player.current_room
    # Mark the direction we traveled as explored in the old
    #  room and set to new room
    visited[prev.id][move] = curr.id
    # Get our new exits
    exits = curr.get_exits()
    # If current room hasn't been visited before,
    if not visited[curr.id]:
        # Put its exits into visited with ? for unexplored
        visited[curr.id] = {e: '?' for e in exits}
        # Mark the direction we just came from explored and
        #  set to old room
        visited[curr.id][reverse_direction[move]] = prev.id


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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
