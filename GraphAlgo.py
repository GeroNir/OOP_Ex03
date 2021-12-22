import math
import random
from queue import Queue
from typing import List

from DiGraph import DiGraph
from src import GraphInterface
import json
import matplotlib as gui


class GraphAlgo():

    def __init__(self):
        self.graph = DiGraph()

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:

        try:
            with open(file_name) as b1:
                f = json.load(b1)
            tmpEdges = f['Edges']
            tmpNodes = f['Nodes']
            self.graph.Edges = {}
            self.graph.Nodes = {}
            self.graph.nodeSize = len(tmpNodes)
            self.graph.edgeSize = len(tmpEdges)
            self.graph.MC = 0
            self.graph.outEdges = []
            self.graph.inEdges = []
            for n in tmpNodes:
                self.graph.outEdges.insert(0, [])
                self.graph.inEdges.insert(0, [])
                self.graph.Nodes[n['id']] = n
            for e in tmpEdges:
                key = str(e['src']) + "," + str(e['dest'])
                self.graph.inEdges[e['dest']].insert(0, e)
                self.graph.outEdges[e['src']].insert(0, e)
                self.graph.Edges[key] = e
            # tmpIn = {}
            # tmpOut = {}
            # for e in self.graph.inEdges:
            #     key = e[0]['dest']
            #     tmpIn[key] = e
            # for e in self.graph.outEdges:
            #     key = e[0]['src']
            #     tmpOut[key] = e
            # self.graph.outEdges = tmpOut
            # self.graph.inEdges = tmpIn
        except NotImplementedError:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        dist, prev = self.dijkstra(id1)
        shortest_path = dist[id2]
        tmp = prev[id2]
        ans = []
        ans.insert(0, id2)
        ans.insert(0, tmp)
        while tmp != id1:
            tmp = prev[tmp]
            ans.insert(0, tmp)
        return shortest_path, ans

    def isConnected(self) -> bool:
        bool = self.BFS_check()
        if bool:
            self.getTranspose()
            bool = self.BFS_check()
            if bool:
                return True
            else:
                self.getTranspose()
        return False

    def dijkstra(self, src):
        visited = {}
        prev = {}
        queue = Queue()
        dist = {}
        for n in self.get_graph().get_all_v():
            dist[n] = float('inf')
            visited[n] = False
        dist[src] = 0
        queue.put(src)
        while not queue.empty():
            curr = queue.get()
            if visited.get(curr) is False:
                for e in self.get_graph().Edges.values():
                    distance = dist[curr] + float(e['w'])
                    if distance < dist[int(e['dest'])] and e['src'] == curr:
                        dist[int(e['dest'])] = distance
                        prev[e['dest']] = int(e['src'])
                        queue.put(int(e['dest']))
            visited[curr] = True
        return dist, prev

    def BFS_check (self) -> bool:
        queue = Queue()
        queue.put(self.graph.Nodes[0]['id'])
        visited = []
        visited.append(self.graph.Nodes[0]['id'])
        while not queue.empty():
            check = queue.get()
            for e in self.graph.Edges:
                if self.get_graph().Edges[e]['src'] == check:
                    dest = self.graph.Edges[e]['dest']
                    if dest in visited:
                        pass
                    else:
                        queue.put(dest)
                        visited.append(dest)
        if len(visited) == self.graph.nodeSize:
            return True
        else:
            return False

    def dijkstra_max(self, src):
        dist, prev = self.dijkstra(src)
        max = -1
        i = 0
        indx = 0
        for d in dist.values():
            if max < d:
                max = d
                indx = i
                i += 1
        return indx, max

    def dijkstra_dist(self, src):
        visited = {}
        prev = {}
        queue = Queue()
        dist = {}
        for n in self.get_graph().get_all_v():
            dist[n] = float('inf')
            visited[n] = False
        dist[src] = 0
        queue.put(src)
        while not queue.empty():
            curr = queue.get()
            if visited.get(curr) is False:
                for e in self.get_graph().Edges.values():
                    distance = dist[curr] + float(e['w'])
                    if distance < dist[int(e['dest'])]:
                        dist[int(e['dest'])] = distance
                        prev[int(e['dest'])] = int(e['src'])
                        queue.put(int(e['dest']))
            visited[curr] = True
        return dist

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        dist = []
        min_dist = float('inf')
        for n in self.get_graph().get_all_v().values():
            dist.insert(int(n['id']), self.dijkstra_dist(int(n['id'])))
        for n1 in node_lst:
            for n2 in node_lst:
                last_val = dist[n1][n2]
                if (last_val < min_dist and last_val != 0):
                    min_dist = last_val
                    src = n1
                    dest = n2
        ans = []
        node_lst_copy = node_lst.copy()
        ans.append(src)
        ans.append(dest)
        node_lst_copy.remove(src)
        node_lst_copy.remove(dest)
        last = dest
        while len(node_lst_copy) > 0:
            min_dist = float('inf')
            for n in node_lst_copy:
                last_val = dist[last][n]
                if (last_val < min_dist and last_val != 0):
                    min_dist = last_val
                    indx = n
            node_lst_copy.remove(indx)
            ans.append(indx)
            last = indx
        return ans

    def save_to_json(self, file_name: str) -> bool:
        try:
            Edges = []
            Nodes = []
            graph = {}
            for e in self.get_graph().Edges.values():
                Edges.append(e)
            for n in self.get_graph().Nodes.values():
                Nodes.append(n)
            graph['Edges'] = Edges
            graph['Nodes'] = Nodes
            with open(file_name, 'w') as outfile:
                json.dump(graph, outfile, indent=2)
            return True
        except:
            return False

    def getTranspose(self) -> DiGraph:
        new = {}
        for e in self.get_graph().Edges.values():
            tmp = e['src']
            e['src'] = e['dest']
            e['dest'] = tmp
            new[str(e['src']) + "," + str(e['dest'])] = e
        del self.get_graph().Edges
        self.get_graph().Edges = new
        return self.get_graph()

    def centerPoint(self) -> (int, float):
        if self.isConnected():
            cen = []
            for n in self.graph.Nodes:
                cen.append(self.dijkstra_max(n))
            min = float('inf')
            for i in cen:
                if i[1] < min:
                    min = i[1]
                    indx = i[0]
            return indx, min
        else:
            print("The Graph is not Connected")

    def plot_graph(self) -> None:
        graph = self.graph
        for src in graph.get_all_v().keys():
            for dest, w in graph.all_in_edges_of_node(src).items():
                radius = 0.01
                x_src, y_src, z_src = graph.get_node(src).pos
                x_dest, y_dest, z_dest = graph.get_node(dest).pos
                distance = math.sqrt((x_src - x_dest) * 2 + (y_src - y_dest) * 2)
                direction_x = (x_src - x_dest) / distance
                direction_y = (y_src - y_dest) / distance
                x_dest = direction_x * radius + x_dest
                y_dest = direction_y * radius + y_dest
                x_src = direction_x * (-radius) + x_src
                y_src = direction_y * (-radius) + y_src
                gui.arrow(x_src, y_src, (x_dest - x_src), (y_dest - y_src), length_includes_head=True,
                          width=0.003 * distance, head_width=0.1 * distance, color='black')

                for node in graph.get_all_v().values():
                    if node.pos is None:
                        node.pos = (random.uniform(0, 5), random.uniform(0, 5), 0)
                    gui.text(node.pos[0], node.pos[1], str(node.key), horizontalalignment='center',
                             verticalalignment='center',
                             bbox=dict(facecolor='red', edgecolor='black', boxstyle='circle, pad=0.1'))
                gui.show()



g = DiGraph()
algo = GraphAlgo()
# algo.load_from_json('data/not_connected.json')
#print(algo.centerPoint())
algo.load_from_json('data/A0.json')
print(algo.centerPoint())
# print(algo.shortest_path(1,7))
print(algo.shortest_path(1,7))
# algo.plot_graph()

