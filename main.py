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
