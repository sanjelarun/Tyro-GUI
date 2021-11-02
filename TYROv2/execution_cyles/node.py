class Node:
    def __init__(self) -> object:
        self.id = -1
        self.ast_node = ""
        self.code_in_string = ""
        self.next = []
        self.label = ""
        self.parent = []
        self.loop_counter = 0

    def set_next_node(self, next_node):
        self.next.append(next_node)

    def set_parent_node(self, parent_node):
        self.parent.append(parent_node)


    def set_loop_counter(self, count):
        self.loop_counter = count

