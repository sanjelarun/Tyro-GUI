from builder import CFGBuilder

a = CFGBuilder().build_from_file('model.py', './model.py')
a.build_visual('example.pdf','pdf')