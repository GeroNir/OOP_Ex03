import json
from collections import defaultdict
import string

# TODO: exceptions
from typing import cast


class DiGraph:

    def load(self, file):
        with open(file) as b1:
            f = json.load(b1)
        tmpEdges = f['Edges']
        tmpNodes = f['Nodes']
        self.Edges = {}
        self.Nodes = {}
        self.nodeSize = len(tmpNodes)
        self.edgeSize = len(tmpEdges)
        self.MC = 0
        self.outEdges = []
        self.inEdges = []
        for n in tmpNodes:
            self.outEdges.insert(0, [])
            self.inEdges.insert(0, [])
            self.Nodes[n['id']] = n
        for e in tmpEdges:
            key = str(e['src']) + "," + str(e['dest'])
            self.inEdges[e['dest']].insert(0, e)
            self.outEdges[e['src']].insert(0, e)
            self.Edges[key] = e
        # tmpIn = {}
        # tmpOut = {}
        # for e in self.inEdges:
        #     key = e[0]['dest']
        #     tmpIn[key] = e
        # for e in self.outEdges:
        #     key = e[0]['src']
        #     tmpOut[key] = e
        # self.outEdges = tmpOut
        # self.inEdges = tmpIn

    def __init__(self):
        self.Edges = {}
        self.Nodes = {}
        self.nodeSize = 0
        self.edgeSize = 0
        self.MC = 0
        self.outEdges = {}
        self.inEdges = {}
        tmpIn = {}
        tmpOut = {}
        self.visited = []

    def v_size(self) -> int:
        return self.nodeSize

    def e_size(self) -> int:
        return self.edgeSize

    def get_all_v(self):
        return self.Nodes

    def all_in_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.inEdges[id]
        return tmp

    def all_out_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.outEdges[id]
        return tmp

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, src: int, dest: int, weight: float) -> bool:
        # check if the edge is already exists
        key = str(src) + "," + str(dest)
        try:
            self.Edges[key]
            return False
        except:
            try:
                self.Nodes[src]
                self.Nodes[dest]
                e = {}
                e['src'] = src
                e['w'] = weight
                e['dest'] = dest
                self.Edges[key] = e
                self.inEdges[e['dest']] = e
                self.outEdges[e['src']] = e
                self.MC += 1
                self.edgeSize += 1
                return True
            except:
                return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:  # O(n) n = nodeSize
        try:
            self.Nodes[node_id]
            return False
        except:
            n = {}
            n["pos"] = pos
            n["id"] = node_id
            self.Nodes[node_id] = n
            self.MC += 1
            self.nodeSize += 1
            # self.inEdges[node_id] = n
            # self.outEdges[node_id] = n
            return True

    def remove_node(self, node_id: int) -> bool:
        rm = self.Nodes.pop(node_id, None)
        if (rm != None):
            for e in self.inEdges[node_id]:
                key = str(e['src']) + "," + str(e['dest'])
                self.Edges.pop(key)
            for e in self.outEdges[node_id]:
                key = str(e['src']) + "," + str(e['dest'])
                self.Edges.pop(key)
            self.nodeSize -= 1
            self.edgeSize -= len(self.inEdges[node_id]) + len(self.outEdges[node_id])
            self.MC = 1 + len(self.inEdges[node_id]) + len(self.outEdges[node_id])
            del self.inEdges[node_id]
            del self.outEdges[node_id]
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        key = str(node_id1) + "," + str(node_id2)
        rm = self.Edges.pop(key, None)
        if (rm != None):
            del self.outEdges[node_id1]
            del self.inEdges[node_id2]
            self.MC += 1
            return True
        return False

    def __repr__(self):
        return f'DiGraph\nEdges:\n{self.Edges}\nNodes:\n{self.Nodes}'

    def get_node(self, node_id: int):
        return self.get_all_v().get(node_id)

    def get_pos(self, node_id: int):
        return self.get_node(node_id).get('pos')

    def get_x(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[0])

    def get_y(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[1])

    def get_z(self, node_id: int):
        s = self.get_pos(node_id)
        s: cast(string, s)
        s = s.split(',')
        return float(s[2])