from copy import deepcopy

goal = [[1,2,3],[4,5,6],[7,8,0]]

def is_goal(s):
    return s == goal

def find_zero(s):
    for i in range(3):
        for j in range(3):
            if s[i][j] == 0:
                return i,j

def neighbors(state):
    x,y = find_zero(state)
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    res = []
    for dx,dy in dirs:
        nx,ny = x+dx,y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new = deepcopy(state)
            new[x][y], new[nx][ny] = new[nx][ny], new[x][y]
            res.append(new)
    return res

def dfs_path(start):
    stack = [(start, [start])]
    visited = set()

    while stack:
        state, path = stack.pop()
        t = tuple(tuple(r) for r in state)
        if t in visited:
            continue
        visited.add(t)

        if is_goal(state):
            return path

        for nxt in neighbors(state):
            stack.append((nxt, path+[nxt]))

    return None


initial = [
    [1,2,3],
    [4,5,6],
    [0,7,8]
]

path = dfs_path(initial)

for p in path:
    for row in p:
        print(row)
    print()
