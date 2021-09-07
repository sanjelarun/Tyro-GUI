import ast
from model.udf_models import BinOps


class NestedLoop:
    """
    Class NestedLoop is a sub structure used for store nested loop information.
    Not only NestedLoop stores the information it also convert the detects join key.
    """
    def __init__(self):
        self.is_join = False
        self.join_key_index = ""
        self.operations = []
        self.data_1 = ""
        self.data_2 = ""
        self.code_generation = []
        self.ops_body = ast.If
        # check Number

    def variable_check(self, operand):
        if isinstance(operand, ast.Name):
            return operand.id
        elif isinstance(operand, ast.Num):
            return operand.n

    def add_operations(self, bino):
        self.operations.append(bino)

    def check_join(self, node):
        for tmp in ast.walk(node):
            if isinstance(tmp, ast.For):
                self.data_2 = tmp.iter.id
            if isinstance(tmp, ast.If):
                self.is_join = True
                self.join_key_index = 0
                self.ops_body = tmp
                break
        self.code_gen_static()

    def code_gen_static(self):
        self.code_generation.append(self.data_1 + "_RDD = sc.parallelize(" + self.data_1 + ")")
        self.code_generation.append(self.data_2 + "_RDD = sc.parallelize(" + self.data_2 + ")")
        if not self.is_join:
            self.code_generation.append(
                self.data_1 + "_RDD_combine =" + self.data_1 + "_RDD.cartesian(" + self.data_2 + "_RDD)")
        else:
            self.code_generation.append(
                self.data_1 + "_RDD_combine =" + self.data_1 + "_RDD.join(" + self.data_2 + "_RDD)")

    def get_all_operation(self):
        for tmp in ast.walk(self.ops_body):
            try:
                for a in tmp.body:
                    if isinstance(a.value, ast.BinOp):
                        left = self.variable_check(a.value.left)
                        op = a.value.op
                        right = self.variable_check(a.value.right)
                        # target = tmp_node.targets[0].id
                        print(left, op, right, "")
                        binary_operation = BinOps(left, right, "", op)
                        binary_operation.get_operation_from_operator()
                        self.add_operations(binary_operation)
            except:
                print("")

    def convert_operations_mapper_reducer(self):
        var1 = self.data_1 + "_RDD_combine =" + self.data_1+ "_RDD_combine"
        for each_op in self.operations:
            # num = num_RDD_0.join(num_RDD_1).map(lambda x: (x[0], x[1][0] +x[1][1]) ).collect()
            tmp_code = var1 + ".map(lambda x: (x[0],x[1][0]" + each_op.operation + "x[1][1])).collect()"
            self.code_generation.append(tmp_code)
        if len(self.operations) != 0:
            self.code_generation.append("return "+ self.data_1 + "_RDD_combine")
        else:
            self.code_generation.append("return " + self.data_1 + "_RDD_combine.collect()")
        return self.code_generation