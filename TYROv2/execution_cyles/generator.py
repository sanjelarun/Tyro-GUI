from graph import Graph
import ast
import astor
from node import Node

STATEMENT_INSTANCES = [ast.Expr, ast.Assign, ast.AugAssign]
LOOP_INSTANCES = [ast.For, ast.While]


def print_graph(graph: Graph):
    not_visited_queue = []  # FIFO
    visited = []
    if graph:
        not_visited_queue.append(graph.root)
        while not_visited_queue:
            currNode = not_visited_queue.pop(0)
            visited.append(currNode.id)
            print(str(currNode.id) + " " + currNode.label + "-->" )
            for eachNext in currNode.next:
                if eachNext.id not in visited:
                    not_visited_queue.append(eachNext)


def is_func_def(astNode):
    if isinstance(astNode, ast.FunctionDef):
        return True
    return False


def is_loop(astNode):
    if astNode.__class__ in LOOP_INSTANCES:
        return True
    return False


def is_statement(astNode):
    if astNode.__class__ in STATEMENT_INSTANCES:
        return True
    return False


def get_loop_variables(loopNode):
    return loopNode.target.id


def get_count_variables(loopNode):
    if loopNode.iter.args[0].__class__ == ast.Name :
        return loopNode.iter.args[0].id
    return None


def convert_loop_expression_to_graph(loop_node_ast, parentNode : Node, graph):

    mainNode = graph.create_new_node(node_ast=loop_node_ast,
                                     exp=get_expression_from_node(loop_node_ast),
                                     parent=parentNode)
    tmp = get_loop_variables(loop_node_ast)
    if tmp is not None:
        mainNode.add_variables(tmp)
    tmp = get_count_variables(loop_node_ast)
    if tmp is not None:
        mainNode.add_variables(tmp)
    currNode = mainNode
    loopNode = mainNode
    for a in loop_node_ast.body:
        #currNode = parentNode
        # hello = astor.to_source(a)
        flag = check_ast_for_type(a)
        if flag == 1:
            newNode = convert_loop_expression_to_graph(a, currNode, graph)
            newNode.set_parent_loop(loopNode)
            tmp = get_loop_variables(a)
            if tmp is not None:
                newNode.add_variables(tmp)
            tmp = get_count_variables(a)
            if tmp is not None:
                newNode.add_variables(tmp)
            currNode.set_next_node(newNode)
            currNode = newNode
            loopNode = newNode
        elif flag == 2:
            exp = graph.create_new_node(node_ast=a, exp=get_expression_from_node(a), parent=currNode)
            currNode.set_next_node(exp)
            currNode = exp
        elif flag == 3:
            currNode.set_next_node(None)
    currNode.set_next_node(mainNode)
    return mainNode


def get_expression_from_node(astNode):
    source_code = astor.to_source(astNode).split("\n")[0]
    return source_code


def check_ast_for_type(astNode):
    if is_loop(astNode):
        return 1
    elif is_statement(astNode):
        return 2
    elif is_func_def(astNode):
        return 3
    return -1, None


def convert_graph_to_struct(source_filepath):
    convertedGraph = Graph()
    test = astor.code_to_ast.parse_file(source_filepath)
    rootNode = convertedGraph.create_new_node(node_ast=test.body[0], exp=get_expression_from_node(test.body[0]))
    convertedGraph.root = rootNode
    currNode = rootNode
    for a in test.body[1:]:
        # hello = astor.to_source(a)
        flag = check_ast_for_type(a)
        if flag == 1:
            #currNode.set_next_node(node)
            newNode =  convert_loop_expression_to_graph(a, currNode, convertedGraph)
            newNode.set_parent_loop(currNode)
            newNode.add_variables(get_loop_variables(a))
            newNode.add_variables(get_count_variables(a))
            currNode.set_next_node(newNode)
            currNode = newNode
        elif flag == 2:
            newNode = convertedGraph.create_new_node(a, exp=get_expression_from_node(a), parent=currNode)
            currNode.set_next_node(newNode)
            currNode =  newNode
        elif flag == 3:
            newNode = convertedGraph.create_new_node(a, exp=get_expression_from_node(a), parent=currNode)
            currNode.set_next_node(newNode)
            currNode = newNode
    return convertedGraph


filepath = "/home/sanjelarun/Tyro_GUI/Tyro-GUI/TYROv2/execution_cyles/add-numbers-1.py"
root = convert_graph_to_struct(filepath)
print_graph(root)

root.get_graph_pdf()
