""" graphs.py

Graph Theory """

from . constants import getDirections


def getPath(graph, start, end, path=[]):
    path = path + [start]

    if start == end:
        return path

    if start not in graph:
        return None

    shortest = None

    for node in graph[start]:
        if node not in path:
            newpath = getPath(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def getGraph(nodes):
    graph = dict()
    for node in nodes:
        directions = set(getDirections(node))
        graph[node] = nodes & directions  # Set Intersection

    return graph

if __name__ == '__main__':
    nodes = {(0, 0), (0, 1), (1, 0), (2, 0), (3, 0), (3, 1)}
    graph = getGraph(nodes)
    path = getPath(graph, (0, 0), (3, 1))
    print(path)
