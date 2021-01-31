from itertools import chain, combinations

def arryToGraphDict(A):
    dim  = len(A)
    graph = {}
    for i in range(dim):
        line = A[i][:]
        line.pop(i)
        nodes = list(range(dim))
        nodes.pop(i)
        graph[i] = dict(zip(nodes,line))
    return graph

def bellman_ford(graph, source):
    # Step 1: Prepare the distance and predecessor for each node
    distance, predecessor = dict(), dict()
    negativeWeightCycles = []
    for node in graph:
        distance[node] = float('inf')
        predecessor[node] = None
    distance[source] = 0

    # Step 2: Relax the edges
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbour in graph[node]:
                # If the distance between the node and the neighbour is lower than the current, store it
                if distance[neighbour] > distance[node] + graph[node][neighbour]:
                    distance[neighbour] = distance[node] + graph[node][neighbour]
                    if predecessor[neighbour]:
                        predecessor[neighbour].append(node) 
                    else:
                        predecessor[neighbour] = [node]
    # Step 3: Check for negative weight cycles
    for node in graph:
        for neighbour in graph[node]:
            if distance[neighbour] > distance[node] + graph[node][neighbour]:
                negativeWeightCycles.append((node,neighbour))
 
    return distance, predecessor, negativeWeightCycles
    
def getAllPaths(n):
    s = list(range(n-2))
    paths = []
    for path in chain.from_iterable(combinations(s, r) for r in range(n-1)):
        p = [i+1 for i in path]
        paths.append([0] + p + [n-1])
    return paths
         
def timeOf(path, arr):
    p = path[:]
    tot = 0
    tmpDest = p.pop()
    while len(p) > 0:
        tmpSource = p[-1]
        tot += arr[tmpSource][tmpDest]
        tmpDest = p.pop()
    return tot

def solution(arr, timeLimit):
    graph = arryToGraphDict(arr)
    bunniesLst = list(range(len(arr)-2))
    dim = len(arr)
    
    bestPathsCost, bestPaths, cycles = [], [], []
    for i in range(dim):
        distance, predecessor, negativeWeightCycles = bellman_ford(graph, source=i)
        bestPathsCost.append(list(distance.values()))
        if negativeWeightCycles:
            return bunniesLst
    
    # Now we have a directed graph made from arr.
    # In the graph no negative weight cycles otherwise - func had returned.
    # In the new graph, for any u,v nodes in ['s',0,1,..,n,'e'], 
    # the shortest path from u to v takes bestPathsCost[u,v] secondes. 

    paths = getAllPaths(dim)
    legalPaths, bestPaths = [], []
    maxBunniesNum = i = 0
    for path in paths:        
        if timeOf(path, bestPathsCost) <= timeLimit:
            l = len(path)-2
            maxBunniesNum = l if maxBunniesNum < l else maxBunniesNum
            legalPaths.append(path[1:-1])
    legalPaths = sorted(legalPaths, key=lambda l: len(l), reverse=True)
    tmpLen = len(legalPaths[i])
    for p in legalPaths:
        if len(p) == maxBunniesNum:
            bestPaths.append(p)
    bestPaths = sorted(bestPaths)
    return [i-1 for i in bestPaths[0]]

print solution([
    [0, 2, 2, 2, -1], 
    [9, 0, 2, 2, -1], 
    [9, 3, 0, 2, -1], 
    [9, 3, 2, 0, -1], 
    [9, 3, 2, 2,  0]
    ],
    1
)
# Output:
#     [1, 2]

print solution([
    [0, 1, 1, 1, 1], 
    [1, 0, 1, 1, 1], 
    [1, 1, 0, 1, 1], 
    [1, 1, 1, 0, 1], 
    [1, 1, 1, 1, 0]], 
    3
)

# times, times_limit