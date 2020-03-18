from util import Stack

def earliest_ancestor(ancestors, starting_node):
    # Check for no parents
    if not get_parents(ancestors, starting_node):
        return -1
    
    # DFS
    s = Stack()
    s.push([starting_node])
    visited = []#set()
    while s.size() > 0:
        v = s.pop()
        if v[-1] not in visited:
            visited.append(v)
            for parent in get_parents(ancestors, v[-1]):
                s.push([*v, parent])

    # Get the longest chain
    m = []
    for v in visited:
        if len(v) > len(m):
            m = v
        if len(v) == len(m):
            if v[-1] <= m[-1]:
                m = v

    # Return final element (earliest ancestor)
    return m[-1]


def get_parents(ancestors, node):
    """
    Returns a list of the parent ids for the given node
    """
    return [a[0] for a in ancestors if a[1] == node]