import prop_logic_parse

def parse_string(str_inp):
	return prop_logic_parse.parse_string(str_inp)

def print_subformula(formula: prop_logic_parse.LogicNode):
	print('print subformula for',formula)
	pass

def print_truth_table(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	truth_table = prop_logic_parse.build_truth_table(formula_root,symbol_set)
	row_count = len(truth_table)-1
	col_count = len(truth_table[0])
	header_len = []
	header_str = ''
	for i in range(col_count):
		header_entry = truth_table[0][i]
		header_len.append(len(header_entry))
		header_str += header_entry
		if i < col_count-1:
			header_str += ' '
	print(header_str)
	for i in range(1,row_count+1):
		row_str = ''
		for j in range(col_count):
			row_str += ('{truth_val:<' + str(header_len[j]) + 'd}').format(truth_val=truth_table[i][j])
			if j < col_count-1:
				row_str += ' '
		print(row_str)
	pass

def print_equivalent_cnf(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	formula_cnf = prop_logic_parse.to_cnf(formula_root)
	clauses = prop_logic_parse.simplify_cnf_set_of_sets(prop_logic_parse.get_set_of_clauses(formula_cnf))
	print(prop_logic_parse.format_set_of_sets(prop_logic_parse.sort_clauses(clauses)))
	pass

def print_resolution_process(formula: prop_logic_parse.LogicNode):
	print('print resolution process for',formula)
	pass

def print_validation_check_process(formula: prop_logic_parse.LogicNode):
	print('print validation check process for',formula)
	pass

def print_entailment_check(kb_formula: prop_logic_parse.LogicNode, alpha_formula: prop_logic_parse.LogicNode):
	print('print entailment check process for',kb_formula,'and',alpha_formula)
	pass

def get_formulas(str_inp):
	bracket_count = 0
	breakpoints = []
	for i in range(len(inp_split[1])):
		if inp_split[1][i] == ' ' and bracket_count == 0:
			breakpoints.append(i)
		elif inp_split[1][i] == '(':
			bracket_count += 1
		elif inp_split[1][i] == ')':
			bracket_count -= 1
	if len(breakpoints) == 0:
		return [parse_string(str_inp)]
	else:
		return [parse_string(str_inp[i+1:j]) for i,j in zip([-1] + breakpoints, breakpoints + [len(str_inp)])]
	
if __name__ == '__main__':
	n = int(input())
	for i in range(n):
		inp_split = input().split(maxsplit=1)
		cmd = inp_split[0]
		formulas = get_formulas(inp_split[1])
		if (cmd == 'sub'):
			print_subformula(formulas[0])
		elif (cmd == 'tt'):
			print_truth_table(formulas[0])
		elif (cmd == 'ecnf'):
			print_equivalent_cnf(formulas[0])
		elif (cmd == 'res'):
			print_resolution_process(formulas[0])
		elif (cmd == 'valid'):
			print_validation_check_process(formulas[0])
		elif (cmd == 'ent'):
			kb_formula = formulas[0]
			for alpha_formula in formulas[1:]:
				print_entailment_check(kb_formula,alpha_formula)
