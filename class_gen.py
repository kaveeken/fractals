from math import sqrt
import matplotlib.pyplot as plt

class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def rotate(self, trend):
        return Node(self.x, self.y + trend * self.x)
    def translate(self,dx,dy):
        return Node(self.x + dx, self.y + dy)
    def stretch(self,factor_x,factor_y):
        return Node(self.x * factor_x, self.y * factor_y)

def print_nodes(nodes):
    for node in nodes:
        print(node.x, node.y)

def sequence_check(nodes):
    for i in range(1, len(nodes)):
        if nodes[i].x < nodes[i-1].x:
            return i
    return False


class Graph:
    def __init__(self, end_x = 10, end_y = 2):
        self.nodes = [Node(0,0), Node(end_x, end_y)]
        self.trend = end_y / end_x

    def find_longest(self):
        longest = {"length": 0.}
        for i in range(1, len(self.nodes)):
            a = self.nodes[i].x - self.nodes[i-1].x
            b = self.nodes[i].y - self.nodes[i-1].y
            c = sqrt(a * a + b * b)
            if a > 0 and c > longest["length"]:
                longest["index"] = i
                longest["length"] = c
                longest["trend"] = b / a
                longest["loc_x"] = self.nodes[i-1].x
                longest["loc_y"] = self.nodes[i-1].y
                longest["scale_x"] = a
                longest["scale_y"] = b  # flat lines stay flat lines
        return longest

    def apply_generator(self, generator):
        longest = self.find_longest()
        index = longest["index"]
        nodes_stretched = generator.stretch(longest["scale_x"],longest["scale_y"])
        nodes_rotated = [node.rotate(longest["trend"]) for node in nodes_stretched]
        nodes_done = [node.translate(longest["loc_x"], longest["loc_y"]) \
                      for node in nodes_rotated]
        nodes_done.append(self.nodes[index])
        sequence_error = sequence_check(nodes_done)
        while sequence_error:
            # sequence errors get turned into straight up/down lines
            nodes_done[sequence_error].x = nodes_done[sequence_error - 1].x 
            sequence_error = sequence_check(nodes_done)
        self.nodes[index - 1 : index + 1] = nodes_done

    def report(self):
        self.xs = []
        self.ys = []
        for node in self.nodes:
            self.xs.append(node.x)
            self.ys.append(node.y)
        #print_nodes(self.nodes)
        plt.scatter(self.xs, self.ys)
        plt.show()

class Generator:
    def __init__(self, inter_width, inter_heigth):
        self.nodes = [Node(0,0),
                      Node(0.5 - inter_width, inter_heigth),
                      Node(0.5 + inter_width, 0 - inter_heigth),
                      Node(1,0)]
    def stretch(self, factor_x, factor_y):
        return [node.stretch(factor_x, factor_y) for node in self.nodes][:-1]

    def report(self):
        self.xs = []
        self.ys = []
        for node in self.nodes:
            self.xs.append(node.x)
            self.ys.append(node.y)
        print([self.xs,self.ys])
        plt.scatter(self.xs, self.ys)
        plt.show()


test_graph = Graph(10, 0.5)
test_gen = Generator(0.2, 0.3)
#test_gen.report()
for i in range(1000):
    test_graph.apply_generator(test_gen)
test_graph.report()
#test_graph.apply_generator(test_gen)
#test_gen.report()
#test_graph.report()
#test_graph.apply_generator(test_gen)
#test_graph.report()
