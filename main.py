import prop_logic_parse

def parse_string(str_inp):
	return prop_logic_parse.parse_string(str_inp)

def print_subformula(formula: prop_logic_parse.LogicNode):
	print('print subformula for',formula)
	pass

def print_truth_table(formula: prop_logic_parse.LogicNode):
	print('print truth table for',formula)
	pass

def print_equivalent_cnf(formula: prop_logic_parse.LogicNode):
	print('print equivalent cnf for',formula)
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

def get_formulas_str(str_inp):
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
		return [str_inp]
	else:
		return [str_inp[i+1:j] for i,j in zip([-1] + breakpoints, breakpoints + [len(str_inp)])]
	
if __name__ == '__main__':
	n = int(input())
	for i in range(n):
		inp_split = input().split(maxsplit=1)
		cmd = inp_split[0]
		formulas = get_formulas_str(inp_split[1])
		print(formulas)
		if (cmd == 'sub'):
			pass
			# print_subformula(formula)
		elif (cmd == 'tt'):
			pass
			# print_truth_table(formula)
		elif (cmd == 'ecnf'):
			pass
			# print_equivalent_cnf(formula)
		elif (cmd == 'res'):
			pass
			# print_resolution_process(formula)
		elif (cmd == 'valid'):
			pass
			# print_validation_check_process(formula)
		elif (cmd == 'ent'):
			pass
			# print_entailment_check(kb_formula,alpha_formula)
