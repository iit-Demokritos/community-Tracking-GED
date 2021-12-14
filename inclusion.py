# -*- coding: utf-8 -*-
import networkx as nx


class Inclusion():

    def __init__(self, g1, g2):
        self.inclusion = None
        self.inverse_inclusion = None
        self.g1 = g1
        self.g2 = g2

    def compute_inclusion(self, ):
        inclusion, inversed_inclusion = self.find_inclusions(self.g1, self.g2)
        self.inclusion = inclusion
        self.inversed_inclusion = inversed_inclusion
        return inclusion, inversed_inclusion

    def find_inclusions(self, g1, g2):
        pass

    def get_inlcusion(self, ):
        return self.inclusion

    def get_inv_inclusion(self, ):
        return self.inverse_inclusion

    def find_intersection(self, g1, g2):
        return (list(set(g1.nodes()) & set(g2.nodes())))

    def find_group_quantity(self, intersection, g1):
        return (len(intersection) /
                          float(g1.number_of_nodes()))

    def find_group_quality(self, intersection, g1):
        intersection_sum = sum([g1._node[node]['centrality'] for node in intersection])
        g1_sum = sum([d['centrality'] for node,d in g1.nodes(data=True)])
        if (not g1_sum): return 0
        return intersection_sum / g1_sum


class SocialPositionInclusion(Inclusion):

    def __init__(self, g1, g2):
        Inclusion.__init__(self, g1, g2)

    def find_inclusions(self, g1, g2):
        g1_with_sp = self.compute_social_position(g1, 0.85, 40)
        g2_with_sp = self.compute_social_position(g2, 0.85, 40)
        intersection = self.find_intersection(g1_with_sp, g2_with_sp)
        inclusion = (self.find_group_quantity(intersection, g1_with_sp) *
                     self.find_group_quality(intersection, g1_with_sp))
        inv_inclusion = (self.find_group_quantity(intersection, g2_with_sp) *
                     self.find_group_quality(intersection, g2_with_sp))
        return inclusion, inv_inclusion

    def compute_social_position(self, initial_graph, alpha, iterations):
        num_nodes = len(initial_graph)
        graph = self.initialize_sp(initial_graph)
        for _ in range(iterations):
            previous_sum = sum([d['centrality'] for n,d in graph.nodes_iter(data=True)])
            for node,d  in graph.nodes_iter(data=True):
                sp = 0.0
                neighbors = len(graph.neighbors(node))
                for neighbor in graph.neighbors(node):
                    sp += (1.0 / neighbors) * graph.node[neighbor]['centrality']#*edge_weight
                d['centrality'] = alpha * sp + (1 - alpha) / num_nodes
            new_sum = sum([d['centrality'] for n,d in graph.nodes(data=True)])
            if 0.00001 > abs(new_sum - previous_sum):
                #print '[INFO]: Converged in %s iterations...' % _
                return graph
        return graph

    def initialize_sp(self, graph):
        for n,d in graph.nodes_iter(data=True):
            d['centrality'] = 1.0
        return graph


class CentralityInclusion(Inclusion):

    def __init__(self, g1, g2):
        Inclusion.__init__(self, g1, g2)

    def find_degree(self, initial_graph):
        #degrees_dict = nx.pagerank(initial_graph, alpha=0.9)
        degrees_dict = nx.degree_centrality(initial_graph)
        for node, value in degrees_dict.items():
            initial_graph._node[node]['centrality'] = value
        return initial_graph

    def find_inclusions(self, g1, g2):
        g1_with_degrees = self.find_degree(g1)
        g2_with_degrees = self.find_degree(g2)
        intersection = self.find_intersection(g1_with_degrees, g2_with_degrees)
        inclusion = (self.find_group_quantity(intersection, g1_with_degrees) *
                     self.find_group_quality(intersection, g1_with_degrees))
        inv_inclusion = (self.find_group_quantity(intersection, g2_with_degrees) *
                     self.find_group_quality(intersection, g2_with_degrees))
        return inclusion, inv_inclusion
