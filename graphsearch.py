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
    def __init__(self, x, y, traversable = True):
        self.x = x
        self.y = y
    
    def to_string(self):
        return "X: %i Y: %i G: %i H: %i F: %i " % (self.x, self.y, self.g, self.h, self.f)

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
            #raw_input()
            print("main loop")
            current = self.get_node_with_lowest_f_cost(open_nodes)
            #print("in loop with current X: %i Y: %i") % (current.x, current.y)
            open_nodes.remove(current)
            closed_nodes.append(current)
            print("node %s" % current.to_string())

            if current.x == target_node.x and current.y == target_node.y:
                print("Found target. yay!")
                while current.parent != "":
                    print(current.to_string())
                    current = current.parent
                sys.exit()
            
            print(self.get_range(current.x, size))
            print(self.get_range(current.y, size))
            for x in self.get_range(current.x, size):
                for y in self.get_range(current.y, size):
                    neighbour = self.tilelist[x][y]

                    if self.contains(neighbour, closed_nodes):
                        continue

                    if neighbour.x == current.x and neighbour.y == current.y:
                        continue

                    if neighbour.traversable == False:
                        self.remove_from_list(neighbour, open_nodes)
                        self.add_to_list(neighbour, closed_nodes)
                        continue

                    if not self.contains(neighbour, open_nodes):
                        open_nodes.append(neighbour)
                        neighbour.g = current.g + self.get_cost(neighbour, current)
                        neighbour.h = self.get_cost(neighbour, target_node)
                        neighbour.f = neighbour.g + neighbour.h
                        neighbour.parent = current
                    else:
                        score = neighbour.g + self.get_cost(current, neighbour)
                        if score >= current.g:
                            continue
                        neighbour.parent = current
                        print("NEW BEST: %s" % neighbour.to_string())
        
            self.print_map(open_nodes, closed_nodes, size)

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
            if node.f == 0:
                #print("node has no f cost. skipping")
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

        return range(min, max)

if __name__ == '__main__':
    GraphSearch()