"""
Developed by - Avikalp Srivastava
Page - github.com/Avikalp7
Description:
A learning program that plays with the users and depends on their inputs to learn optimal strategy
in the classic game of tic-tac-toe.
Concepts used - Reinforcement/ Q-Learning  
"""

import copy
import pickle
import prettytable
import time
from prettytable import PrettyTable


def decimal_to_three_base(num):
	""" Convert a given decimal number to base 3 number and return it in the format of a state [[, , ], [, , ], [, , ]]"""
	vars = [0]*9
	three_pows = [1,3,9,27,81,243,729,2187,6561]
	t = num
	for j in xrange(8, -1, -1):
		vars[j] = t/three_pows[j]
		t = t%three_pows[j]
	p = [vars[8:5:-1], vars[5:2:-1],vars[2::-1]]
	return p
    

def categorize(state):
	""" Given a state, categorize it as winning(good)=0/ losing(bad)=1/ tie=2 or incomplete game=3 state"""
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
	
	tie_exp = True
	for i in range(0,3):
		if not tie_exp:
			break
		for j in range(0,3):
			if state[i][j] == 1:
				tie_exp = False
				break
	if tie_exp:
		return 2 # TIE
	else:
		return 3 # GAME ON


def set_initial_values(state_num, good_states, bad_states, tie_states):
	""" 
	Sets the initial values for leaarning rate, intitial V* values for good/bad/tie final states 
	It also buids the sets - good/bad/tie sets, each containing all possible sets of their respective scenario
	"""
	good_value = 1000
	bad_value = -1000
	tie_value = 100
	for i in xrange(0, 19683):						# Considering all 3^9 states
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

def vaild_goto_states(current_state, good_states, bad_states):
	""" Compute valid states that the machine can go to from the current state and returns them as a list """
	if current_state in good_states or current_state in bad_states:				# If final state reached, return to init
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
	""" Given the choice of state (i, j) by user, check the validity of the move """
	return i < 0 or j < 0 or i > 2 or j > 2 or current_state[i][j] != 1

def convert_state_to_decimal(state):
	""" Converts the given state of game (base 3) to decimal value """
	decimal_value = 0
	three_pow = 6561
	for k in range(0, 9):
		i = k/3
		j = k%3
		decimal_value += three_pow * state[i][j]
		three_pow /= 3
	return decimal_value 

def user_input():
	""" Returns False for continue, True for exit """
	input_str = raw_input('Enter \'X\' to exit, Enter / any other string to continue: ')
	return input_str == 'X'


def main():
	learning_rate = 0.5
	state_num = [0]*19683												# State_Num capture the V* values for states(their dec value)
	try:
		state_num_temp = pickle.load(open('save_vstar.p', 'rb'))		# Check if any progress exists
		choice = raw_input('Load previous progress - Y\~Y : ')	
		if choice == 'Y':
			state_num = state_num_temp									
		else:
			state_num = [0]*19683
	except:
		pass

	good_states = []
	bad_states = []
	tie_states = []
	set_initial_values(state_num, good_states, bad_states, tie_states)
	init_state = [[1,1,1],[1,1,1],[1,1,1]]
	current_state = copy.deepcopy(init_state)
	
	mapping = {0:'O', 1: ' ', 2: 'X'}									# MAPPING : O -> 0, _ -> 1, X -> 2
	
	iter1 = True														# 1st iteration Bool												
	while(True):
		pickle.dump(state_num, open('save_vstar.p', 'wb'))				# Save the progress thus far
		if iter1:														# iter1 is set to false down below
			print 'Current State of the Game :'
			t = PrettyTable(header = False, hrules = prettytable.ALL)
			t.add_row([mapping[current_state[0][0]], mapping[current_state[0][1]], mapping[current_state[0][2]]])
			t.add_row([mapping[current_state[1][0]], mapping[current_state[1][1]], mapping[current_state[1][2]]])
			t.add_row([mapping[current_state[2][0]], mapping[current_state[2][1]], mapping[current_state[2][2]]])
			print t
			

		print 'Machine Thinking...'
		time.sleep(1)

		# Get list of all valid states the machine can goto
		goto_states = vaild_goto_states(current_state, good_states, bad_states)
		
		# Now we find the state with the largest V* / state_num value in the goto states
		max_vstar = -10000
		for state in goto_states:
			temp_max = state_num[convert_state_to_decimal(state)]
			if temp_max > max_vstar:
				max_vstar = temp_max
				try:
					goto_state[:] = []
				except:
					pass
				goto_state = copy.deepcopy(state)
		# If the machine is returning to initial state, notify it to the user
		if goto_state == init_state:
			current_state = copy.deepcopy(init_state)
			print 'Returning to initial state'
			continue
		# Setting the value of state_num/ V* for the current state based on the goto state chosen
		state_num_current_state = learning_rate*state_num[convert_state_to_decimal(goto_state)]
		state_num[convert_state_to_decimal(current_state)] = state_num_current_state
		# Now goto state has become the current state
		current_state[:] = []
		current_state = copy.deepcopy(goto_state)

		t.clear()
		t = PrettyTable(header = False, hrules = prettytable.ALL)
		t.add_row([mapping[current_state[0][0]], mapping[current_state[0][1]], mapping[current_state[0][2]]])
		t.add_row([mapping[current_state[1][0]], mapping[current_state[1][1]], mapping[current_state[1][2]]])
		t.add_row([mapping[current_state[2][0]], mapping[current_state[2][1]], mapping[current_state[2][2]]])
		print t

		if current_state in good_states:
			print 'The machine has won!\nRise of the Deux Ex Machina.'
			current_state[:] = []
			current_state = copy.deepcopy(init_state)
			if user_input():
				exit(0)
			else:
				continue

		if current_state in bad_states:
			print 'User has won'
			current_state[:] = []
			current_state = copy.deepcopy(init_state)
			if user_input():
				exit(0)
			else:
				continue

		if current_state in tie_states:
			print 'Its a TIE!'
			current_state[:] = []
			current_state = copy.deepcopy(init_state)
			if user_input():
				exit(0)
			else:
				continue

		print 'YOUR MOVE!'
		i = -1
		j = -1
		while is_invalid_choice(i, j, current_state):
			print 'Input an available cell number',
			if iter1:
				print '(Eg. format -> 0 2 ) : ',
				iter1 = False
			else:
				print ': ',
			str_arr = raw_input().split(' ') 
			try:
				i,j = [int(num) for num in str_arr]
			except ValueError:
				i, j = [-1, -1]
				continue

		prev_state = copy.deepcopy(current_state)
		current_state[i][j] = 0

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
			if user_input():
				exit(0)
			else:
				continue
		
		if current_state in tie_states:
			print 'Its a TIE!'
			current_state[:] = []
			current_state = copy.deepcopy(init_state)
			if user_input():
				exit(0)
			else:
				continue


if __name__ == '__main__':
	main()