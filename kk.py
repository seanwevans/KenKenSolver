#!/usr/bin/env python
from itertools import permutations, product
from functools import reduce
from random import choice

# Loop through two lists of equal length and return True
# if no two elements match exactly in index and value.
# none_match( [1,2,3] , [4,5,6] ) == True
# none_match( [1,2,3] , [4,5,3] ) == False
def none_match(m1, m2):
	for i in range(len(m1)):
		if m1[i] == m2[i]:	
			return False
	return True
	
# Main Ken Ken Board Class
class KenKen(object):
	
	def __init__(self, board):
		self.board = board
		self.size = self.find_size()
		
	def find_size(self):
		# Assumes a square board, returns maximum board dimension
		m = 0
		for k in self.board:
			for (x,y) in self.board[k][2]:
				if x > m:	m = x
				if y > m:	m = y
		return(m)
		
	def print_board(self):
	# Prints board showing id
		for row in range(1, self.size+1):
			for col in range(1, self.size+1):
				for k in self.board:
					if (col, row) in self.board[k][2]:
						print(k, end='')
						break
			print()
	
	def get_id_from_pos(self, i, j):
		# Given a position on the board return appropriate id
		for id in self.board:
			if (j,i) in self.board[id][2]:
				return id
					
	def print_board2(self):
		# Prints board showing target numbers and operations
		border = "-" * (3 * self.size + 1)
				
		for i in range(1,self.size+1):
			print(border)
			s = "|"
			t = "|"
			for j in range(1,self.size+1):
				gtij = self.get_id_from_pos(i,j)
				s += self.board[gtij][0]
				if len(str(gtij)) == 1: s += " "
				s += "|"
				t += str(self.board[gtij][1])
				if len(str(self.board[gtij][1])) == 1: t += " "
				t += "|"
			print(s)
			print(t)
		
		print(border)
	
	def check_id(self, id, answers):
		# Return True if the list of answers conforms to the operation id.
		op = self.board[id][0]
		target = self.board[id][1]
		
		# If answers add to target
		if op == '+':
			if sum(answers) == target:	return True
			else:	return False
			
		# If some permutation of answers subtract to target
		elif op == '-':
			for p in permutations(answers, len(answers)):
				if reduce(lambda x,y: x-y, p) == target:	return True
			return False
		
		# If answers multiply to target
		elif op == '*':
			if reduce(lambda x,y: x*y, answers) == target:	return True
			else:	return False
			
		# If some permutation divides to target
		elif op == '/':
			for p in permutations(answers, len(answers)):
				if reduce(lambda x,y: x/y, p) == target:	return True
			return False
		
		# Defined block, no operation
		elif op == ' ':
			if answers[0] == target:	return True
			else:	return False
	
	def check_board(self, answers):
		# Checks entire board to make sure calculations are valid
		for id in self.board:
			ans = []
			for (x,y) in self.board[id][2]:
				ans.append(answers[y-1][x-1])
			if(not self.check_id(id, ans)):	return False
		return(True)
		
	def check_valid_answer(self, answers):
		valid = [j for j in range(1, self.size+1)]
		for i in answers:
			if sorted(i) != valid: return False
		for i in range(self.size):
			if sorted([x[i] for x in answers]) != valid:	return False
		return True
	
	def solve(self):
		# Brute force check every permutationsutation to solve puzzle
		# Only for four squares
		sols = [i for i in permutations(range(1,self.size+1),self.size)]
			
		for a in sols:
			for b in [i for i in sols if none_match(a,i)]:
				for c in [i for i in sols if none_match(a,i) and none_match(b,i)]:
					for d in [i for i in sols if none_match(a,i) and none_match(b,i) and none_match(c,i)]:
						att_sol = (a,b,c,d)
						if(self.check_board(att_sol)):
							return(att_sol)
	
	def box_coords(self, coordinate):
		# Calculate tikz coordinates for a box around one local coordinate
		(x,y) = coordinate
		p = 2 * (x - 1)
		q = 2 * (5 - y)
		return([[(p,q), (p,q-2)], [(p,q-2),(p+2,q-2)], [(p+2,q-2),(p+2,q)], [(p+2,q),(p,q)]])
	
	def tikz_coords(self, id):
		# draw a box around the ids
		coordinates = self.board[id][2]
		t_coords = []
		for c in coordinates:
			# c = (1,1)
			b = self.box_coords(c)
			# b =  [[(0,8),(0,6)],[(0,6),(2,6)],[(2,6),(2,8)],[(2,8),(0,8)]]
			for d in b:
				# d = [(0,8),(0,6)]
				if d in t_coords or d[::-1] in t_coords:
					try:
						t_coords.remove(d)	
					except:
						t_coords.remove(d[::-1])
				else:
					t_coords.append(d)
		outstr = ""
		
		return(t_coords)
	
	def gen_latex(self, solve=True):
		# Generates pdfLaTeX source for puzzle
		head =\
"""\\documentclass{article}

\\usepackage{tikz}

\\pagenumbering{gobble}

\\begin{document}

\\begin{tikzpicture}
	
	% The Grid
	\\draw[step=2cm,gray,very thin] (0,0) grid (8,8);

"""
		
		body = 	""
		
		tail =\
"""
\\end{tikzpicture}

\\end{document}
"""
		
		op_dict = { "-":"--", "*":"$\\times$", "/":"$\\div$", " ":" ", "+":"+" }
		
		for id in self.board:
			
			coords = self.tikz_coords(id)
			first_t = coords[0]
			body += "\t% id: " + str(id) + "\n"
			for t in coords:
				body += "\t\\draw[thick] "
				body += str(t[0]) + " -- " + str(t[1])
				if t[1] == first_t[0]:
					op = self.board[id][0]
					body += " node[anchor=north west] {"					
					body += str(self.board[id][1]) + " " + op_dict[op] + "};\n"
				else:
					body += ";\n"
			body += "\n"
					
		if solve:
			body += "\t% Solution\n"
			solved = self.solve()
	
			for row in range(self.size):
				for col in range(self.size):
					body += "\t\\draw (" + \
							str(2*col+1) + "," + str(6-2*row+1) + \
							") node[anchor=center] {\\Huge " + \
							str(solved[row][col]) + "};\n"

		return(head + body + tail)
		
if __name__ == "__main__":	
	import test