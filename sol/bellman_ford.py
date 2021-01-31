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
    
if __name__ == '__main__':
    
    A = [
            [0, 2, 2, 2, -1], 
            [9, 0, 2, 2, -1], 
            [9, 3, 0, 2, -1], 
            [9, 3, 2, 0, -1], 
            [9, 3, 2, 2,  0]
    ]

    graph = arryToGraphDict(A)
    
    # print(graph)
    # print(A)
    bestPathsCost, bestPaths, cycles = [], [], []
    
    for i in range(len(A)):
        distance, predecessor, negativeWeightCycles = bellman_ford(graph, source=i)
        bestPathsCost.append(list(distance.values()))
    
    for l in bestPathsCost:
        print(l)

