#! python        
from itertools import permutations

def getBestPathsTimes(time):
    """
    A derivation of Bellman-Ford.
    In the case there is no negativeWeightCycles in the graph -
    Returns the best posible times from i to j for all i,j nodes on graph.
    """
    dim = len(time)
    for k in range(dim):
        for i in range(dim):
            for j in range(dim):
                if time[i][j] > time[i][k] + time[k][j]:
                    time[i][j] = time[i][k] + time[k][j]
    return time
    
def negativeWeightCyclesExists(graph):
    for i in range(len(graph)):
        # A negative weight cycles means a node and a cycle on it
        # exists, such that walking the cycle adds time to the clock.
        if graph[i][i] < 0: 
            return True
    return False
    
def timeOf(path, time):
    """
    path: An ordered list of bunnies 
    arr: A 2D arr such that arr[i][j] is the time from node i to node j
    return: total time of legel (start at 0 , end at -1) walk on graph. 
    """
    p = [0] + path[:] + [-1]
    tot = 0
    for i in range(len(p)-1):
        source = p[i]
        dest = p[i+1]
        tot += time[source][dest]
    return tot

def solution(time, time_limit):
    """
    Let G be the directed, bidirectional, full graph with nodes marking
    the start, end and bunnies location. We have an edge between any 2 nodes
    with wieght defind by 'time' array. 
    Solution will:
    1) use the Bellman-Ford method to relax paths from any 
    node to any node (I.E fix each node as a starting node and
    find best paths from it to all the rest.
    2) In case negative weight cycles exists - we can keep improving #1
    so we can always have more time to get more bunnies - return all bunnies.
    3) Now, we have a "new" graph we get from #1 and #2, such that it has 
    no negative weight cycles and, for every 2 nodes i,j, the shortest time 
    from i to j is the weight of the edge (i->j). we must start at the start
    node and finish at the end node. Because the new graph is optimal,
    revisiting nodes can only take time so we won't do it (I.E. there's no reson 
    to go back to a visted node. For exapmle (s,0,1,0,e) is the same as (s,0,1,e)
    but takes at least the same time). All we have now is decide which 
    bunnies we go get. We do that by looking at all possible combinations.
    Complexity: #1 - O(pow(n,3)). #2 - O(n). 
    #3 - O(sum([ i! for i in range(n-1)])) (oh no o:). 
    """
    bunniesNum = len(time) - 2
    time = getBestPathsTimes(time)
    
    if negativeWeightCyclesExists(time):
        # We can accumulate as much time we need and get all bunnies.
        return list(range(bunniesNum))

    # iterate on all possible number of retrievable bunnies 
    # starting with the largest one - all bunnies.
    for i in reversed(range(bunniesNum+1)):
        # Per i, iterate over all possible ways to retrive i bunnies.
        # 'permutations' returns an ordered iterable so, while 
        # traversing it, we start with the minimal bunny ID. 
        for p in permutations(range(1, bunniesNum+1), i):
            timeOfPath = timeOf(list(p), time)
            # The first time the if statment below is True -
            # it means we got to the largest number of retrievable
            # bunnies and our path goes throw the minimal Indices. 
            if timeOfPath <= time_limit:
                return sorted([i-1 for i in p])
    return []

print solution([
    [0, 2, 2, 2, -1], 
    [9, 0, 2, 2, -1], 
    [9, 3, 0, 2, -1], 
    [9, 3, 2, 0, -1], 
    [9, 3, 2, 2,  0]
    ],
    1
) == [1,2]
# Output:
#     [1, 2]

print solution([
    [0, 1, 1, 1, 1], 
    [1, 0, 1, 1, 1], 
    [1, 1, 0, 1, 1], 
    [1, 1, 1, 0, 1], 
    [1, 1, 1, 1, 0]], 
    3
) == [0,1]

print solution([
    [0,-10],
    [1,0]
],1) == []

print solution([
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0]], 
    0
) == [0,1,2]

print solution([
    [0,  1,  5,  5,  2], 
    [10, 0,  2,  6,  10], 
    [10, 10, 0,  1,  5], 
    [10, 10, 10, 0,  1], 
    [10, 10, 10, 10, 0]], 
    5
) == [0,1,2]

# links to challenge 
# Refer a friend: "https://foobar.withgoogle.com/?eid=VDuOf" (Unused)
# Refer a friend: "https://foobar.withgoogle.com/?eid=MeheO" (Unused)

