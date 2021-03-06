import numpy as np

class LogicNode(object):
	def __init__(self, parent=None): pass
	
	def __eq__(self, other): pass
	
	def __hash__(self): pass

class OperatorNode(LogicNode):
	def __init__(self, type, parent:LogicNode=None):
		self.type = type
		self.parent = parent
	
	def __eq__(self, other): pass
	
	def __hash__(self): pass

class UnaryOperatorNode(OperatorNode):
	def __init__(self, type, operand: LogicNode, parent: LogicNode=None):
		if (not isinstance(operand, LogicNode)):
			raise TypeError('operand must be an instance of LogicNode')
		else:
			self.type = type
			self.operand = operand
			self.parent = parent
	
	def __eq__(self, other):
		if not isinstance(other, UnaryOperatorNode):
			return False	
		return self.type == other.type and self.operand == other.operand
	
	def __hash__(self):
		return 17 * hash(self.type) + hash(self.operand)
	
	def __repr__(self):
		return repr(self.type) + '(' + repr(self.operand) + ')'
	
	def __str__(self):
		return str(self.type) + str(self.operand)

class BinaryOperatorNode(OperatorNode):
	def __init__(self, type, operand1: LogicNode, operand2: LogicNode, parent: LogicNode=None):
		if (not isinstance(operand1, LogicNode) or not isinstance(operand2, LogicNode)):
			raise TypeError('both operands must be instances of LogicNode')
		else:
			self.type = type
			self.operand1 = operand1
			self.operand2 = operand2
			self.parent = parent
	
	def __eq__(self, other):
		if not isinstance(other, BinaryOperatorNode):
			return False
		return self.name == other.name and self.type == other.type and self.operand1 == other.operand1 and self.operand2 == other.operand2
	
	def __hash__(self):
		return 31 * hash(self.type) +  17 * hash(self.operand1) + hash(self.operand2)
	
	def __repr__(self):
		return repr(self.type) + '(' + repr(self.operand1) + ',' + repr(self.operand2) + ')'
	
	def __str__(self):
		return '(' + str(self.operand1) + ' ' + str(self.type) + ' ' + str(self.operand2) + ')'

class SymbolNode(LogicNode):
	def __init__(self, name, parent: LogicNode=None):
		self.name = name
		self.parent = parent
	
	def __hash__(self):
		return hash(self.name)
	
	def __repr__(self):
		return repr(self.name)
	
	def __str__(self):
		return str(self.name)
	
	def __eq__(self, other):
		if not isinstance(other, SymbolNode):
			return False
		return self.name == other.name

def parse_string(str_inp: str):
	symbol_set = set()
	if (str_inp is None or len(str_inp) == 0):
		return symbol_set,None
	elif (str_inp[0].isalpha()):
		symbol_set.add(str_inp)
		return symbol_set,SymbolNode(str_inp)
	elif (str_inp[0] == '~'):
		symbol_set,child_node = parse_string(str_inp[1:])
		return symbol_set,UnaryOperatorNode('~',child_node)
	elif(str_inp[0] == '('):
		parentheses_count = 0
		operator_idx = -1
		length = len(str_inp)
		idx = 1
		is_implication = False
		is_biimplication = False
		while (idx < len(str_inp)):
			if (str_inp[idx] == '|' or str_inp[idx] == '&') and (parentheses_count == 0):
				operator_idx = idx
			elif (str_inp[idx] == '-' and parentheses_count == 0):
				if (str_inp[idx-1] == '<'):
					is_biimplication = True
				else:
					is_implication = True
				operator_idx = idx
			elif (str_inp[idx] == '('):
				parentheses_count += 1
			elif (str_inp[idx] == ')'):
				parentheses_count -= 1
			idx += 1
		if is_implication:
			operand1_end_idx = operator_idx-1
			operator = str_inp[operator_idx:operator_idx+2]
			operand2_start_idx = operator_idx+3
		elif is_biimplication:
			operand1_end_idx = operator_idx-2
			operator = str_inp[operator_idx-1:operator_idx+2]
			operand2_start_idx = operator_idx+3
		else:
			operand1_end_idx = operator_idx-1
			operator = str_inp[operator_idx]
			operand2_start_idx = operator_idx+2
		symbol_set_1,child_node_1 = parse_string(str_inp[1:operand1_end_idx])
		symbol_set_2,child_node_2 = parse_string(str_inp[operand2_start_idx:length-1])
		return symbol_set_1.union(symbol_set_2),BinaryOperatorNode(operator, child_node_1, child_node_2)

