#author Jianheng qiu 8852908632
#x is x axis value and y is y axis value
#ans is the number of activity points collected
#num is the count of the mumber of assigned officers
def DFS_search(x, y, ans, num):
	global max_value
	global visited	
	num += 1
	ans += map[x][y]			
	if num >= officers:
		#all the officers must be assigned to a specific position.
		if ans > max_value:
			max_value = ans
		return
	#every row in the city area
	for x_next in range(scale):
		#to chack whether a position is available
		check = 0
		for y_used in range(num):
			x_used = visited[y_used]
			#the position cannot conflict with each other
			if x_next == x_used or abs(y + 1 - y_used) == abs(x_next - x_used):
				check = 1
				break
		if check == 0:
			visited[num] = x_next
			DFS_search(x_next, y + 1, ans, num)
			visited[num] = -1


f = open("input.txt", "r")
g = open("output.txt", "w")

flag = 0
scale = 0
officers = 0
scooters = 0

for x in f:
	if flag == 0:
		scale = int(x)
		map = [[0 for col in range(scale)] for row in range(scale)]
	elif flag == 1:
		officers = int(x)
	elif flag == 2:
		scooters = int(x)
	else:
		#store the route of scooters in the map
		map[int(x[0])][int(x[2])] += 1		
	flag = flag + 1
	
#the max value of activity positions	
max_value = 0
for x_in in range(scale):

	visited = [-1 for i in range(scale)]
	visited[0] = x_in
	ans = 0
	DFS_search(x_in, 0, ans, 0)	
	
g.write(str(max_value))
f.close()
g.close()

