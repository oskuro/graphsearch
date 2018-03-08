#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# G-cost = a nodes cost from starting node.
# H-cost = a nodes cost from target node
# F-cost = g-cost + h-cost

class Node(object):
    def __init__(self, x, y, traversable = True):
        self.x = x
        self.y = y
        self.traversable = traversable

    
    def to_string(self):
        return "X: %i Y: %i G: %s H: %s F: %s " % (self.x, self.y, self.g, self.h, self.f)

    x = 0
    y = 0

    g = float("inf")
    h = float("inf")
    f = float("inf")

    parent = None
    traversable = True


class GraphSearch(object):

    def __init__(self):
        
        print("starting...")
        self.adjecent_cost = 10
        self.diagonal_cost = 14

        self.tilelist = [[Node(0,0, True), Node(0,1, True), Node(0,2, True), Node(0,3, True), Node(0,4, True)],
                         [Node(1,0, True), Node(1,1, True), Node(1,2, True), Node(1,3, True), Node(1,4, True)],
                         [Node(2,0, True), Node(2,1, True), Node(2,2, True), Node(2,3, True), Node(2,4, True)],
                         [Node(3,0, True), Node(3,1, False), Node(3,2,False), Node(3,3, False), Node(3,4, False)],
                         [Node(4,0, True), Node(4,1, True), Node(4,2, True), Node(4,3, True), Node(4,4, True)]]

        size = len(self.tilelist)                         
        open_nodes = []  # set of nodes that needs to be evaluated
        closed_nodes = []  # set of nodes that is already evaluated

        start_node = self.tilelist[0][0]
        target_node = self.tilelist[4][4]

        start_node.g = 0
        start_node.h = self.get_cost(start_node, target_node)
        start_node.f = start_node.h

        open_nodes.append(start_node)

        while len(open_nodes) > 0:
            
            current = self.get_node_with_lowest_f_cost(open_nodes)
            #print("Current: %s" % current.to_string())
            open_nodes.remove(current)
            closed_nodes.append(current)

            if current == target_node:
                print("Found target. yay!")
                self.print_path(current)
                self.print_parents()
                #self.print_map(open_nodes, closed_nodes, current, size)
                sys.exit()
            
            for nx in self.get_range(current.x, size):
                for ny in self.get_range(current.y, size):
                    neighbour = self.tilelist[nx][ny]

                    if self.contains(neighbour, closed_nodes):
                        continue

                    if neighbour == current:
                        continue

                    if not neighbour.traversable:
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
        
            

    def print_path(self, node):
        while True:
            print(node.to_string())
            node = node.parent
            if node == None:
                break

    def remove_from_list(self, node, list):
        if self.contains(node, list):
            list.remove(node)

    def add_to_list(self, node, list):
        if not self.contains(node, list):
            list.append(node)

    def print_map(self, o, c, curr, s):
        for x in range(0, s):
            for y in range(0, s):
                node = self.tilelist[x][y]
                if node == curr:
                    sys.stdout.write("@")
                elif self.contains(node, o):
                    sys.stdout.write("A")
                elif not node.traversable:
                    sys.stdout.write("U")
                elif self.contains(node, c):
                    sys.stdout.write("C")
                else:
                    sys.stdout.write("#")
            print("")

    def print_parents(self):
        for x in range(0, 5):
            for y in range(0, 5):
                node = self.tilelist[x][y]
                if node.parent == None:
                    sys.stdout.write(" # ")
                    continue
                if node.x > node.parent.x:        # parent is to the left
                    if node.y > node.parent.y:    # parent is above
                        sys.stdout.write(" ↖ ")
                    elif node.y == node.parent.y: # parent on same row
                        sys.stdout.write(" ↑ ")
                    else:                         # parent is below
                        sys.stdout.write(" ↙ ") 
                elif node.x == node.parent.x:     # parent is on same column
                    if node.y > node.parent.y:    # parent is above
                        sys.stdout.write(" ← ")
                    elif node.y == node.parent.y: # parent on the same row
                        pass # this should never happen
                    else:                         # parent is below
                        sys.stdout.write(" → ")
                else:                             #parent is to the right
                    if node.y > node.parent.y:    # parent is above
                        sys.stdout.write(" ↗ ")
                    elif node.y == node.parent.y: # parent on same row
                        sys.stdout.write(" ↓ ")
                    else:                         # parent is below
                        sys.stdout.write(" ↘ ") 
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
            max = size

        return range(min, max)

if __name__ == '__main__':
    GraphSearch()
