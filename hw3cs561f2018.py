import numpy as np
	
def get_rewards(obstacle, state, info_car_end, car_num):
	if state in obstacle:
		return -101.0
	elif state == info_car_end[car_num]:
		return 99.0
	else:
		return -1.0
	
	
def value_iteration(states_list, expected_value_dict, move_to_list, size, car_num, info_car_end, obstacles):
	actions = ['N', 'S', 'E', 'W']
	gamma = 0.9
	for iteration in xrange(1000):
		delta = 0.0
		for state in states_list:
			if state == info_car_end[car_num]:
				continue
			action_suggest = actions[0]
			r = get_rewards(obstacles, state, info_car_end, car_num)
			value_cal = r + gamma * get_expected_value(expected_value_dict, action_suggest, state, size)
			for action in actions:
				r = get_rewards(obstacles, state, info_car_end, car_num)
				if value_cal < r + gamma * get_expected_value(expected_value_dict, action, state, size):
					action_suggest = action
					value_cal = r + gamma * get_expected_value(expected_value_dict, action, state, size)
				else:
					continue
			delta = delta + abs(value_cal - expected_value_dict[state])
			move_to_list[state] = action_suggest
			expected_value_dict[state] = value_cal
		
		if delta < 1e-6:
			break
			
	return move_to_list, expected_value_dict
	
def get_expected_value(expected_value_dict, action, state, size):
	north_value = get_north_value(expected_value_dict, state, size)
	south_value = get_south_value(expected_value_dict, state, size)
	east_value = get_east_value(expected_value_dict, state, size)
	west_value = get_west_value(expected_value_dict, state, size)
	cal_value = 0.0
	if action == 'N':
		cal_value = 0.7 * north_value + 0.1 * (south_value + east_value + west_value)
	elif action == 'S':
		cal_value = 0.7 * south_value + 0.1 * (north_value + east_value + west_value)
	elif action == 'E':
		cal_value = 0.7 * east_value + 0.1 * (north_value + south_value + west_value)
	else:
		cal_value = 0.7 * west_value + 0.1 * (north_value + south_value + east_value)
	return cal_value
		
def get_north_value(expected_value_dict, state, size):
	north_state_row = state[0] + 0
	north_state_col = state[1] - 1
	north_state = (north_state_row, north_state_col)
	if not check_location_available(north_state, size):
		north_state = state
	return expected_value_dict[north_state]

def get_south_value(expected_value_dict, state, size):
	south_state_row = state[0] + 0
	south_state_col = state[1] + 1
	south_state = (south_state_row, south_state_col)
	if not check_location_available(south_state, size):
		south_state = state
	return expected_value_dict[south_state]
	
def get_east_value(expected_value_dict, state, size):
	east_state_row = state[0] + 1
	east_state_col = state[1] + 0
	east_state = (east_state_row, east_state_col)
	if not check_location_available(east_state, size):
		east_state = state
	return expected_value_dict[east_state]
	
def get_west_value(expected_value_dict, state, size):
	west_state_row = state[0] - 1
	west_state_col = state[1] + 0
	west_state = (west_state_row, west_state_col)
	if not check_location_available(west_state, size):
		west_state = state
	return expected_value_dict[west_state]

def simulator(movement, car_num, info_car_start, info_car_end, size, obstacles):
	total_earned = 0.0
	average_earned = 0
	for j in range(10):
		pos = info_car_start[car_num]
		earned = 0.0 
		np.random.seed(j)
		swerve = np.random.random_sample(1000000)
		k = 0
		while pos != info_car_end[car_num]:
			move = movement[pos]
			if swerve[k] > 0.7:
				if swerve[k] > 0.8:
					if swerve[k] > 0.9:
						move = turn_right(turn_right(move))
					else:
						move = turn_right(move)
				else:
					move = turn_left(move)
			pos = take_move(move, pos, size)
			earned = earned - 1
			if pos in obstacles:
				earned = earned - 100.0
			k = k + 1
		earned = earned + 100.0
		total_earned = total_earned + earned
	average_earned = int(np.floor(total_earned / 10))
	return average_earned
	
def take_move(move, pos, size):
	direction = {"N": [0, -1], "S": [0, 1], "E":[1, 0], "W":[-1,0]}
	next_pos_row = pos[0] + direction[move][0]
	next_pos_col = pos[1] + direction[move][1]
	next_pos = (next_pos_row, next_pos_col)
	if not check_location_available(next_pos, size):
		next_pos = pos
	return next_pos
	
def check_location_available(state, size):
	if state[0] < 0 or state[0] >= size:
		return False
	elif state[1] < 0 or state[1] >= size:
		return False
	else:
		return True
		
def turn_left(move):
	if move == "N":
		return "W"
	elif move == "S":
		return "E"
	elif move == "E":
		return "N"
	elif move == "W":
		return "S"

def turn_right(move):
	if move == "N":
		return "E"
	elif move == "S":
		return "W"
	elif move == "E":
		return "S"
	elif move == "W":
		return "N"
		
input_file = open("input.txt")
information = input_file.readlines()
information = [line.strip() for line in information]

rewards = dict()
size = int(information[0])
total_car = int(information[1])
total_obstacle = int(information[2])

obstacles = []
for index in range(0, total_obstacle):
	obstacle_s = information[3 + index]
	obstacle_l = obstacle_s.split(",")
	obstacles.append((int(obstacle_l[0]), int(obstacle_l[1])))
	rewards[(int(obstacle_l[0]), int(obstacle_l[1]))] = -101.0

index_forward = 3 + total_obstacle
info_car_start = dict()
for index in range(0, total_car):
	start_s = information[index_forward + index]
	start_l = start_s.split(",")
	info_car_start[index] = (int(start_l[0]), int(start_l[1]))

index_forward = index_forward + total_car
info_car_end = dict()
for index in range(0, total_car):
	end_s = information[index_forward + index]
	end_l = end_s.split(",")
	info_car_end[index] = (int(end_l[0]), int(end_l[1]))
	rewards[(int(end_l[0]), int(end_l[1]))] = 99.0

	
actions = ['N', 'S', 'E', 'W']
states = []
for row in range(size):
	for col in range(size):
		states.append((row,col))

expect_value = dict()
movement = dict()
car_num = 3
output_file = open("output.txt", "a")
for car_num in range(total_car):
	move_to = dict()
	expected_value = dict()
	for row in range(size):
		for col in range(size):
			move_to[(row,col)] = ""
			expected_value[(row,col)] = -1.0
	for initial in obstacles:
		expected_value[initial] = -101.0
	stop = info_car_end[car_num]
	expected_value[stop] = 99.0
	movement, expect_value= value_iteration(states, expected_value, move_to, size, car_num, info_car_end, obstacles)
	average = simulator(movement, car_num, info_car_start, info_car_end, size, obstacles)
	output_file.write(str(average))
	output_file.write("\n")
output_file.close()