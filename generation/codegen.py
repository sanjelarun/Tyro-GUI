import ast

from model.models import LoopReplace


# Lets start codegen with no verification or anything just to test the my analysis works or not
def mapper_reducer_generation(program_information):
    """
    Generates all map and reduce required.
    :param program_information: the whole Meta-information
    :return: All converted Python operations to PySpark operations
    """

    list_of_new_operations = []
    s = ''
    initial_number = 0
    final_number = 0
    for functions in program_information.all_functions:
        for iteration in functions.iteration:
            initial_number = iteration.initial_line_number
            final_number = iteration.final_line_number
            for ops in iteration.operations:
                if isinstance(ops.op, ast.Add) and ops.ops == "ADD":
                    changeRDD = ops.left + '_RDD = sc.parallelize(' + 'numbers' + ')'
                    list_of_new_operations.append(changeRDD)
                    # s += ops.left + '=' + ops.left + '_RDD.map(lambda x:(1, x)).reduceByKey(lambda accum, num: accum + num).collect()'
                    s += ops.left + '=' + ops.left + '_RDD.sum()'
                    list_of_new_operations.append(s)
                    s = ''
                elif isinstance(ops.op, ast.Add) and ops.ops == "COUNT":
                    changeRDD = ops.left + '_RDD = sc.parallelize(' + 'numbers' + ')'
                    list_of_new_operations.append(changeRDD)
                    # s += ops.left + '=' + ops.left + '_RDD.map(lambda x:(1, x)).reduceByKey(lambda accum, _: accum +' + ops.right + ').collect()'
                    s += ops.left + '=' + ops.left + '_RDD.count()'
                    list_of_new_operations.append(s)
                    s = ''
                elif isinstance(ops.op, ast.Lt) and ops.ops == "MAX":
                    changeRDD = ops.left + '_RDD = sc.parallelize(' + 'numbers' + ')'
                    list_of_new_operations.append(changeRDD)
                    # s += ops.left + '=' + ops.left + '_RDD.map(lambda x:(1, x)).reduceByKey(lambda accum, _: accum +' + ops.right + ').collect()'
                    s += ops.left + '=' + ops.left + '_RDD.max()'
                    list_of_new_operations.append(s)
                    s = ''
                elif isinstance(ops.op, ast.Gt) and ops.ops == "MIN":
                    changeRDD = ops.left + '_RDD = sc.parallelize(' + 'numbers' + ')'
                    list_of_new_operations.append(changeRDD)
                    # s += ops.left + '=' + ops.left + '_RDD.map(lambda x:(1, x)).reduceByKey(lambda accum, _: accum +' + ops.right + ').collect()'
                    s += ops.left + '=' + ops.left + '_RDD.min()'
                    list_of_new_operations.append(s)
                    s = ''
    return LoopReplace(initial_number, final_number, list_of_new_operations)


def write_all(replace, fout):
    for s in replace:
        fout.write("    " + s + "\n")


def codeGen(replace, filepath):
    """
    Generate a PySpark program

    Parameters:
    replace: the contents to replace with
    filepath: Old Filepath

    """
    fin = open(filepath, "rt")
    fout = open("../result/gen.py", "wt")
    cnt = 0
    fout.write("import pyspark as ps\n")
    for i, line in enumerate(fin):
        if not (replace.initial_line_no <= i + 1 <= replace.final_line_number):
            fout.write(line)
        else:
            if cnt == 0:
                fout.write("    sc = ps.SparkContext()\n")
                write_all(replace.replace_strings,fout)
                cnt += 1