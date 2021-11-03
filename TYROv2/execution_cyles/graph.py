import astor
import graphviz

from node import Node

COLORS = ['red', 'green']


class Graph:

    def __init__(self):
        self.root = None
        self.nodeID = 0
        self.nodes = []
        self.sub_graphs = []

    def hasCylces(self):
        return False

    def getCycleNodes(self):
        return False

    def addNode(self, new_node: Node):
        if new_node.ast_node and new_node.code_in_string:
            self.node.append(new_node)

    def create_new_node(self, node_ast, exp="", parent=None):
        node = Node()
        node.id = self.nodeID
        self.nodeID += 1
        node.label = exp
        node.ast_node = node_ast
        node.code_in_string = astor.to_source(node_ast)
        node.parent = parent
        self.nodes.append(node)
        return node

    def addNodes(self, node: Node):
        self.nodes.append(node)

    def get_all_parents(self, node: Node):
        parents = []
        currPointer = node
        while currPointer:
            if currPointer.parent_loop_node:
                parents.append(currPointer.parent_loop_node)
            currPointer = currPointer.parent_loop_node
        return parents



    def get_graph_pdf(self):
        not_visited_queue = []  # FIFO
        dot = graphviz.Digraph(comment="Preview")
        not_visited_queue.append(self.root)
        visited = []
        while not_visited_queue:
            currNode = not_visited_queue.pop(0)
            visited.append(currNode.id)
            if currNode.id not in visited:
                dot.node(str(currNode.id), currNode.label)
            for eachNext in currNode.next:
                if eachNext.id not in visited:
                    dot.node(str(eachNext.id), eachNext.label)
                    visited.append(eachNext.id)
                    not_visited_queue.append(eachNext)
                dot.edge(str(currNode.id), str(eachNext.id), constraints='false')

        for eachNode in self.nodes:
            if eachNode.parent_loop_node:
                parents = self.get_all_parents(eachNode)
                for p in parents:
                    for loop_val in eachNode.loop_variables:
                        if loop_val in p.loop_variables:
                            print(loop_val, "Compare", p.loop_variables)
                            print(eachNode.id, p.id)
                            dot.edge(str(eachNode.id), str(p.id), constraints='false',color=COLORS[1], arrowsize='3')
                # for loop_val in eachNode.loop_variables:
                #     if loop_val in eachNode.parent_loop_node.loop_variables:
                #         dot.edge(str(eachNode.id), str(eachNode.parent_loop_node.id), color=COLORS[1])
        print(dot.source)
        dot.render('test-output/round-table.gv', view=True)  # doctest: +SKIP
        'test-output/round-table.gv.pdf'

    def print_graph(self):
        not_visited_queue = []  # FIFO
        visited = []
        if self:
            not_visited_queue.append(self.root)
            while not_visited_queue:
                currNode = not_visited_queue.pop(0)
                visited.append(currNode.id)
                print(str(currNode.id) + " " + currNode.label + "-->")
                for eachNext in currNode.next:
                    if eachNext.id not in visited:
                        not_visited_queue.append(eachNext)