import copy
from random import randint 
import pickle
from prettytable import PrettyTable
import prettytable
import time


def decimal_to_three_base(num):
	vars = [0]*9
	three_pows = [1,3,9,27,81,243,729,2187,6561]
	t= num
	for j in xrange(8, -1, -1):
		vars[j] = t/three_pows[j]
		t = t%three_pows[j]
	p = [vars[8:5:-1], vars[5:2:-1],vars[2::-1]]
	return p
    

def categorize(state):
	if (state[0][0] == 2 and state[0][1] == 2 and state[0][2] == 2) or (
		state[1][0] == 2 and state[1][1] == 2 and state[1][2] == 2) or (
		state[2][0] == 2 and state[2][1] == 2 and state[2][2] == 2) or (
		state[0][0] == 2 and state[1][0] == 2 and state[2][0] == 2) or (
		state[0][1] == 2 and state[1][1] == 2 and state[2][1] == 2) or (
		state[0][2] == 2 and state[1][2] == 2 and state[2][2] == 2) or (
		state[0][0] == 2 and state[1][1] == 2 and state[2][2] == 2) or (
		state[0][2] == 2 and state[1][1] == 2 and state[2][0] == 2):
		return 0 # GAME WON 
	if (state[0][0] == 0 and state[0][1] == 0 and state[0][2] == 0) or (
		state[1][0] == 0 and state[1][1] == 0 and state[1][2] == 0) or (
		state[2][0] == 0 and state[2][1] == 0 and state[2][2] == 0) or (
		state[0][0] == 0 and state[1][0] == 0 and state[2][0] == 0) or (
		state[0][1] == 0 and state[1][1] == 0 and state[2][1] == 0) or (
		state[0][2] == 0 and state[1][2] == 0 and state[2][2] == 0) or (
		state[0][0] == 0 and state[1][1] == 0 and state[2][2] == 0) or (
		state[0][2] == 0 and state[1][1] == 0 and state[2][0] == 0):
		return 1 # GAME LOST
	exp = True
	for i in range(0,3):
		if not exp:
			break
		for j in range(0,3):
			if state[i][j] == 1:
				exp = False
				break
	if exp:
		return 2 # TIE
	else:
		return 3 # GAME ON

def set_initial_values(state_num, good_states, bad_states):
	global learning_rate
	learning_rate = 0.5
	good_value = 1000
	bad_value = -1000
	tie_value = 100
	for i in xrange(0, 19683):
		state = decimal_to_three_base(i)
		category = categorize(state)
		if category == 0:
			good_states.append(state)
			state_num[i] = good_value
		elif category == 1:
			bad_states.append(state)
			state_num[i] = bad_value
		elif category == 2:
			tie_states.append(state)
			state_num[i] = tie_value

def vaild_goto_states(current_state):
	if current_state in good_states or current_state in bad_states:
		return [init_state]
	goto_states = []
	for i in range(0,3):
		for j in range(0,3):
			if current_state[i][j] == 1:
				new_state = copy.deepcopy(current_state)
				new_state[i][j] = 2
				goto_states.append(copy.deepcopy(new_state))
				new_state[:] = []
	return goto_states

def is_invalid_choice(i, j, current_state):
	return i < 0 or j < 0 or i > 2 or j > 2 or current_state[i][j] != 1

def convert_state_to_decimal(state):
	decimal_value = 0
	three_pow = 6561
	for k in range(0, 9):
		i = k/3
		j = k%3
		decimal_value += three_pow * state[i][j]
		three_pow /= 3
	return decimal_value 

learning_rate = 0.0
try:
	state_num_temp = pickle.load(open('save_vstar.p', 'rb'))
	choice = raw_input('Load previous progress - Y\~Y : ')
	if choice == 'Y':
		state_num = state_num_temp
	else:
		state_num = [0]*19683
except:
	state_num = [0]*19683

good_states = []
bad_states = []
tie_states = []
state = [[1,1,1], [1,1,1], [1,1,1]]

