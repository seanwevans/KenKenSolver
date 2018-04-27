# given a list of local coordinates, convert to tikz coordinates with a box.
#	tikz
# (0,8)	 _______________________________
# 		| (1,1) | (2,1) | (3,1) | (4,1) |
# (0,6)	|_local_|_______|_______|_______|
#		| (1,2) | (2,2) | (3,2) | (4,2) |
# (0,4)	|_______|_______|_______|_______|
#		| (1,3) | (2,3) | (3,3) | (4,3) |
# (0,2)	|_______|_______|_______|_______|
# 		| (1,4) | (2,4) | (3,4) | (4,4) |
# (0,0)	|_______|_______|_______|_______|
#				(2,0)	(4,0)	(6,0)	(8,0)
# For example if the list of local coordinates was [(1,1), (2,1), (2,2)]
# We would need to output [[(0,8),(0,6)],[(0,6),(2,6)],[(2,6),(2,4)],[(2,4),(4,4)],[(4,4),(4,6)],[(4,6),(4,8)],[(4,8),(2,8)],[(2,8),(0,8]]
# [(1,1)] ==> [[(0,8),(0,6)],[(0,6),(2,6)],[(2,6),(2,8)],[(2,8),(0,8)]]

def box_coords(coordinate):
		# Calculate tikz coordinates for a box around one local coordinate
		(x,y) = coordinate
		p = 2 * (x - 1)
		q = 2 * (5 - y)
		return([[(p,q), (p,q-2)], [(p,q-2),(p+2,q-2)], [(p+2,q-2),(p+2,q)], [(p+2,q),(p,q)]])
		
def tikz_box(coordinates):
	a = []
	for c in coordinates:
		# c = (1,1)
		b = box_coords(c)
		# b =  [[(0,8),(0,6)],[(0,6),(2,6)],[(2,6),(2,8)],[(2,8),(0,8)]]
		for d in b:
			# d = [(0,8),(0,6)]
			if d in a or d[::-1] in a:
				try:
					a.remove(d)	
				except:
					a.remove(d[::-1])
			else:
				a.append(d)
	return(a)
	
print(tikz_box([(1,1),(2,1),(2,2)]))