def copy_formula(root: LogicNode):
	if (root is None):
		return None
	elif (isinstance(root,SymbolNode)):
		return SymbolNode(root.name)
	elif (isinstance(root,UnaryOperatorNode)):
		return UnaryOperatorNode(root.type, copy_formula(root.operand))
	elif (isinstance(root,BinaryOperatorNode)):
		return BinaryOperatorNode(root.type, copy_formula(root.operand1), copy_formula(root.operand2))

def open_macro(root: LogicNode):
	return open_macro_rec(copy_formula(root))

def open_macro_rec(root: LogicNode):
	if (root is None or isinstance(root,SymbolNode)):
		return root
	elif (isinstance(root,UnaryOperatorNode)):
		root.operand = open_macro(root.operand)
	elif (isinstance(root,BinaryOperatorNode)):
		operand1 = root.operand1
		operand2 = root.operand2
		if (root.type == '<->'):
			new_type = '&'
			new_operand1 = open_macro(BinaryOperatorNode('->',operand1,operand2))
			new_operand2 = open_macro(BinaryOperatorNode('->',operand2,operand1))
		elif (root.type == '->'):
			new_type = '|'
			new_operand1 = negate(open_macro(operand1))
			new_operand2 = open_macro(operand2)
		else:
			new_type = root.type
			new_operand1 = open_macro(operand1)
			new_operand2 = open_macro(operand2)
		root.type = new_type
		root.operand1 = new_operand1
		root.operand2 = new_operand2
	return root

def to_nnf(root: LogicNode):
	root = open_macro(copy_formula(root))
	return to_nnf_rec(root)

def to_nnf_rec(root: LogicNode):
	if (root is None or isinstance(root,SymbolNode)):
		return root
	elif (isinstance(root,BinaryOperatorNode)):
		root.operand1 = to_nnf(root.operand1)
		root.operand2 = to_nnf(root.operand2)
	elif (isinstance(root,UnaryOperatorNode)):
		if (isinstance(root.operand,UnaryOperatorNode)):
			return to_nnf(root.operand.operand)
		elif (isinstance(root.operand,BinaryOperatorNode)):
			if (root.operand.type == '|'):
				new_type = '&'
			else:
				new_type = '|'
			new_operand1 = to_nnf_rec(negate(root.operand.operand1))
			new_operand2 = to_nnf_rec(negate(root.operand.operand2))
			root = BinaryOperatorNode(new_type, new_operand1, new_operand2)
	return root

def to_cnf(root: LogicNode):
	root = to_nnf(copy_formula(root))
	return to_cnf_rec(root, root)

def to_cnf_rec(root: LogicNode, true_root):
	if (root is None or isinstance(root,SymbolNode) or isinstance(root,UnaryOperatorNode)):
		return root
	elif (isinstance(root,BinaryOperatorNode)):
		new_type = root.type
		new_operand1 = to_cnf_rec(root.operand1, true_root)
		new_operand2 = to_cnf_rec(root.operand2, true_root)
		if (root.type == '|' and ((isinstance(root.operand1,BinaryOperatorNode) and root.operand1.type == '&') or (isinstance(root.operand2,BinaryOperatorNode) and root.operand2.type == '&'))):
			new_type = '&'
			if (isinstance(root.operand1,BinaryOperatorNode) and root.operand1.type == '&'):
				new_operand1 = to_cnf_rec(BinaryOperatorNode('|',root.operand1.operand1,root.operand2), true_root)
				new_operand2 = to_cnf_rec(BinaryOperatorNode('|',root.operand1.operand2,root.operand2), true_root)
			else:
				new_operand1 = to_cnf_rec(BinaryOperatorNode('|',root.operand2.operand1,root.operand1), true_root)
				new_operand2 = to_cnf_rec(BinaryOperatorNode('|',root.operand2.operand2,root.operand1), true_root)
		root.type = new_type
		root.operand1 = new_operand1
		root.operand2 = new_operand2
	return root

def is_cnf(root: LogicNode):
	return is_cnf_rec(root, '&')

