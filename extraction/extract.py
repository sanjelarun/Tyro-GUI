from model.models import *
import ast
from model.udf import udf_calls
from generation.codegen_udf import *
from model.nested_loop import NestedLoop


def _compute_interval(node):
    """
    Computes the initial and final linenumber of a node.
    :param node: AST node
    :return: initial and final number
    """
    min_lineno = node.lineno
    max_lineno = node.lineno
    for node in ast.walk(node):
        if hasattr(node, "lineno"):
            min_lineno = min(min_lineno, node.lineno)
            max_lineno = max(max_lineno, node.lineno)
    return min_lineno, max_lineno


# check Number
def variable_check(operand):
    """
    Checks weather variable is number or not
    :param operand: AST node of the operand
    :return: return id if name or  number if number
    """
    if isinstance(operand, ast.Name):
        return operand.id
    elif isinstance(operand, ast.Num):
        return operand.n



def extracted_loops(node, program_info : ProgramInformation):
    """
    Extracts all loops from a function node
    :param node:  Ast node
    :param program_info: Meta-information
    :return: updated meta-information
    """
    if isinstance(node, ast.For):
        min_line_no, max_line_no = _compute_interval(node)
        temp_f = LoopInformation(min_line_no, max_line_no)
        has_compare = check_for_compare(node)
        temp_f.change_nested_loop(temp_f.check_for_nested(node.body[0]))
        # FOR NESTED LOOP
        if temp_f.has_nested_loops:
            temp_f.nested_loop_info.data_1 = node.iter.id
            temp_f.nested_loop_info.check_join(node)
            if temp_f.nested_loop_info.is_join:
                temp_f.nested_loop_info.get_all_operation()
            codegen_list = temp_f.nested_loop_info.convert_operations_mapper_reducer()
            code_gen_file(program_info.filepath, min_line_no-1, max_line_no+1, codegen_list, 1)
            print(temp_f)
            return -2
        else:
            for v_node in ast.walk(node):
                # print(node) get all variables
               # Line 45 - 59 comment
                if isinstance(v_node, ast.Call) and v_node.func.id is not "enumerate":
                    funcName = v_node.func.id
                    assignmentInfo = node.body.pop(0)
                    if isinstance(assignmentInfo.targets[0], ast.Name):
                        final_target = assignmentInfo.targets[0].id
                        try:
                            input_dataset = node.iter.id
                        except:
                            input_dataset = "random" # TODO CHANGE THIS ONE AS WELL
                        #input_dataset = ""
                        udf_calls(program_info.get_function_node_by_name(funcName), "rExpression",final_target, program_info, min_line_no, max_line_no, input_dataset)
                    else:
                        final_target = assignmentInfo.targets[0].value.id
                        udf_calls(program_info.get_function_node_by_name(funcName), "mExpression", final_target, program_info, min_line_no, max_line_no)
                    break
                if isinstance(v_node, ast.Name) and isinstance(v_node.ctx, ast.Store):
                    if not temp_f.allVariables.__contains__(v_node.id):
                        print(v_node.id)
                        temp_f.add_variables(v_node.id)
                # Only for Sum and Count
                if not has_compare:
                    if isinstance(v_node, ast.Assign):
                        print(v_node)
                        if isinstance(v_node.value, ast.BinOp):
                            left = variable_check(v_node.value.left)
                            op = v_node.value.op
                            right = variable_check(v_node.value.right)
                            target = v_node.targets[0].id
                            if target != left:
                                temp = left
                                left = right
                                right = temp
                            print(left, op, right, target)
                            if right == "1" or right == 1:
                                temp_f.add_operations(OperationInformation(left, op, right, target, "COUNT"))
                            else:
                                temp_f.add_operations(OperationInformation(left, op, right, target, "ADD"))
                else:
                    if isinstance(v_node, ast.If):
                        compare_info = CompareInformation(v_node.test.left.id, v_node.test.ops[0], v_node.test.comparators[0].id)
                        temp_f.add_comapre_information(compare_info)
                        print(compare_info)
                        for ifbody in v_node.body:
                            if isinstance(ifbody, ast.Assign):
                                target = ifbody.targets[0].id
                                if isinstance(compare_info.ops,ast.Lt):
                                    temp_f.add_operations(OperationInformation(target, compare_info.ops, "", target,"MAX"))
                                else:

                                    temp_f.add_operations(OperationInformation(target, compare_info.ops, "", target,"MIN"))
        return temp_f
    return None


#
def check_for_compare(node):
    """
    Check if  For Loop has if or any condition
    :param node: AST nod
    :return: return True if the node has a if/else block
    """
    for tmp in ast.walk(node):
        if isinstance(tmp, ast.Compare):
            return True
    return False


#
def funtion_analysis(node, progam_info):
    """
    Extract  function  then searches for loops in it. Store all loop information
    :param node: AST node
    :param progam_info: meta-information
    :return: Updated meta-information
    """
    if isinstance(node, ast.FunctionDef):
        function_info = FunctionInformation(node)
        function_info.name = node.name
        function_info.input_variable.append(node.args.args)
        progam_info.all_functions.append(function_info)
        for x in ast.walk(node):
            loop_information = extracted_loops(x, progam_info)
            if loop_information == -2:
                return
            # CHECK FOR NESTED LOOP HERE

            if loop_information != -1:
                function_info.iteration.append(loop_information)
        # for x in function_info.iteration:
        #     print(x.initial_line_number)
        #     print(x.final_line_number)
        #     print(x.allVariables)
        return function_info


#
def program_analysis(program_information : ProgramInformation, filepath):
    """
     Walks for finding various functions
    :param program_information: Meta-information
    :param filepath: Input File Path
    :return: pass
    """
    program_information.set_filepath(filepath)
    with open(filepath, "rt") as fin:
        tree = ast.parse(fin.read())
    for x in ast.walk(tree):
        if isinstance(x, ast.FunctionDef):
            function_info = funtion_analysis(x, program_information)



#Convert expression extracted to standard one
# def convert_expression_to_standard():
#   return ""