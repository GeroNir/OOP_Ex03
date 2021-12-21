import json
from collections import defaultdict


# TODO: exceptions

class DiGraph:

    def __init__(self, file):
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
        tmpIn = {}
        tmpOut = {}
        print(self.inEdges)
        for e in self.inEdges:
            key = e[0]['dest']
            tmpIn[key] = e
        for e in self.outEdges:
            key = e[0]['src']
            tmpOut[key] = e

        self.outEdges = tmpOut
        self.inEdges = tmpIn
    def v_size(self) -> int:
        return self.nodeSize

    def e_size(self) -> int:
        return self.edgeSize

    def get_all_v(self):
        return self.Nodes

    def all_in_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.inEdges.get(id)
        return tmp

    def all_out_edges_of_node(self, id) -> dict:
        tmp = {}
        tmp[id] = self.outEdges.get(id)
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
            e = {}
            e['src'] = src
            e['w'] = weight
            e['dest'] = dest
            self.Edges[key] = e
            self.inEdges[e['dest']].insert(e)
            self.outEdges[e['src']].insert(e)
            self.MC += 1
            self.edgeSize += 1
            return True

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
            for n in self.inEdges[node_id2]:
                if n['dest'] == node_id2 and n['src'] == node_id1:
                    self.inEdges[node_id2].remove(n)
            for n in self.outEdges[node_id1]:
                if n['dest'] == node_id2 and n['src'] == node_id1:
                    self.outEdges[node_id1].remove(n)
            return True
        return False

file = r'C:\Users\Hagai\PycharmProjects\OOP_Ex4\data\A0.json'
g = DiGraph(file)
print(g.v_size())
print(g.e_size())
print(g.Edges)
print(g.get_all_v())
print(g.all_in_edges_of_node(0))
print("")
print(g.all_out_edges_of_node(1))
print(g.get_mc())
print(g.add_edge(5, 6, 1.7389217398173891))
print(g.all_in_edges_of_node(6))
#print(g.add_node(12, (35.18753, 32.1037822, 0.0)))
print("")
print(g.remove_node(0))
print(g.all_in_edges_of_node(0))
print(g.all_out_edges_of_node(0))
print(g.get_all_v())
print(g.Edges)
print(g.nodeSize)
print(g.edgeSize)
print(g.get_mc())
print(g.remove_edge(1,2))