def is_cnf_rec(root: LogicNode, current_type):
	# CNF in binary tree representation must follow:
	# (n >= 0) times & => (m >= 0) times | => 0 or 1 time ~ => symbol
	if root is None:
		return True
	elif current_type == '&':
		if (isinstance(root,SymbolNode)):
			return True
		else:
			if (isinstance(root,UnaryOperatorNode)):
				return is_cnf_rec(root.operand, root.type)
			else:
				return is_cnf_rec(root.operand1, root.type) and is_cnf_rec(root.operand2, root.type)
	elif current_type == '|':
		if (isinstance(root,SymbolNode)):
			return True
		else:
			if (isinstance(root,UnaryOperatorNode)):
				return is_cnf_rec(root.operand, root.type)
			else:
				if root.type == '&':
					return False
				else:
					return is_cnf_rec(root.operand1, root.type) and is_cnf_rec(root.operand2, root.type)
	elif current_type == '~':
		if (isinstance(root,SymbolNode)):
			return True
		else:
			return False
	else:
		return False

def get_set_of_clauses(root: LogicNode):
	if (not is_cnf(root)):
		raise ValueError('formula must be in CNF form')
	return get_set_of_clauses_rec(root, set())

def get_set_of_clauses_rec(root: LogicNode, clauses):
	if root is None:
		return clauses
	elif (isinstance(root,SymbolNode)):
		clauses.add(frozenset([root]))
		return clauses
	elif (isinstance(root,UnaryOperatorNode)):
		clauses.add(frozenset([root]))
		return clauses
	elif (isinstance(root,BinaryOperatorNode)):
		if (root.type == '|'):
			clauses.add(frozenset(get_set_of_literals(root)))
			return clauses
		else:
			return clauses.union(get_set_of_clauses_rec(root.operand1, clauses)).union(get_set_of_clauses_rec(root.operand2, clauses))
	else:
		return clauses

def get_set_of_literals(root: LogicNode):
	return get_set_of_literals_rec(root, set())

def get_set_of_literals_rec(root: LogicNode, literals):
	if root is None:
		return literals
	elif (isinstance(root,SymbolNode)):
		return literals.union(set([root]))
	elif (isinstance(root,UnaryOperatorNode)):
		if (isinstance(root.operand,SymbolNode)):
			return literals.union(set([root]))
		else:
			return get_set_of_literals_rec(root.operand, literals)
	elif (isinstance(root,BinaryOperatorNode)):
		return literals.union(get_set_of_literals_rec(root.operand1, literals)).union(get_set_of_literals_rec(root.operand2, literals))
	else:
		return literals

def conjunct(operand1: LogicNode, operand2: LogicNode):
	if (not isinstance(operand1,LogicNode) or not isinstance(operand2,LogicNode)):
		raise TypeError('both operands must be instances of LogicNode')
	else:
		return BinaryOperatorNode('&',operand1,operand2)

def disjunct(operand1: LogicNode, operand2: LogicNode):
	if (not isinstance(operand1,LogicNode) or not isinstance(operand2,LogicNode)):
		raise TypeError('both operands must be instances of LogicNode')
	else:
		return BinaryOperatorNode('&',operand1,operand2)

def negate(operand: LogicNode):
	if (not isinstance(operand,LogicNode)):
		raise TypeError('operand must be an instance of LogicNode')
	else:
		return UnaryOperatorNode('~',operand)

def negate_lit(operand):
	if (len(operand) == 1):
		return '~' + operand
	else:
		return operand[1:]

def negate_simplify(operand: LogicNode):
	if (not isinstance(operand,LogicNode)):
		raise TypeError('operand must be an instance of LogicNode')
	else:
		if (isinstance(operand,UnaryOperatorNode) and operand.type == '~'):
			return operand.operand
		else:
			return UnaryOperatorNode('~',operand)

def negate_deep_simplify(operand: LogicNode):
	if (not isinstance(operand,LogicNode)):
		raise TypeError('operand must be an instance of LogicNode')
	else:
		negated = negate(operand)
		while (isinstance(negated,UnaryOperatorNode) and negated.type == '~' and isinstance(negated.operand,UnaryOperatorNode) and negated.operand.type == '~'):
			negated = negated.operand.operand
		return negated

def imply(operand1: LogicNode, operand2: LogicNode):
	if (not isinstance(operand1,LogicNode) or not isinstance(operand2,LogicNode)):
		raise TypeError('both operands must be instances of LogicNode')
	else:
		return BinaryOperatorNode('->',operand1,operand2)

def biimply(operand1: LogicNode, operand2: LogicNode):
	if (not isinstance(operand1,LogicNode) or not isinstance(operand2,LogicNode)):
		raise TypeError('both operands must be instances of LogicNode')
	else:
		return BinaryOperatorNode('<->',operand1,operand2)

