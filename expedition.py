from math import sqrt

__author__ = 'TriD'


class Expedition:
    def __init__(self):
        self.x = 5
        self.y = 5
        self.finished = False
        self.returned = False
        self.path = []

    def find_path(self, pos_x, pos_y, dst_x, dst_y, passed=[]):
        #something too much to really use it, but i will...
        min_dist = None

        if pos_x == dst_x and pos_y == dst_y:
            return

        def count_dist(x, y, x1, y1):
            x_dist = float(x - x1) * (x - x1)
            y_dist = float(y - y1) * (y - y1)
            return sqrt(x_dist + y_dist)

        def check_dist(tx, ty, dst_x, dst_y, min_dist):
            dist = count_dist(tx, ty, dst_x, dst_y)
            if min_dist > dist:
                return dist, True
            return min_dist, False

        #check east
        tx = pos_x + 1
        best_x = pos_x + 1
        best_y = pos_y
        min_dist = count_dist(tx, pos_y, dst_x, dst_y)
        #check south-east
        ty = pos_y + 1
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check south
        tx = pos_x
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check south-west
        tx = pos_x - 1
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check west
        ty = pos_y
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check north-west
        ty = pos_y - 1
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check north
        tx = pos_x
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty
        #check north-west
        tx = pos_x + 1
        min_dist, better = check_dist(tx, ty, dst_x, dst_y, min_dist)
        if better:
            best_x = tx
            best_y = ty

        passed.append((best_x, best_y))
        self.find_path(best_x, best_y, dst_x, dst_y, passed)
        self.path = passed

    def move(self):
        if self.path:
            pos_x, pos_y = self.path[0]
            self.x = pos_x
            self.y = pos_y
            del self.path[0]
        elif not self.finished:
            self.finished = True
            self.find_path(self.x, self.y, 5, 5)
            self.x, self.y = self.path[0]
            del self.path[0]
        else:
            self.returned = True