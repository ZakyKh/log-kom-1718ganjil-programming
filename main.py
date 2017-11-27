import prop_logic_parse

def parse_string(str_inp):
	return prop_logic_parse.parse_string(str_inp)

def print_subformula(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	formula_root_open = prop_logic_parse.open_macro(formula_root)
	subformula_list,subformula_set = prop_logic_parse.sub(formula_root_open)
	print("\n".join(str(e) for e in subformula_list))
	print(formula_root,'has',len(subformula_set),'different subformulas')

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

def print_equivalent_cnf(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	formula_cnf = prop_logic_parse.to_cnf(formula_root)
	clauses = prop_logic_parse.simplify_cnf_set_of_sets(prop_logic_parse.get_set_of_clauses(formula_cnf))
	print(prop_logic_parse.format_set_of_sets(prop_logic_parse.sort_clauses(clauses)))

def print_resolution_process(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	formula_root_cnf = prop_logic_parse.to_cnf(formula_root)
	print(formula_root_cnf)
	set_of_clauses = prop_logic_parse.simplify_cnf_set_of_sets(prop_logic_parse.get_set_of_clauses(formula_root_cnf))
	resolutions,clause_list,unsatisfiable = prop_logic_parse.resolve(set_of_clauses)
	for resolution_step in resolutions:
		clause_idx_pair, resolvent_idx, is_new_clause = resolution_step
		if clause_idx_pair is None:
			print(str(resolvent_idx) + ': ',print_set(clause_list[resolvent_idx]))
		elif is_new_clause:
			print(str(resolvent_idx) + ': ',print_set(clause_list[resolvent_idx]),'---',clause_idx_pair)
		else:
			print('...',clause_idx_pair,'yields clause at',resolvent_idx)
	if (unsatisfiable):
		print('unsatisfiable')
	else:
		print('satisfiable')
	return unsatisfiable

def print_validation_check_process(formula: prop_logic_parse.LogicNode):
	symbol_set,formula_root = formula
	formula_neg = prop_logic_parse.negate(formula_root)
	print('check if',formula_neg,' is unsatisfiable')
	unsatisfiable = print_resolution_process((symbol_set,formula_neg))
	if (unsatisfiable):
		print(formula_root,'is valid')
	else:
		print(formula_root,'is not valid')

def print_entailment_check(kb_formula: prop_logic_parse.LogicNode, alpha_formula: prop_logic_parse.LogicNode):
	symbol_set_kb,formula_root_kb = kb_formula
	symbol_set_alpha,formula_root_alpha = alpha_formula
	formula_combined = prop_logic_parse.conjunct(formula_root_kb,prop_logic_parse.negate(formula_root_alpha))
	print('check if',formula_combined,'is unsatisfiable')
	unsatisfiable = print_resolution_process((symbol_set_kb | symbol_set_alpha, prop_logic_parse.to_cnf(formula_combined)))
	if (unsatisfiable):
		print(formula_root_kb,'entails',formula_root_alpha)
	else:
		print(formula_root_kb,'does not entail',formula_root_alpha)

def print_set_of_sets(clauses):
	return '{' + ', '.join(print_set(clause) for clause in clauses) + '}'

def print_set(s):
	return '{' + ', '.join(str(e) for e in s) + '}'

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
