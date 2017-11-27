The main file (file containing main program) is main.py. Inputs and outputs are handled in main.py.

The prop_logic_parse.py deals mostly with the logic-related parts of the code.

Main functions used in prop_logic_parse:

	parse_string: parses input string into a logic formula binary tree represented by LogicNodes (used in all commands)

	sub: retrieves all subformulas of a given formula representation (used for 'sub' commands)

	build_truth_table: builds the truth table of a given formula representation (used for 'tt' commands)

	to_cnf: creates a simplified equivalent CNF formula representation
	get_set_of_clauses: retrieves a 'set of sets' representation of a given CNF formula (throws error if the given formula is not in CNF)
	simplify_set_of_clauses: simplifies a given set of clauses (removes tautology, etc. returns an empty set if all clauses contained are tautologies. returns a set containing an empty set if an empty clause is contained)
	*to_cnf, get_set_of_clauses, and simplify_set_of_clauses are all used for  'ecnf' commands

	resolve: performs resolution on a given set of clauses. returns 3 values: the list of resolution steps representing the order of operations, the resulting list of clauses, and a boolean value indicating whether an empty clause is contained within the list of clauses or not (True = empty clause detected). A resolution step is represented by 3 values: a pair of integers representing the indices of the clauses involved in that single resolution step, the index of the resolvent, and a boolean value indicating whether the resolvent is a new clause or not. The clauses' indices are their indices in the returned list of clauses. (used for 'res' commands)

	valid: checks whether the given formula is valid or not (used for 'valid' commands)

	ent: checks whether the first given formula entails the second one or not (used for 'ent' commands)