class Node:
    def __init__(self) -> object:
        self.id = -1
        self.ast_node = ""
        self.code_in_string = ""
        self.next = []
        self.label = ""
        self.parent = []
        self.loop_counter = 0
        self.loop_variables = []
        self.parent_loop_node = None

    def set_next_node(self, next_node):
        self.next.append(next_node)

    def set_parent_node(self, parent_node):
        self.parent.append(parent_node)


    def set_loop_counter(self, count):
        self.loop_counter = count


    def add_variables(self, val):
        if val not in self.loop_variables:
            self.loop_variables.append(val)

    def set_parent_loop(self, parentNode):
        self.parent_loop_node = parentNode
