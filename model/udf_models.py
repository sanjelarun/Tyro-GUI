import ast

# Stores Codegen Stuff
class MapperCodeGen:
    def __init__(self):
        self.mr_steps = []

    def add_mapper(self, mapper: str):
        self.mr_steps.append(mapper)


class Condition_info:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.operator = ""
        self.convert_to_standard()

    def convert_to_standard(self):
        if isinstance(self.left, ast.Num):
            tmp = self.left
            self.left = self.right
            self.right = tmp
        self.left = self.left.id
        # self.right = self.right.n

    def convert_to_compare_symbol(self, symb):
        if isinstance(symb, ast.Gt):
            self.operator = ">"
        elif isinstance(symb, ast.GtE):
            self.operator = ">="
        elif isinstance(symb, ast.Lt):
            self.operator = "<"
        elif isinstance(symb, ast.LtE):
            self.operator = "<="
        elif isinstance(symb, ast.Eq):
            self.operator = "=="
        elif isinstance(symb, ast.NotEq):
            self.operator = "!="


class EachFilter:

    def __init__(self, condition, operation, mapper_index):
        self.filter_condition = condition
        self.operation = operation
        self.mapper_index = mapper_index


# Stores all filter information
class FilterInformation:

    def __init__(self):
        self.filter_condition = []
        self.has_else = False
        self.has_if = False
        self.has_elif = False

    def add_filter(self, each_filter: EachFilter):
        self.filter_condition.append(each_filter)


# Binary Operation Store
class BinOps:
    left = ""
    right = ""
    target = ""
    operation = ""
    operator = ""

    def __init__(self, left, right, target, operator):
        self.left = left
        self.right = right
        self.target = target
        self.operator = operator

    def get_operation_from_operator(self):
        if isinstance(self.operator, ast.Add):
            self.operation = "+"
        elif isinstance(self.operator, ast.Sub):
            self.operation = "-"
        elif isinstance(self.operator, ast.Mult):
            self.operation = "*"
        elif isinstance(self.operator, ast.Div):
            self.operation = "/"


