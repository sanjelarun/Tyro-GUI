"""
The models defines the meta-information which is extracted using Abstract Syntax Tree (AST).
The meta-information structure has four different substructures: Program Information, Function Information,
Loop Information,and Operation Information.
"""

import ast

from model.nested_loop import NestedLoop


class ProgramInformation:
    """
        The Program Information stores all of the program information like the filename, line number, data sets, a
        nd imports used in the original program.
    """
    filepath = ""

    def __init__(self):
        self.all_functions = []

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_function_node_by_name(self, name):
        for tmp in self.all_functions:
            if tmp.name == name:
                return tmp.node


# Store all function information
class FunctionInformation:
    """
    The class FunctionInformation stores all the information about the functions in the given program
    """
    def __init__(self, node):
        self.name = ""
        self.iteration = []
        self.input_variable = []
        self.return_variable = []  # TODO:  add return type for generation
        self.node = node
        self.return_type = ""


# Store all loop information [Right now it is only for loop]
class LoopInformation:
    """
    The LoopInformation substructure stores all of the information regarding a loop
    including  the  AST  node  for  that  loo
    """

    def __init__(self, initial_line_number: int, final_line_number: int):
        self.loop_variables = ''
        self.allVariables = []
        self.initial_line_number = initial_line_number
        self.final_line_number = final_line_number
        self.operations = []
        self.conditions = []
        self.mainOperations = ""
        self.compareInformation = []
        self.has_nested_loops = False
        self.nested_loop_info = NestedLoop()

    def add_conditions(self, condition):
        self.conditions.append(condition)

    def add_operations(self, operation):
        self.operations.append(operation)

    def add_variables(self, variable):
        self.allVariables.append(variable)

    def add_comapre_information(self, compare_info):
        self.compareInformation.append(compare_info)

    def change_nested_loop(self, val: bool):
        self.has_nested_loops = val

    def check_for_nested(self, node: ast.For)->bool:
        for tmp in ast.walk(node):
            if isinstance(tmp, ast.For):
                return True
        return False

# Operation information stored in (left, op,  right)
class OperationInformation:
    """
    The OperationInformation stores the information about operations along with the filter index if applicable.
    It stores the transformed operationo f the extracted AST node.
    """
    def __init__(self, left, op, right, target, main_ops):
        self.left = left
        self.op = op
        self.right = right
        self.target = target
        self.ops = main_ops


class CompareInformation:
    """
    Stores all if/else condition for us
    """
    def __init__(self, left, ops, compare):
        self.left = left
        self.ops = ops
        self.compare = compare


class LoopReplace:
    """
    Stores all replace line information
    """
    def __init__(self, initial_line_no, final_line_number, replace_strings):
        self.initial_line_no = initial_line_no
        self.final_line_number = final_line_number
        self.replace_strings = replace_strings



class BinOps:
    """
    Stores all of the binary operation inside the loop in a "standard" form.
    The Standard here is defined as target = left operator right.
    """
    left = ""
    right = ""
    target = ""
    operation = ""
    operator = ""

    def __init__(self, left="", right="", target="", operations="", operator=""):
        self.left = left
        self.right = right
        self.target = target
        self.operation = operations
        self.operator = operator


#
class SearchConfig:
    """
    For UDF we need to search for summary and grammar
    """
    def __init__(self):
        self.inbits = 2
        self.arraySize = 4
        self.intRange = 4
        self.loopUnrolled = 4

        self.maxMR = 5
        self.maxEmits = 5
        self.maxTuple = 5
        self.maxRecursionDept = 5


# Variable Information
class VariableInformation:
    def __init__(self, varName, varType):
        self.varName = varName
        self.varType = varType