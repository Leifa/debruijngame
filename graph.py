from node import Node
import random

class Graph:

    def __init__(self, nodes, green, red):
        self.nodes = nodes
        self.red = red
        self.green = green

    def add_red_edge(self, edge):
        if edge not in self.red:
            self.red.append(edge)

    def add_green_edge(self, edge):
        if edge not in self.green:
            self.green.append(edge)

    def remove_node(self, node):
        self.nodes.remove(node)
        edges_to_remove = []
        for edge in self.red:
            if node in edge:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.red.remove(edge)
        edges_to_remove = []
        for edge in self.green:
            if node in edge:
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            self.green.remove(edge)

    def add_product_node(self, node1, node2):
        px = (node1.pos[0] + node2.pos[0]) / 2
        py = (node1.pos[1] + node2.pos[1]) / 2
        product = Node((px, py))
        self.nodes.append(product)
        # red successors
        for edge in self.red:
            if edge[0] == node1 or edge[0] == node2:
                if (product, edge[1]) not in self.red:
                    self.red.append((product, edge[1]))
        # green successors
        for edge in self.green:
            if edge[0] == node1 or edge[0] == node2:
                if (product, edge[1]) not in self.green:
                    self.green.append((product, edge[1]))
        # red preds
        for edge1 in self.red:
            for edge2 in self.red:
                if edge1[0] == edge2[0]:
                    if edge1[1] == node1 and edge2[1] == node2:
                        if (edge1[0], product) not in self.red:
                            self.red.append((edge1[0], product))
        # green preds
        for edge1 in self.green:
            for edge2 in self.green:
                if edge1[0] == edge2[0]:
                    if edge1[1] == node1 and edge2[1] == node2:
                        if (edge1[0], product) not in self.green:
                            self.green.append((edge1[0], product))

    def has_red_edge(self, node1, node2):
        return (node1, node2) in self.edges

    def randomize_positions(self, width, height):
        for node in self.nodes:
            node.pos = (random.randint(0,width), random.randint(0,height))

    @staticmethod
    def pattern(n, code):
        nodes = [Node((300 * (i + 1) % 810, 100 * (i + 1) % 690)) for i in range(0, n)]
        red = []
        green = []
        for i in range(n):
            for j in range(n):
                if code % 2 == 1:
                    green.append((nodes[i],nodes[j]))
                code = code // 2
        for i in range(n):
            for j in range(n):
                if code % 2 == 1:
                    red.append((nodes[i], nodes[j]))
                code = code // 2
        return Graph(nodes, green, red)