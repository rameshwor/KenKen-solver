# Solver for KenKen puzzles (version 1)

import	string


# Return first non-false value, or False
def first(iterable):
	for i in iterable:
		if (i): return i
	return False

#select one member from each set and make the sum?
def can_make_sum_p(t, sets):
    if (not sets): return (t == 0)
    head = sets[0]; tail = sets[1:]
    return any(can_make_sum_p(t-e, tail) for e in head if e <= t)

# select one member from each set  and make the product
def can_make_product_p(t, sets):
    if (not sets): return (t == 1)
    head = sets[0]; tail = sets[1:]
    return any(can_make_product_p(t/e, tail) for e in head if not t%e)


def print_solution(s):
	if (not s):
		#print s
		return

	rows	= list(set(k[0] for k in s.keys()))
	rows.sort()
	cols	= list(set(k[1] for k in s.keys()))
	cols.sort()
	max_len = max(map(len, s.values()))
	row_div = '\n' + '-+-'.join('-'*max_len for c in cols) + '\n'
	answerlist = []
	for r in rows:
		for c in cols:
			answerlist.append(s[r+c])
	return answerlist

class Constraint(object):
	def __init__(self, value, *cells):
		self.cells	= set(cells)
		self.value	= int(value)
	def _test_component(self, component, context):
		return True
	def apply(self, solution):
		d_sets = dict((c, map(int, solution[c])) for c in self.cells); d_bad = {}
		for k,v in d_sets.items():
			others = [ov for ok,ov in d_sets.items() if ok != k]
			d_bad[k] = ''.join(str(e) for e in v if not self._test_component(e, others))
		return d_bad

class Assert(Constraint):
	def apply(self, solution):
		return dict((c, solution[c].replace(str(self.value), '')) for c in self.cells)
	
class Sum(Constraint):
	def _test_component(self, component, context):
		return (self.value>=component) and can_make_sum_p(self.value-component, context)

class Diff(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) != 2): raise Exception('difference can be doen only for two cells')
	def _test_component(self, component, context):
		return (self.value+component in context[0]) or (component-self.value in context[0])

class Prod(Constraint):
	def _test_component(self, component, context):
		return (not self.value%component) and can_make_product_p(self.value/component, context)

class Div(Constraint):
	def __init__(self, value, *cells):
		Constraint.__init__(self, value, *cells)
		if (len(cells) != 2): raise Exception('divison can be done for only two cells')
	def _test_component(self, component, context):
		return (self.value*component in context[0]) or (float(component)/self.value in context[0])

class Set(Constraint):
	def apply(self, solution):
		# For each cell:
		d_bad = {}
		for c in self.cells:
			# If a cell has only one possible value, remove that value from all other cells
			if (len(solution[c]) != 1): continue
			for c2 in self.cells:
				if (c2 != c): d_bad[c2] = d_bad.get(c2,'') + solution[c]
		return d_bad


class Puzzle(object):
	lut = {'!':Assert, '+':Sum, '-':Diff, '*':Prod, '/':Div}
	def __init__(self, fn):
		# Parse file
		lines = [l.split() for l in file(fn, 'rb').read().strip().split('\n')]
		if (lines[0][0] != '#'):
			raise Exception('Puzzle definitions must begin with a size ("#") line')
		self.size	= int(lines[0][1])
		self.cages	= [self.lut[l[0]](*l[1:]) for l in lines[1:]]


def solve(puzzle):
	# Derived from the problem size
	rows	= string.ascii_uppercase[:puzzle.size]
	cols	= string.digits[1:1+puzzle.size]
	sets	= [Set(0, *(r+c for c in cols)) for r in rows] + \
			  [Set(0, *(r+c for r in rows)) for c in cols]
	d_constraints = dict((r+c, set()) for r in rows for c in cols)
	for constraint in sets+puzzle.cages:
		for cell in constraint.cells:
			d_constraints[cell].add(constraint)
	#  Given a partial solution, apply (potentially) unsatisfied constraints
	def constrain(solution, *constraints):
		queue = set(constraints)
		while (queue):
			constraint = queue.pop()
			for cell, bad_choices in constraint.apply(solution).items():
				values = solution[cell]
				for choice in bad_choices:
					values = values.replace(choice, '')
				if (not values):
					return False
				if (solution[cell] == values):
					continue
				solution[cell] = values
				queue.update(d_constraints[cell])
		return solution
	#  Given a partial solution, force one of its cells to a given value
	def assign(solution, cell, value):
		solution[cell] = value
		return constrain(solution, *d_constraints[cell])
	# : Recursively refine a solution with search and propogation
	def search(solution):
		if ((not solution) or all(len(v)==1 for v in solution.values())):
			return solution
		# Find a most-constrained unsolved cell
		cell = min((len(v),k) for k,v in solution.items() if len(v)>1)[1]
		# f
		return first(search(assign(solution.copy(), cell, h)) for h in solution[cell])
	# Solve
	symbols = string.digits[1:1+puzzle.size]
	return search(constrain(dict((c,symbols) for c in d_constraints.keys()), *puzzle.cages))