# New Function information
class CustomLoopInformation:
    loopVariable = set()
    udf_call_type = ""
    filter_info = FilterInformation()
    mapper_list = MapperCodeGen()
    final_codegen_value = []
    input_dataset = ""
    multipleMapCode = []
    parallilizeList = []
    complexExpression = ""

    def __init__(self, call_type, input_dataset, program_info):
        print(call_type)
        self.udf_call_type = call_type
        self.input_dataset = input_dataset
        self.program_info = program_info

    # check Number
    def variable_check(self, operand):
        if isinstance(operand, ast.Name):
            return operand.id
        elif isinstance(operand, ast.Num):
            return operand.n

    def convert_condition(self, compare: ast.Compare):
        con_info = Condition_info(compare.left, compare.comparators[0].n)
        con_info.convert_to_compare_symbol(compare.ops[0])
        return con_info

    def extraction_if_else(self, node: ast.If, mapper_flag):
        print("here")
        case = 0
        if node.orelse:
            self.filter_info.has_else = True
            flag = True
            while flag:
                if self.udf_call_type is "mExpression":
                    self.mapper_only(node.body[0].value)

                if isinstance(node.test, ast.Compare):
                    condition = self.convert_condition(node.test)
                    tmp_filter = EachFilter(condition, "", case)
                    self.filter_info.add_filter(tmp_filter)
                    case += 1

                if len(node.orelse) == 0:
                    flag = False
                elif isinstance(node.orelse[0], ast.If):
                    node = node.orelse[0]
                else:
                    self.mapper_only(node.orelse[0].value)
                    tmp_filter = EachFilter(None, "", case)
                    self.filter_info.add_filter(tmp_filter)
                    case += 1
                    flag = False

        else:
            if self.udf_call_type is "mExpression":
                self.mapper_only(node.body[0].value)
            condition = self.convert_condition(node.test)
            tmp_filter = EachFilter(condition, "", case)
            self.filter_info.add_filter(tmp_filter)
            case += 1

    def check_for_filter(self, exp, flag):
        if exp is None:
            return
        else:
            for tmp in ast.walk(exp):
                if isinstance(tmp, ast.If):
                    self.filter_info.has_if = True
                    self.extraction_if_else(tmp, flag)
                    break

    def get_condition_for_else(self, input_var):
        all_else_condtion = []
        for cond in self.filter_info.filter_condition[:-1]:
            condition = cond.filter_condition
            all_else_condtion.append("not (" + input_var + condition.operator + str(condition.right) + ")")
        return " and ".join(all_else_condtion)

    def combine_mapper_filter(self):
        combined_code_list = []
        for tmp_filter in self.filter_info.filter_condition:
            each_filter_info: EachFilter = tmp_filter.filter_condition
            if each_filter_info is not None:
                s = ".filter(lambda " + each_filter_info.left + ":" + each_filter_info.left + each_filter_info.operator + str(
                    each_filter_info.right) + ")"
                s += self.mapper_list.mr_steps[tmp_filter.mapper_index]
                combined_code_list.append(s)
            else:
                s = ".filter( lambda x : " + self.get_condition_for_else("x") + ")"
                s += self.mapper_list.mr_steps[tmp_filter.mapper_index]
                combined_code_list.append(s)
        return combined_code_list

    def check_has_else(self):
        all_else = []
        input_var = "x"
        lastCondition: EachFilter = self.filter_info.filter_condition[-1]
        if lastCondition.filter_condition is None:
            return -1
        else:
            for cond in self.filter_info.filter_condition:
                condition = cond.filter_condition
                all_else.append("not (" + input_var + condition.operator + str(condition.right) + ")")
        tmp_s = " and ".join(all_else)
        tmp_s = ".filter(lambda " + input_var + " : " + tmp_s + ")"
        return tmp_s

    def mapper_only_codegen(self, operation: BinOps):
        s = ".map(lambda " + operation.left + ": " + str(operation.left) + operation.operation + str(
            operation.right) + ")"
        self.mapper_list.add_mapper(s)
        return

    def reduce_codegen(self, operation: BinOps):
        if isinstance(operation.right, str):
            s = ".reduce(lambda accum," + operation.right + ": accum" + operation.operation + str(operation.right) + ")"
        else:
            s = ".reduce(lambda accum," + operation.left + ": accum " + operation.operation + operation.left + operation.operation + str(
                operation.right) + ")"
        self.mapper_list.add_mapper(s)

    def mapper_filter_ops(self, exp):
        codelist = self.combine_mapper_filter()
        if self.udf_call_type is "mExpression":
            s = self.check_has_else()
            if s is not -1:
                codelist.append(s)
        return codelist

    def mapper_only(self, exp):
        print("Mapper Only")
        for tmp_node in ast.walk(exp):
            if isinstance(tmp_node, ast.BinOp):
                left = self.variable_check(tmp_node.left)
                op = tmp_node.op
                right = self.variable_check(tmp_node.right)
                # target = tmp_node.targets[0].id
                print(left, op, right, "")
                binary_operation = BinOps(left, right, "", op)
                binary_operation.get_operation_from_operator()
                self.mapper_only_codegen(binary_operation)
        return

    def getAllMappers(self):
        all_mappers = [self.input_dataset]
        all_mappers.append(self.program_info.all_functions[-1].input_variable[0][0].arg)
        return all_mappers

    def get_operation_from_operator(self, operator):
        if isinstance(operator, ast.Add):
            return "+"
        elif isinstance(operator, ast.Sub):
            return "-"
        elif isinstance(operator, ast.Mult):
            return "*"
        elif isinstance(operator, ast.Div):
            return "/"

    def convert_variable_name_to_tuple(self, vname, accum, counter, each_mapper):
        if vname is accum:
            return "accum[0]"
        elif vname is counter:
            return "num[1]"
        elif vname is each_mapper:
            return "num[0]"
        else:
            return vname

    def convert_complex_binOps(self, binOperator, flag):
        if isinstance(binOperator.left, ast.BinOp) or isinstance(binOperator, ast.BinOp):
            if isinstance(binOperator.left, ast.BinOp):
                self.convert_complex_binOps(binOperator.left, flag)

            else:
                self.complexExpression += "( " + str(self.variable_check(binOperator.left))
                flag += 1
            self.complexExpression += " " + self.get_operation_from_operator(binOperator.op) + " "
            if isinstance(binOperator.right, ast.BinOp):
                self.convert_complex_binOps(binOperator.right, flag)

            else:
                self.complexExpression += " " + str(self.variable_check(binOperator.right)) + " )"
                flag -= 1
                if flag < 0:
                    self.complexExpression = "(" + self.complexExpression

    def reducer_binary_multiple_map(self, exp):
        accum = exp.args.args[0].arg
        counter = exp.args.args[1].arg
        each_mapper = exp.args.args[2].arg
        flag = 0
        # return ((accum[0] * num[1]) + num[0]) / (num[1] + 1),
        self.parallilizeList = self.getAllMappers()
        self.complexExpression = ""
        self.convert_complex_binOps(exp.body[0].value, flag)
        print(self.complexExpression)
        expression_list = self.complexExpression.split()
        for i, lit in enumerate(expression_list):
            if lit == accum:
                expression_list[i] = "accum[0]"
            elif lit == counter:
                expression_list[i] = "num[1]"
            elif lit == each_mapper:
                expression_list[i] = "num[0]"
        return_statement = " ".join(expression_list)
        udf1 = "def udf(accum, num): \n"
        udf1 += "\treturn " + return_statement+ ",0\n"
        self.multipleMapCode.append(udf1)
        return

    def reducer_binary_ops(self, exp):
        print("Mapper and Reducer")
        if len(exp.args.args) is 3:
            self.reducer_binary_multiple_map(exp)
            return 2
        for tmp_node in ast.walk(exp):
            if isinstance(tmp_node, ast.BinOp):
                left = self.variable_check(tmp_node.left)
                op = tmp_node.op
                right = self.variable_check(tmp_node.right)
                # target = tmp_node.targets[0].id
                print(left, op, right, "")
                binary_operation = BinOps(left, right, "", op)
                binary_operation.get_operation_from_operator()
                self.reduce_codegen(binary_operation)
        return 1

    def classify_udf(self, node):
        if self.udf_call_type is "mExpression" and self.filter_info.has_if is False:
            self.mapper_only(node)
            return 0

        elif self.udf_call_type is "mExpression" and self.filter_info.has_if is True:
            self.final_codegen_value = self.mapper_filter_ops(node)
            return 1
        else:
            type = 2
            if not self.filter_info.has_if:
                type = 3
            ch = self.reducer_binary_ops(node)
            if ch == 1:
                self.final_codegen_value = self.mapper_filter_ops(node)
                return type
            else:
                return 5