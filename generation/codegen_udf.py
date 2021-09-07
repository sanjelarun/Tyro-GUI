def codegen_complete_mapper(target, mapper_operations, input_data):
    """
     Code Generation for all Map stage synthesis
    :param target: target operations
    :param mapper_operations: All Map operation
    :param input_data: Given Data
    :return: List of all converted Mapper
    """
    count = 0
    complete_code = []
    final_RDD =  target +"_RDD_"
    if len(input_data) == 0:
        tmp = final_RDD + str(count) + " = sc.parallelize(" + target + ")"
    else:
        tmp = final_RDD + str(count) + " = sc.parallelize(" + input_data + ")"
    complete_code.append(tmp)
    count += 1
    for each_mapper in mapper_operations[:-1]:
        tmp = final_RDD + str(count) + " = " + final_RDD + str(count - 1) + each_mapper
        count += 1
        complete_code.append(tmp)
    tmp = target + " = " + final_RDD + str(count - 1) + mapper_operations[-1]
    complete_code.append(tmp)
    return complete_code


def codegen_complete_mapper_filter(target, mapper_operations):
    """
     Code generation for all map with filter synthesis
    :param target: target operations
    :param mapper_operations: Map with filter operations
    :return: List of converted code
    """
    count = 0
    complete_code = []
    final_RDD = target + "_RDD_"
    tmp = final_RDD + str(count) + " = sc.parallelize(" + target + ")"
    complete_code.append(tmp)
    count += 1
    for each_mapper in mapper_operations:
        tmp = final_RDD + str(count) + " = " + final_RDD + "0" + each_mapper
        count += 1
        complete_code.append(tmp)
    s = target + " = " + "sc.union(["
    for i in range(count - 1):
        s += final_RDD + str(i + 1) + ","
    s += "])"
    complete_code.append(s)
    return complete_code


def codegen_complete_reducer(target, mr_operations, input_datset):
    """
     Code conversion for Reduce stage of Synthesis
    :param target: Target operations
    :param mr_operations: Converted reduced operations
    :param input_datset: The data set that needs to converted to RDD
    :return: list of generated operation
    """
    count = 0
    complete_code = []
    final_RDD = target
    tmp = final_RDD + str(count) + " = sc.parallelize(" + input_datset + ")"
    complete_code.append(tmp)
    count += 1
    for each_mapper in mr_operations[:-1]:
        tmp = final_RDD + str(count) + " = " + final_RDD + "0" + each_mapper
        count += 1
        complete_code.append(tmp)
    tmp = final_RDD + " = " + final_RDD + "0" + mr_operations[-1]
    # s = target + " = " + "sc.union(["
    # for i in range(count - 1):
    # s += final_RDD + str(i + 1) + ","
    # s += "])"
    # complete_code.append(s)
    complete_code.append(tmp)
    return complete_code


def codegen_complete_reducer_multiple_mapper(target, list_of_mapper):
    """
    Code conversion for multiple mapper in a same loop
   :param target: target operations list
   :param list_of_mapper: List of all mapper that needs to converted
   :return:
    """
    count = 0
    complete_code = []
    final_RDD = target + "_RDD_"
    for i in list_of_mapper:
        tmp = final_RDD + str(count) + " = sc.parallelize(" + i + ")"
        complete_code.append(tmp)
        count += 1
    tmp = final_RDD+str(count) + " = " + final_RDD + str(count - 1) + ".zip(" + final_RDD + "0)"
    complete_code.append(tmp)
    # s = target + " = " + "sc.union(["
    # for i in range(count - 1):
    # s += final_RDD + str(i + 1) + ","
    # s += "])"
    # complete_code.append(s)
    tmp = target + " = " + final_RDD + str(count) + ".map(lambda x: (1, (x[0],x[1]))).reduceByKey(udf).collect()"
    complete_code.append(tmp)
    return complete_code


def write_all(replace, a):
    for s in replace:
        a.write("    " + s + "\n")


def code_gen_file(filepath, intial_num, final_num, codelist, type, function_def=""):
    """
    Generates PySpark
    :param filepath: Input Python Program
    :param intial_num:  Initial line number
    :param final_num:  Final line number
    :param codelist: List of all translated code
    :param type: Type of Synthesis ( Stages)
    :param function_def: function def name
    :return: pass
    """
    fin = open(filepath, "rt")
    fout = open("result/gen.py", "wt")
    cnt = 0
    fout.write("import pyspark as ps\n")
    if type == 5:
        for each in function_def:
            fout.write(each)
    for i, line in enumerate(fin):
        if not (intial_num <= i + 1 <= final_num):
            fout.write(line)
        else:
            if cnt == 0:
                fout.write("    sc = ps.SparkContext()\n")
                for s in codelist:
                    fout.write("    " + s + "\n")
                cnt = 1