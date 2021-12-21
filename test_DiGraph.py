from unittest import TestCase
from DiGraph import DiGraph


class TestDiGraph(TestCase):

    def test_v_size(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual(11, g.v_size())
        g.add_node(11, (1, 2, 3))
        self.assertEqual(12, g.v_size())
        g.add_node(11, (1, 2, 5))
        self.assertEqual(12, g.v_size())
        self.assertEqual(1, g.get_mc())

    def test_e_size(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertEqual(22, g.e_size())
        g.add_edge(0, 3, 5.367)
        self.assertEqual(23, g.e_size())
        g.add_edge(0, 1, 1.32131)
        self.assertEqual(1, g.get_mc())
        self.assertFalse(g.add_edge(15, 0, 3.61786378))

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        ans = g.all_in_edges_of_node(0)
        a1 = ans.get(0)[0]['dest']
        a2 = ans.get(0)[1]['dest']
        self.assertEqual(0, a1)
        self.assertEqual(0, a2)

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        ans = g.all_out_edges_of_node(0)
        a1 = ans.get(0)[0]['src']
        a2 = ans.get(0)[1]['src']
        self.assertEqual(0, a1)
        self.assertEqual(0, a2)

    def test_get_mc(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        g.remove_node(0)
        self.assertEqual(5, g.get_mc())
        g.add_node(0)
        self.assertEqual(6, g.get_mc())
        g.remove_edge(5, 4)
        self.assertEqual(7, g.get_mc())
        g.remove_edge(0, 1)
        self.assertEqual(7, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        g.add_edge(0, 3, 1.463275)
        key = "0,3"
        self.assertEqual(g.Edges[key]['w'], 1.463275)

    def test_add_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        lastValue = g.v_size()
        g.add_node(0, (1, 2, 3))
        self.assertEqual(lastValue, g.v_size())
        self.assertNotEqual(g.get_all_v()[0]['pos'], (1, 2, 3))
        g.add_node(12, (1, 2, 3))
        self.assertEqual(lastValue + 1, g.v_size())

    def test_remove_node(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertTrue(g.remove_node(0))
        self.assertFalse(g.remove_node(0))
        self.assertEqual(5, g.get_mc()) # 5 because it have 4 edges that goes in/out

    def test_remove_edge(self):
        g = DiGraph()
        file = 'data/A0.json'
        g.load(file)
        self.assertTrue(g.remove_edge(0,1))
        self.assertFalse(g.remove_edge(0,1))
        self.assertEqual(1, g.get_mc())  # 5 because it have 4 edges that goes in/out
