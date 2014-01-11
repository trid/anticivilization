import math
from point import Point

__author__ = 'TriD'


class Node:
    def __init__(self, game_map, point):
        self.game_map = game_map
        self.point = point

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return self.point.x * 101 + self.point.y

    def get_edges(self):
        #Very strange coroutine that will save some time in coding
        game_map = self.game_map
        point = self.point
        points = (Point(point.x, point.y - 1),
                  Point(point.x + 1, point.y - 1),
                  Point(point.x + 1, point.y),
                  Point(point.x + 1, point.y + 1),
                  Point(point.x, point.y + 1),
                  Point(point.x - 1, point.y + 1),
                  Point(point.x - 1, point.y),
                  Point(point.x - 1, point.y - 1))
        for point in points:
            if game_map[point.x][point.y].ground != 'water':
                yield Edge(game_map, self, Node(game_map, point))


class Edge:
    def __init__(self, game_map, node_from, node_to):
        self.game_map = game_map
        self.node_from = node_from
        self.node_to = node_to


class AStarFinder():
    def find(self, game_map, start_point, end_point, limit=()):
        start_node = Node(game_map, start_point)
        finish_node = Node(game_map, end_point)
        start_heuristic = self.heuristic(start_node.point, end_point)

        closed_set = set()
        open_set = [(start_node, start_heuristic)]
        came_from = {}

        gscore = {start_node: 0}
        fscore = {start_node: start_heuristic}

        while open_set:
            current_node = open_set.pop()[0]
            closed_set.add(current_node)
            if current_node == finish_node:
                return self.formate_path(came_from, current_node)
            for edge in current_node.get_edges():
                if edge.node_to in closed_set:
                    continue
                #Here will be cost for passing tile
                #and somehow i'll add here some way to avoid tiles that character can't pass
                tentative_g_score = gscore[current_node] + 1
                hcost = self.heuristic(end_point, edge.node_to.point)

                if not self.is_in_open_set(open_set, edge.node_to) or tentative_g_score < gscore[edge.node_to]:
                    came_from[edge.node_to] = edge
                    gscore[edge.node_to] = tentative_g_score
                    fscore[edge.node_to] = gscore[edge.node_to] + self.heuristic(end_point, edge.node_to.point)
                    if not self.is_in_open_set(open_set, edge.node_to):
                        self.add_to_open_set(open_set, edge.node_to, fscore[edge.node_to])

        return None

    def heuristic(self, point1, point2):
        return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

    def add_to_open_set(self, open_set, node_to, heuristic):
        if not len(open_set):
            open_set.append((node_to, heuristic))
            return
        else:
            for i in range(0, len(open_set)):
                if open_set[i][1] < heuristic:
                    open_set.insert(i, (node_to, heuristic))
                    return
        open_set.append((node_to, heuristic))

    def formate_path(self, came_from, node):
        current_node = node
        path = [current_node.point]
        while current_node in came_from:
            current_node = came_from[current_node].node_from
            path.append(current_node.point)
        return path

    def is_in_open_set(self, open_set, node):
        for t in open_set:
            if t[0] == node:
                return True
        return False