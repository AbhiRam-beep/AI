import heapq

goal = ((1,2,3),(4,5,6),(7,8,0))

def manhattan(s):
    d = 0
    for i in range(3):
        for j in range(3):
            v = s[i][j]
            if v != 0:
                gi = (v-1)//3
                gj = (v-1)%3
                d += abs(i-gi) + abs(j-gj)
    return d

def neighbors(state):
    s = [list(r) for r in state]
    x=y=0
    for i in range(3):
        for j in range(3):
            if s[i][j]==0: x,y=i,j
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    res=[]
    for dx,dy in moves:
        nx,ny=x+dx,y+dy
        if 0<=nx<3 and 0<=ny<3:
            new = [row[:] for row in s]
            new[x][y], new[nx][ny] = new[nx][ny], new[x][y]
            res.append(tuple(tuple(r) for r in new))
    return res

def astar(start):
    pq = []
    heapq.heappush(pq, (manhattan(start), start))
    g = {start: 0}
    parent = {}

    while pq:
        f, state = heapq.heappop(pq)

        if state == goal:
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            return path[::-1]

        for nxt in neighbors(state):
            new_g = g[state] + 1
            if nxt not in g or new_g < g[nxt]:
                g[nxt] = new_g
                f = new_g + manhattan(nxt)
                heapq.heappush(pq, (f, nxt))
                parent[nxt] = state

    return None


start = ((1,2,3),
         (4,5,6),
         (0,7,8))

path = astar(start)

for p in path:
    for row in p:
        print(row)
    print()
