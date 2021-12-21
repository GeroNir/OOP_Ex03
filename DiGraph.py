import json

#TODO: exceptions

class DiGraph:

    # v_size = 0
    # e_size = 0
    # Edges = {}
    # Nodes = {}

    def __init__(self, file):
        with open(file) as b1:
            f = json.load(b1)
        self.Edges = f['Edges']
        self.Nodes = f['Nodes']
        self.nodeSize = len(self.Nodes)
        self.edgeSize = len(self.Edges)
        self.MC = 0

    def v_size(self) -> int:
       return self.nodeSize

    def e_size(self) -> int:
        return self.edgeSize

    def get_all_v(self):
        return self.Nodes

    def all_in_edges_of_node(self, id) -> dict:
        res = []
        count = 0
        for e in self.Edges:
            if e['dest'] == id:
                res.insert(count, e)
                count += 1
        return res

    def all_out_edges_of_node(self, id)  -> dict:
        res = []
        count = 0
        for e in self.Edges:
            if e['src'] == id:
                res.insert(count, e)
                count += 1
        return res

    def get_mc(self) -> int:
        return self.MC

    def add_edge(self, src: int, dest: int, weight: float) -> bool:
        for e in self.Edges:
            if e['src'] == src and e['dest'] == dest:
                return False
        e = {}
        e['src'] = src
        e['w'] = weight
        e['dest'] = dest
        self.Edges.insert(self.edgeSize, e)
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        for n in self.Nodes:
            if n['id'] == node_id or n['pos'] == pos:
                return False
        n = {}
        n["pos"] = pos
        n["id"] = node_id
        self.Nodes.insert(self.nodeSize, n)
        return True

    def remove_node(self, node_id: int) -> bool:
        for n in self.Nodes:
            if n['id'] == node_id:
                self.Nodes.remove(n)
                return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        for e in self.Edges:
            if e['src'] == node_id1 and e['dest'] == node_id2:
                self.Edges.remove(e)
                return True
        return False
file = r'C:\Users\Hagai\PycharmProjects\OOP_Ex4\data\A0.json'
g = DiGraph(file)
print(g.v_size())
print(g.e_size())
print(g.Edges)
print(g.get_all_v())
print(g.all_in_edges_of_node(0))
print(g.all_out_edges_of_node(1))
print(g.get_mc())
g.add_edge(5,6,1.7389217398173891)
print(g.all_in_edges_of_node(6))
print(g.add_node(12, (35.18753,32.1037822,0.0)))


