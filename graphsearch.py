#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from random import randint
import time

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

        size = 50                         

        self.tilelist = []
        self.tilelist = self.init_list(self.tilelist, size)
            

        open_nodes = []  # set of nodes that needs to be evaluated
        closed_nodes = []  # set of nodes that is already evaluated

        start_node = self.tilelist[0][0]
        target_node = self.tilelist[42][49]

        start_node.g = 0
        start_node.h = self.get_cost(start_node, target_node)
        start_node.f = start_node.h

        open_nodes.append(start_node)
        start_time = time.time() 
        self.find_path(open_nodes, closed_nodes, start_node, target_node, size)
        end_time = time.time() - start_time
        print(end_time)

    def find_path(self, open_nodes, closed_nodes, start_node, target_node, size):
         while len(open_nodes) > 0:
                
            current = self.get_node_with_lowest_f_cost(open_nodes)
            #print("Current: %s" % current.to_string())
            open_nodes.remove(current)
            closed_nodes.append(current)

            if current == target_node:
                print("Found target. yay!")
                #self.print_path(current)
                #self.print_parents(self.tilelist)
                #self.print_visual_path(size, current)
                #self.print_map(open_nodes, closed_nodes, current, size)
                return
            
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

    def print_parents(self, nodelist):
        for x in range(0, len(nodelist)):
            for y in range(0, len(nodelist)):
                node = nodelist[x][y]
                if not node.traversable:
                    sys.stdout.write(" X ")
                    continue 
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

    def print_visual_path(self, size, target):
        newlist = self.purge_parents(self.tilelist)
        current = target
        while True:
            newlist[current.x][current.y] = current
            if current.parent == None:
                break
            current = current.parent
        self.print_parents(newlist)


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
    
    def purge_parents(self, parentlist):
        newlist = []
        for x in range(len(parentlist)):
            row = []
            for y in range(len(parentlist)):
                temp = parentlist[x][y]
                row.append(Node(temp.x, temp.y, temp.traversable))
            newlist.append(row)
        return newlist
                
    def init_list(self, emptylist, size):
        for x in range(size):
            temp = []
            for y in range(size):
                r = randint(0,100)
                walkable = True
                if r < 30:
                    walkable = False
                temp.append(Node(x, y, walkable))
            emptylist.append(temp)
        return emptylist

if __name__ == '__main__':
    GraphSearch()
    