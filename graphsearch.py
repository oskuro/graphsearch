#!/usr/bin/env python
import sys


# G-cost = a nodes distance from starting node.
# H-cost = a nodes distance from target node
# F-cost = g-cost + h-cost

''' get neighbour with lowest f-cost
    if more than one neighbour have the same f-cost. choose the one with the lowest h-cost but add the others to open_list
    The chosen neighbour comes current and is added to closed.
    when itterating over neighbours update 
    
'''
class Node(object):
    def __init__(self, x, y, target_node = None, traversable = True):
        self.x = x
        self.y = y

    x = 0
    y = 0

    g = 0
    h = 0
    f = 0

    parent = ""

    traversable = True


class GraphSearch(object):

    def __init__(self):
        
        print("starting...")
        self.adjecent_cost = 10
        self.diagonal_cost = 14

        open_nodes = []  # set of nodes that needs to be evaluated
        closed_nodes = []  # set of nodes that is already evaluated

        start_node = Node(2,3)
        target_node = Node(4,8)

        start_node.h = self.get_cost(start_node, target_node)
        start_node.f = self.get_cost(start_node, target_node)

        size = 10
        self.tilelist = [[Node(x,y, target_node) for x in range(size)] for y in range(size)]

        open_nodes.append(start_node)

        while len(open_nodes) > 0:
            current = self.get_node_with_lowest_f_cost(open_nodes)
            print("in loop with current X: %i Y: %i") % (current.x, current.y)
            open_nodes.remove(current)
            closed_nodes.append(current)

            if current.x == target_node.x and current.y == target_node.y:
                print("Found target. yay!")
                sys.exit()
            
            for x in self.get_range(current.x, size):
                for y in self.get_range(current.y, size):
                    neighbour = self.tilelist[x][y]
                    if self.contains(neighbour, closed_nodes) or (neighbour.x == current.x and neighbour.y == current.y):
                        continue

                    print("Checking neighbour X: %i Y: %i") % (neighbour.x, neighbour.y)

                    if not self.contains(neighbour, open_nodes):
                        open_nodes.append(neighbour)
                        neighbour.g = current.g + 1
                        neighbour.h = self.get_cost(neighbour, target_node)
                        neighbour.f = neighbour.g + neighbour.h
                    else:
                        if neighbour.f < current.f or (neighbour.f == current.f and neighbour.h < current.h):
                            neighbour.g = current.g + 1
                            neighbour.f = neighbour.g + neighbour.h
                            neighbour.parent = current
                            
    def print_map():
        pass
        
    def get_cost(self, node, target_node):
        cost = 0

        xdiff = abs(node.x - target_node.x)
        ydiff = abs(node.y - target_node.y)
            
        cost = min(xdiff, ydiff) * self.diagonal_cost + abs(xdiff - ydiff) * self.adjecent_cost

        return cost

    def get_node_with_lowest_f_cost(self, open_nodes):
        lowest_cost_node = Node(0,0)
        lowest_cost_node.f = 100000
        for node in open_nodes:
            if node.f == 0:
                print("node has no f cost. skipping")
                continue

            if node.f < lowest_cost_node.f or (node.f == lowest_cost_node.f and node.h < lowest_cost_node.h):
                lowest_cost_node = node
        return lowest_cost_node

    def contains(self, node, nodelist):
        for n in nodelist:
            if n == node:
                return True
        return False

    def get_range(self, value, size):
        min = value - 1
        max = value + 2

        if min < 0:
            min = 0

        if max > size:
            max = size -1

        return range(value-1, value+1)

if __name__ == '__main__':
    GraphSearch()