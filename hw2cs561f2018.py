
import copy
import time
class Applicant:
	def __init__(self, 
				ID,
				gender,
				age,
				pets,
				medical_conditions,
				car,
				driver_license,
				days_needed):
		self.ID = ID
		self.gender = gender
		self.age = age
		self.pets = pets
		self.medical_conditions = medical_conditions
		self.car = car
		self.driver_license = driver_license
		self.days_needed = days_needed

class Organization:
	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity
		self.space = [capacity] * 7
		self.applicants = []
		self.efficiency = -1


	def add_applicant(self, applicant):
		# temp_space = array(self.space) - array(applicant.days_needed)
		temp_space = [i - j for i, j in zip(self.space, applicant.days_needed)]

		# no enought space for a new applicant
		if sum([i < 0 for i in temp_space]) > 0:
			return False

		self.space = temp_space
		self.applicants.append(applicant)
		return True

	def remove_applicant(self, applicant):
		if applicant in self.applicants:
			self.space = [i + j for i, j in zip(self.space, applicant.days_needed)]
			self.applicants.remove(applicant)
			return True
		return False

	def calc_efficiency(self):
		self.efficiency = sum([i - j for i, j in zip([self.capacity] * 7, self.space)])



class Applicant_list:
	def __init__(self):
		self.lists = {
			'total': [],    # total list
			'spla': [],     # spla satisfied list
			'lahsa': []     # lahsa satisfied list
		}

		self.best_choice = None

	def spla_satisfied(self, applicant):
		if applicant.car == 'Y' and applicant.driver_license == 'Y' and applicant.medical_conditions == 'N':
			return True
		return False

	def lahsa_satisfied(self, applicant):
		if applicant.gender == 'F' and applicant.age > 17 and applicant.pets == 'N':
			return True
		return False

	def add_applicant(self, applicant):
		self.lists['total'].append(applicant)
		if self.spla_satisfied(applicant):
			self.lists['spla'].append(applicant)
		if self.lahsa_satisfied(applicant):
			self.lists['lahsa'].append(applicant)

	def remove_applicant(self, applicant):
		for key in self.lists:
			if applicant in self.lists[key]:
				self.lists[key].remove(applicant)

	def get_list(self, list_name):
		return self.lists[list_name]  


# first_iter is used for getting the next value (the result we need)
def find_next_applicant(first_iter, applicant_list, current_org, another_org):
	current_list = applicant_list.get_list(current_org.name)
	another_list = applicant_list.get_list(another_org.name)
	if len(current_list) == 0:
		if len(another_list) == 0:
			current_org.calc_efficiency()
			another_org.calc_efficiency()
			return applicant_list, current_org, another_org
		else:
			applicant_list, another_org, current_org = find_next_applicant(False, applicant_list, another_org, current_org)
			return applicant_list, current_org, another_org

	current_efficiency = -1
	another_efficiency = -1

	# flag for stop loop
	no_space = True
	current_list_cp = copy.copy(current_list)
	for applicant in current_list_cp:
		current_org_changed = False
		another_org_changed = False

		current_list.remove(applicant)
		if current_org.add_applicant(applicant):    # add the applicant to current organization
			current_org_changed = True
			no_space = False
			if applicant in another_list:  # remove from another organization
				another_list.remove(applicant)
				another_org_changed = True
		else:
			current_list.append(applicant)
			continue
		applicant_list, another_org, current_org = find_next_applicant(False, applicant_list, another_org, current_org)
		if current_org.efficiency > current_efficiency:
			current_efficiency = current_org.efficiency
			another_efficiency = another_org.efficiency
			if first_iter: # if this is the first iteration, set the best choice
				applicant_list.best_choice = applicant

		# restore the applicant which we deleted from applicant list for iteration
		current_list.append(applicant)
		if current_org_changed: 
			current_org.remove_applicant(applicant)
		if another_org_changed:
			another_list.append(applicant)

	# set current best efficiency for each organization
	current_org.efficiency = current_efficiency
	another_org.efficiency = another_efficiency
	
	# if no space for all applicant, calculate the efficiency to stop this branch
	if no_space:
		current_org.calc_efficiency()
		another_org.calc_efficiency()
	return applicant_list, current_org, another_org

def read_from_file(filename):
	f = open(filename, 'r')
	
	# read first two lines
	lahsa_capacity = int(next(f))
	spla_capacity = int(next(f))

	# initialize organizations and applicant list
	lahsa = Organization('lahsa', lahsa_capacity)
	spla = Organization('spla', spla_capacity)
	applicant_list = Applicant_list()

	# read other lines
	lahsa = Organization('lahsa', lahsa_capacity)
	spla_capacity = Organization('spla', spla_capacity)

	num_lahsa_applicant = int(next(f))
	lahsa_applicant_IDs = [] 
	for i in range(0, num_lahsa_applicant):
		lahsa_applicant_IDs.append(next(f).strip())

	num_spla_applicant = int(next(f))
	spla_applicant_IDs = []
	for i in range(0, num_spla_applicant):
		spla_applicant_IDs.append(next(f).strip())
	
	# read information of applicants
	num_applicant = int(next(f))
	for i in range(0, num_applicant):
		info = next(f).strip()

		ID = info[0:5]
		gender = info[5]
		age = int(info[6:9])
		pets = info[9]
		medical_conditions = info[10]
		car = info[11]
		driver_license = info[12]
		days_needed = list(map(int, info[13:]))

		new_applicant = Applicant(ID,
							gender,
							age,
							pets,
							medical_conditions,
							car,
							driver_license,
							days_needed)

		# save the new applicant into applicant list
		applicant_list.add_applicant(new_applicant)

		# add the applicant (alreadly in a organization) to the organization
		if ID in lahsa_applicant_IDs:
			lahsa.add_applicant(new_applicant)
			applicant_list.remove_applicant(new_applicant)
		if ID in spla_applicant_IDs:
			spla.add_applicant(new_applicant)
			applicant_list.remove_applicant(new_applicant)

	# spla choose next applicant or not
	spla_next = True
	if num_lahsa_applicant < num_spla_applicant:
		spla_next = False

	return applicant_list, lahsa, spla, spla_next

if __name__ == "__main__":
	start_time = time.time()
	applicant_list, lahsa, spla, spla_next = read_from_file("input.txt")
	if not spla_next:   # lahsa select first, then spla
		applicant_list, _, _ = find_next_applicant(True, applicant_list, lahsa, spla)
		applicant_list.remove_applicant(applicant_list.best_choice)
		lahsa.add_applicant(applicant_list.best_choice)

	applicant_list, _, _ = find_next_applicant(True, applicant_list, spla, lahsa)
	#print(applicant_list.best_choice.ID)
	#print(time.time() - start_time)
	output_file = open("output.txt", "w")
	output_file.write(applicant_list.best_choice.ID + "\n")
	output_file.close()

