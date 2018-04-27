#!/usr/bin/env python
from kk import KenKen

def get_boards_from_file(source):
	puzzles = []
	
	# Read file
	with open(source,'r') as test_questions:
		kenkenques = test_questions.read().rsplit('\n')
		
	# Populate puzzles
	for i in range(len(kenkenques)):
		if kenkenques[i] == '{':
			tmp_dict = {}
			i += 1
			while kenkenques[i] != '}':
				raw_str = kenkenques[i].replace('\t','')
				cc = raw_str.split(':')
				dd = cc[1][:-1]
				if dd[-2:] != "]]":	dd += "]"				
				tmp_dict[int(cc[0])] = eval(dd)
				i += 1
		if kenkenques[i] == '}' and tmp_dict != {}:
			puzzles.append(tmp_dict)
			tmp_dict = {}

	return(puzzles)

def get_answers_from_file(source):
	answers = []

	# Read file
	with open(source,'r') as test_answers:
		kenkenans = test_answers.read().rsplit('\n')
	
	# Populate answers
	for i in range(len(kenkenans)):
		answers.append(eval(kenkenans[i]))
		
	return(answers)

def test_run(questions, answers):
	tests = []

	# Run tests
	for puz in q:
		test = KenKen(puz).solve() == a[q.index(puz)]
		tests.append(test)
	
	return(tests)
		
q = get_boards_from_file('kenkenqs.txt')
a = get_answers_from_file('kenkenans.txt')

# Analyze tests
tests_successfull = test_run(q,a)
no_tests = len(tests_successfull)
if all(tests_successfull):
	print("All tests were successfull!")
else:
	for i in range(no_tests):
		if not tests_successfull[i]:
			print("Test " + str(i+1) + " Failed!")