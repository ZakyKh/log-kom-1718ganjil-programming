
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
			raise ValueError('operand must be an instance of LogicNode')
		else:
			self.type = type
			self.operand = operand
			self.parent = parent
	
	def __eq__(self, other):	
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
			raise ValueError('both operands must be instances of LogicNode')
		else:
			self.type = type
			self.operand1 = operand1
			self.operand2 = operand2
			self.parent = parent
	
	def __eq__(self, other):
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
	
	def __eq__(self, other):
		return self.name == other.name
	
	def __hash__(self):
		return hash(self.name)
	
	def __repr__(self):
		return repr(self.name)
	
	def __str__(self):
		return str(self.name)

def parse_logic(str_inp: str):
	symbol_set = set()
	if (str_inp is None or len(str_inp) == 0):
		return symbol_set,None
	elif (str_inp[0].isalpha()):
		symbol_set.add(str_inp)
		return symbol_set,SymbolNode(str_inp)
	elif (str_inp[0] == '~'):
		symbol_set,child_node = parse_logic(str_inp[1:])
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
		symbol_set_1,child_node_1 = parse_logic(str_inp[1:operand1_end_idx])
		symbol_set_2,child_node_2 = parse_logic(str_inp[operand2_start_idx:length-1])
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
			new_operand1 = UnaryOperatorNode('~',open_macro(operand1))
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
			new_operand1 = to_nnf_rec(UnaryOperatorNode('~',root.operand.operand1))
			new_operand2 = to_nnf_rec(UnaryOperatorNode('~',root.operand.operand2))
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

def show_formula(str_inp):
	symbol_set,formula = parse_logic(str_inp)
	print('Original formula: ',formula)
	print('Symbols: ',symbol_set)
	print('Formula tree: ',repr(formula))
	print('Formula (without macro): ',open_macro(formula))
	print('Formula (in NNF): ',to_nnf(formula))
	print('Formula (in CNF): ',to_cnf(formula))

# f_str = '(~(A -> B) & ((B | C) <-> A))'
# f_str = '(~(P1 -> P2) & ((P2 | P3) <-> P1))'
# f_str = '(~(P2 | P3) | P1)'
# f_str = '((((A & B) | C) & D) | E)'
# f_str = '((((A & B) & C) & D) | E)'
# f_str = '~((A -> (~B & (C -> A))) -> B)'
# f_str = '~((P2 -> P4) -> (P3 & P4))'
f_str = '((A1 -> B1) | ((A2 & ~C1) <-> B2))'
# f_str = 'A'
# f_str = '(A | B)'
# f_str = '(A & B)'

show_formula(f_str)