set_initial_values(state_num, good_states, bad_states)
init_state = [[1,1,1],[1,1,1],[1,1,1]]
current_state = copy.deepcopy(init_state)
mapping = {0:'O', 1: ' ', 2: 'X'}
iter1 = True
while(True):
	pickle.dump(state_num, open('save_vstar.p', 'wb'))
	if iter1:
		print 'Current State of the Game :'
		t = PrettyTable(header = False, hrules = prettytable.ALL)
		t.add_row([mapping[current_state[0][0]], mapping[current_state[0][1]], mapping[current_state[0][2]]])
		t.add_row([mapping[current_state[1][0]], mapping[current_state[1][1]], mapping[current_state[1][2]]])
		t.add_row([mapping[current_state[2][0]], mapping[current_state[2][1]], mapping[current_state[2][2]]])
		print t

	print 'Machine Thinking...'
	time.sleep(1)

	goto_states = vaild_goto_states(current_state)
	n = len(goto_states)
	max_vstar = -10000
	for state in goto_states:
		temp = state_num[convert_state_to_decimal(state)]
		if temp > max_vstar:
			max_vstar = temp
			try:
				goto_state[:] = []
			except:
				pass
			goto_state = copy.deepcopy(state)

	if goto_state == init_state:
		current_state = copy.deepcopy(init_state)
		print 'Returning to initial state'
		continue
	
	temp = learning_rate*state_num[convert_state_to_decimal(goto_state)]
	
	state_num[convert_state_to_decimal(current_state)] = temp
	
	current_state[:] = []
	current_state = copy.deepcopy(goto_state)
	# print 'Now, machine has made a move, current state has become :',
	# print current_state
	# print state_num[convert_state_to_decimal(goto_state)]
	t.clear()
	t = PrettyTable(header = False, hrules = prettytable.ALL)
	t.add_row([mapping[current_state[0][0]], mapping[current_state[0][1]], mapping[current_state[0][2]]])
	t.add_row([mapping[current_state[1][0]], mapping[current_state[1][1]], mapping[current_state[1][2]]])
	t.add_row([mapping[current_state[2][0]], mapping[current_state[2][1]], mapping[current_state[2][2]]])
	print t

	if current_state in good_states:
		print 'The machine has won!\nRise of the planet of the Duex Machina!'
		current_state[:] = []
		current_state = copy.deepcopy(init_state)
		t = raw_input('Press enter to continue')
		continue

	if current_state in bad_states:
		print 'User has won'
		current_state[:] = []
		current_state = copy.deepcopy(init_state)
		t = raw_input('Press enter to continue')
		continue

	if current_state in tie_states:
		print 'Its a TIE!'
		current_state[:] = []
		current_state = copy.deepcopy(init_state)
		t = raw_input('Press enter to continue')
		continue

	print 'YOUR MOVE!'
	i = -1
	j = -1
	while is_invalid_choice(i, j, current_state):
		str_arr = raw_input('Input an available cell number (Eg. format -> 0 2 ) : ').split(' ') 
		i,j = [int(num) for num in str_arr]

	prev_state = copy.deepcopy(current_state)
	current_state[i][j] = 0
	# print 'New Current State after user input is = ',
	# print current_state
	t.clear()
	t = PrettyTable(header = False, hrules = prettytable.ALL)
	t.add_row([mapping[current_state[0][0]], mapping[current_state[0][1]], mapping[current_state[0][2]]])
	t.add_row([mapping[current_state[1][0]], mapping[current_state[1][1]], mapping[current_state[1][2]]])
	t.add_row([mapping[current_state[2][0]], mapping[current_state[2][1]], mapping[current_state[2][2]]])
	print t
	t.clear()
	temp = learning_rate*state_num[convert_state_to_decimal(current_state)]
	state_num[convert_state_to_decimal(prev_state)] = temp

	if current_state in bad_states:
		print 'User has won!'
		current_state[:] = []
		current_state = copy.deepcopy(init_state)
		t = raw_input('Press enter to continue')
		continue
	
	if current_state in tie_states:
		print 'Its a TIE!'
		current_state[:] = []
		current_state = copy.deepcopy(init_state)
		t = raw_input('Press enter to continue')
		continue