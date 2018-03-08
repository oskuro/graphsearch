#!/usr/bin/env python
import sys

# G-cost = a nodes cost from starting node.
# H-cost = a nodes cost from target node
# F-cost = g-cost + h-cost

''' get neighbour with lowest f-cost
    if more than one neighbour have the same f-cost. choose the one with the lowest h-cost but add the others to open_list
'''

class Node(object):
    def __init__(self, x, y, traversable = True):
        self.x = x
        self.y = y
    
    def to_string(self):
        return "X: %i Y: %i G: %s H: %s F: %s " % (self.x, self.y, self.g, self.h, self.f)

    x = 0
    y = 0

    g = float("inf")
    h = float("inf")
    f = float("inf")

    parent = ""
    traversable = True


class GraphSearch(object):

    def __init__(self):
        
        print("starting...")
        self.adjecent_cost = 10
        self.diagonal_cost = 14

        size = 10
        self.tilelist = [[Node(x,y) for y in range(size)] for x in range(size)]
        open_nodes = []  # set of nodes that needs to be evaluated
        closed_nodes = []  # set of nodes that is already evaluated

        start_node = self.tilelist[1][3]
        target_node = self.tilelist[4][8]
        print(start_node.to_string())
        print(target_node.to_string())

        start_node.g = 0
        start_node.h = self.get_cost(start_node, target_node)
        start_node.f = start_node.h

        

        open_nodes.append(start_node)

        while len(open_nodes) > 0:
            
            current = self.get_node_with_lowest_f_cost(open_nodes)
            print("Current: %s" % current.to_string())
            open_nodes.remove(current)
            closed_nodes.append(current)

            if current == target_node:
                print("Found target. yay!")
                while current.parent != "":
                    print(current.to_string())
                    current = current.parent
                print(start_node.to_string())
                sys.exit()
            
            for x in self.get_range(current.x, size):
                for y in self.get_range(current.y, size):
                    neighbour = self.tilelist[x][y]

                    if self.contains(neighbour, closed_nodes):
                        continue

                    if neighbour == current:
                        continue

                    if neighbour.traversable == False:
                        self.remove_from_list(neighbour, open_nodes)
                        self.add_to_list(neighbour, closed_nodes)
                        continue

                    score = current.g + self.get_cost(current, neighbour)
                    if not self.contains(neighbour, open_nodes) or score < neighbour.g:
                        neighbour.g = current.g + self.get_cost(neighbour, current)
                        neighbour.h = self.get_cost(neighbour, target_node)
                        neighbour.f = neighbour.g + neighbour.h
                        neighbour.parent = current
                        open_nodes.append(neighbour)
                    else:
                        self.add_to_list(neighbour, closed_nodes)
        
            #self.print_map(open_nodes, closed_nodes, size)

    def remove_from_list(self, node, list):
        if self.contains(node, list):
            list.remove(node)

    def add_to_list(self, node, list):
        if not self.contains(node, list):
            list.append(node)

    def print_map(self, o, c, s):
        for x in range(0, s):
            for y in range(0, s):
                node = self.tilelist[x][y]
                if self.contains(node, o):
                    sys.stdout.write("@")
                else:
                    sys.stdout.write("#")
            print("")
                
        
    def get_cost(self, node, target_node):
        cost = 0

        xdiff = abs(node.x - target_node.x)
        ydiff = abs(node.y - target_node.y)
            
        cost = min(xdiff, ydiff) * self.diagonal_cost + abs(xdiff - ydiff) * self.adjecent_cost

        return cost

    def get_node_with_lowest_f_cost(self, open_nodes):
        lowest_cost_node = Node(0,0)
        lowest_cost_node.f = float("inf")

        for node in open_nodes:

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

        return range(min, max)

if __name__ == '__main__':
    GraphSearch()
