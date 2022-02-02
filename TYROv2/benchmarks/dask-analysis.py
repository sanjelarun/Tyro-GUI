import astor
filepath = "/home/sanjelarun/Tyro_GUI/Tyro-GUI/examples/dask/dask-sum.py"

source_ast = astor.code_to_ast.parse_file(filepath)


print(source_ast)