def simplify_cnf_set_of_sets(clauses):
	new_set = set()
	for clause in clauses:
		new_clause = simplify_set_of_literals(clause)
		if new_clause is None:
			continue
		if len(new_clause) == 0:
			return set([frozenset()])
		else:
			new_set.add(frozenset(new_clause))
	return new_set

def simplify_set_of_literals(literals):
	new_set = set()
	for literal in literals:
		negated_literal = to_nnf(negate(literal))
		if negated_literal in new_set:
			return None
		elif literal not in new_set:
			new_set.add(literal)
	return new_set

def sort_clauses(clauses):
	return sorted([sort_literals(x) for x in clauses], key=str)

def sort_literals(literals):
	return sorted([x for x in literals], key=str)

def format_set_of_sets(clause_list):
	str_out = ''
	str_out += '{'
	for i,clause in enumerate(clause_list):
		str_out += format_set(clause)
		if (i < len(clause_list)-1):
			str_out += ', '
	str_out += '}'
	return str_out

def format_set(clause):
	str_out = ''
	str_out += '{'
	for j,literal in enumerate(clause):
		str_out += str(literal)
		if (j < len(clause)-1):
			str_out += ', '
	str_out += '}'
	return str_out

def assign(root: LogicNode,symbol_values):
	if (root is None):
		return None
	elif (isinstance(root,SymbolNode)):
		return symbol_values[root.name]
	elif (isinstance(root,UnaryOperatorNode)):
		return not assign(root.operand,symbol_values)
	elif (isinstance(root,BinaryOperatorNode)):
		value1 = assign(root.operand1, symbol_values)
		value2 = assign(root.operand2, symbol_values)
		if (root.type == '|'):
			return value1 or value2
		elif (root.type == '&'):
			return value1 and value2
		elif (root.type == '->'):
			return (not value1) or value2
		elif (root.type == '<->'):
			return value1 == value2
		else:
			return None
	else:
		return None

def build_truth_table(formula: LogicNode, symbol_set):
	symbol_count = len(symbol_set)
	table = []
	symbol_list = sorted(list(symbol_set))
	symbol_list.append('F')
	table.append(symbol_list)
	i = 0
	while (i < (2**symbol_count)):
		truth_bitmask = i
		assignment = {}
		row = []
		for j in range(0,symbol_count):
			symbol = symbol_list[symbol_count-j-1]
			truth_val = truth_bitmask % 2
			assignment[symbol] = truth_val
			row.append(truth_val)
			truth_bitmask = truth_bitmask // 2
		assign_val = 1 if assign(formula,assignment) else 0
		row.reverse()
		row.append(assign_val)
		table.append(row)
		i += 1
	return table

def print_sub(root: LogicNode):
	return '\n'.join(str(e) if not isinstance(e, None) else '' for e in sub_rec(copy_formula(root)))

def sub(root: LogicNode):
	return sub_rec(copy_formula(root))

def sub_rec(root: LogicNode):
	subformula_list = []
	subformula_set = set()
	subformula_list.append(root)
	subformula_set.add(root)
	if (isinstance(root, UnaryOperatorNode)):
		subformula_list_child,subformula_set_child = sub(root.operand)
		subformula_list.extend(subformula_list_child)
		subformula_set = subformula_set | subformula_set_child
	elif (isinstance(root, BinaryOperatorNode)):
		subformula_list_child1,subformula_set_child1 = sub(root.operand1)
		subformula_list_child2,subformula_set_child2 = sub(root.operand2)
		subformula_set = subformula_set | subformula_set_child1 | subformula_set_child2
		subformula_list.extend(subformula_list_child1)
		subformula_list.extend(subformula_list_child2)
	return subformula_list,subformula_set

def print_normal(root: LogicNode):
	return print_normal_rec(root)

def print_normal_rec(root: LogicNode):
	if (isinstance(root, SymbolNode)):
		return root.name
	elif (isinstance(root, UnaryOperatorNode)):
		if(isinstance(root.operand, SymbolNode)):
			return '~' + print_normal_rec(root.operand)
		else:
			return '~(' + print_normal_rec(root.operand) + ')' 
	elif (isinstance(root, BinaryOperatorNode)):
		return '(' + print_normal_rec(root.operand1) + ' ' + root.type + ' ' + print_normal_rec(root.operand2) + ')'

