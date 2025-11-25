tree = {
    'A': ['B','C'],
    'B': ['D','E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

goal = 'E'

def dls(node, limit):
    if node == goal:
        return node
    if limit == 0:
        return None
    for child in tree[node]:
        res = dls(child, limit - 1)
        if res:
            return res
    return None

def iddfs(root):
    depth = 0
    while True:
        result = dls(root, depth)
        if result:
            return result
        depth += 1

print(iddfs('A'),"found")
