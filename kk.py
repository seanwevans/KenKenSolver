#!/usr/bin/env python
from itertools import permutations, product
from functools import reduce
from random import choices

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
	
	# Assumes a square board, returns maximum board dimension
	def find_size(self):
		m = 0
		for k in self.board:
			for (x,y) in self.board[k][2]:
				if x > m:	m = x
				if y > m:	m = y
		return(m)
	
	# Prints board showing id
	def print_board(self):
		for row in range(1, self.size+1):
			for col in range(1, self.size+1):
				for k in self.board:
					if (col, row) in self.board[k][2]:
						print(k, end='')
						break
			print()
	
	# Given a position on the board return appropriate id
	def get_id_from_pos(self, i, j):
			for id in self.board:
				if (j,i) in self.board[id][2]:
					return id
					
	# Prints board showing target numbers and operations
	def print_board2(self):
		
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
	
	# Return True if the list of answers conforms to the operation id.
	def check_id(self, id, answers):
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
	
	# Checks entire board to make sure calculations are valid
	def check_board(self, answers):
		for id in self.board:
			ans = []
			for (x,y) in self.board[id][2]:
				ans.append(answers[y-1][x-1])
			if(not self.check_id(id, ans)):	return False
		return(True)
		
	#
	def check_valid_answer(self, answers):
		valid = [j for j in range(1, self.size+1)]
		for i in answers:
			if sorted(i) != valid: return False
		for i in range(self.size):
			if sorted([x[i] for x in answers]) != valid:	return False
		return True
	
	# Brute force check every permutationsutation to solve puzzle
	def dumb_four_square_solve(self):
		# Only for four squares
		sols = [i for i in permutations(range(1,self.size+1),self.size)]
			
		for a in sols:
			for b in [i for i in sols if none_match(a,i)]:
				for c in [i for i in sols if none_match(a,i) and none_match(b,i)]:
					for d in [i for i in sols if none_match(a,i) and none_match(b,i) and none_match(c,i)]:
						att_sol = (a,b,c,d)
						if(self.check_board(att_sol)):
							return(att_sol)
	
	# Transforms from board coordinates to tikz coordinates
	def box_coords(self, board_coords):
		(x,y) = board_coords
		p = 2 * (x - 1)
		q = 2 * (5 - y)
		return([(p,q), (p,q-2), (p-2,q-2), (p-2,q), (p,q)])
	
	# Generates pdfLaTeX source for puzzle
	def gen_latex(self, solve=True):
		head = """
		\\documentclass{article}
		\\usepackage{tikz}
		\\pagenumbering{gobble}
		\\begin{document}
		\\begin{tikzpicture}
		\\draw[step=2cm,gray,very thin] (0,0) grid (8,8);
		"""
		
		body = 	""
		
		tail = """
		\\end{tikzpicture}
		\\end{document}
		"""
		
		# draw a box around the ids
		def tikz_coords(id):
			
			s = ""
			coords = self.board[id][2]
			
			
			
			
			
			
			
			
			# For a single space
			if len(coords) == 1:
				t_coords = self.box_coords(coords[0])
			else:
				return("(0,8) -- (0,6) -- (6,6) -- (6,8)")
					
			# For more than one space
			pass
			
			
			
			
			
			
			
			
			
			for t in t_coords:
				s += str(t) + " -- "
			s = s[:-4]
			
			return(s)
			# [(1,1), (1,2), (2,1)]
			# [(0,8), (0,6), (0,4), (2,4), (2,6), (4,6), (4,8), (2,8), (0,8)]
			#return("(0,8) -- (0,6) -- (6,6) -- (6,8)")
		
		for id in self.board:
			body += "\\draw[thick] "
			body += tikz_coords(id)
			body += " -- cycle node[anchor=north west] {"
			op = self.board[id][0]
			if op == "-":	op = "--"
			if op == "*":	op = "$\\times$"
			if op == "/":	op = "$\\div$"
			body += str(self.board[id][1]) + " " + op + "};\n"

		if solve:
			solved = self.dumb_four_square_solve()
	
			for row in range(self.size):
				for col in range(self.size):
					body += "\\draw (" + \
							str(2*col+1) + "," + str(6-2*row+1) + \
							") node[anchor=center] {\\Huge " + \
							str(solved[row][col]) + "};\n"

		return(head + body + tail)
		
if __name__ == "__main__":	

	# { id:[operation, target number, position list: [(col, row)]] }	
	kenkendef = 	{	1:['*',	12,	[(1,1),(2,1),(1,2)]	], 
						2:['-',	1,	[(3,1),(3,2)]		], 
						3:[' ',	4,	[(4,1)]				], 
						4:['+',	9,	[(2,2),(2,3),(3,3)]	], 
						5:['/',	2,	[(4,2),(4,3)]		], 
						6:['+',	7,	[(1,3),(1,4),(2,4)]	], 
						7:['-',	2,	[(3,4),(4,4)]		]
					}
	
	kenkendefans = ((3,1,2,4),(4,2,3,1),(1,3,4,2),(2,4,1,3))
	
	kk2 = 			{	1:['*', 24, [(1,1),(2,1),(3,1)]	],
						2:['+', 6, 	[(4,1),(3,2),(4,2)]	],
						3:['+', 9, 	[(1,2),(2,2),(2,3)]	],
						4:['-', 2, 	[(1,3),(1,4)]		],
						5:[' ', 2, 	[(3,3)]				],
						6:['-', 1, 	[(4,3),(4,4)]		],
						7:['/', 2,	[(2,4),(3,4)]		]
					}
	
	kk2ans = ((2,3,4,1),(4,1,3,2),(1,4,2,3),(3,2,1,4))
	
	k2 = KenKen(kk2)
	
	print(k2.gen_latex())