def resolve(clauses):
	to_print = list(clauses)
	original_size = len(to_print)
	clause_map = {}
	counter = 0
	sorted_clauses = sort_clauses(clauses)
	resolutions = []
	for clause in sorted_clauses:
		clause_key = frozenset(clause)
		counter += 1
		clause_map[clause_key] = counter
		resolutions.append((None,counter,False))
	resolved_pairs = set()
	cont = True
	while cont:
		old_clauses = clauses
		result_set = set()
		found_empty_clause = False
		for clause1 in clauses:
			for clause2 in clauses:
				clause1_idx = clause_map[clause1]
				clause2_idx = clause_map[clause2]
				clause_idx_pair = (clause1_idx,clause2_idx)
				if (clause1_idx >= clause2_idx or clause_idx_pair in resolved_pairs):
					continue
				for literal1 in clause1:
					literal2 = negate_simplify(literal1)
					if(literal2 in clause2):
						resolvent = (clause1 | clause2).difference(set([literal1,literal2]))
						resolved_pairs.add(clause_idx_pair)
						if (len(resolvent) == 0):
							found_empty_clause = True
						if resolvent in clause_map.keys():
							resolutions.append((clause_idx_pair,clause_map[resolvent],False))
						else:
							counter += 1
							clause_map[resolvent] = counter
							resolutions.append((clause_idx_pair,counter,True))
						if (simplify_set_of_literals(resolvent)) is not None:
							result_set.add(resolvent)
				if found_empty_clause:
					break
			if found_empty_clause:
				break
		clauses = clauses | result_set
		if found_empty_clause or old_clauses == clauses:
			cont = False
	clause_list = [None] * (len(clause_map) + 1)
	for clause in clause_map.keys():
		idx = clause_map[clause]
		clause_list[idx] = clause
	return resolutions,clause_list,found_empty_clause

def sort_stringify_set_of_sets(clauses):
	return format_set_of_sets(sort_clauses(clauses)) 

def sort_stringify_set_of_literals(clause):
	return format_set(sort_literals(clause))

def show_formula(str_inp):
	symbol_set,formula = parse_string(str_inp)
	print('Original formula: ',formula)
	print('Symbols: ',symbol_set)
	print('Formula tree: ',repr(formula))
	print('Formula (without macro): ',open_macro(formula))
	print('Formula (in NNF): ',to_nnf(formula))
	print('Formula (in CNF): ',to_cnf(formula))
	set_of_clauses = simplify_cnf_set_of_sets(get_set_of_clauses(to_cnf(formula)))
	sorted_clauses = sort_clauses(set_of_clauses)
	print('CNF in set of sets: ', format_set_of_sets(sorted_clauses))
	# print('Truth table:')
	# truth_table = build_truth_table(formula, symbol_set)
	# print(np.array(truth_table))
	print('Subformulas:')
	subformula_list,subformula_set = sub(to_nnf(formula))
	print('\n'.join(str(e) for e in subformula_list))
	print(to_nnf(formula),'has',len(subformula_set),'different subformulas')
	# print('resolution process:')
	# result = resolve(set_of_clauses)
	# print('unsatisfiable' if (len(result) == 1 and len(next(iter(result))) == 0) else 'satisfiable')
	# print('subtrees: ')
	# sub(formula)
	# print('resolution: ' + print_set(resolve(set_of_clauses)))

if __name__ == '__main__':
	# f_str = '(~(A -> B) & ((B | C) <-> A))'
	# f_str = '(~(P1 -> P2) & ((P2 | P3) <-> P1))'
	# f_str = '(~(P2 | P3) | P1)'
	# f_str = '(((P2 -> P1) | ~P2) <-> P2)'
	# f_str = '((((A & B) | C) & D) | E)'
	# f_str = '((((A & B) & C) & D) | E)'
	# f_str = '~((A -> (~B & (C -> A))) -> B)'
	# f_str = '~((P2 -> P4) -> (P3 & P4))'
	# f_str = '((A -> B) | ((A & ~C) <-> B))'
	# f_str = 'A'
	# f_str = '~A'
	# f_str = '(A | B)'
	# f_str = '(A & B)'
	# f_str = '(F <-> G)'
	# f_str = '(F -> G)'
	# f_str = '(G -> F)'
	# f_str = '~~~~~~~~~A'
	# f_str = '(((P -> Q) -> (R -> S)) & (Q -> R))'
	# f_str = '((~A | B) & (~B | C))'
	# f_str = '(((A -> B) & (B -> C)) -> (A | B))'
	# f_str = '(((A | ~B) & B) & ~A)'
	# f_str = '~(((A -> B) & (B -> C)) -> ((A | B) -> C))'
	f_str = '(((A | ~B) & B) & ~A)'
	show_formula(f_str)
	symbol_set,formula = parse_string(f_str)
