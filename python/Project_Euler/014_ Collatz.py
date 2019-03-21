#014 

import time
start = time.clock()

List = []

def Collatz(n):
	if n == 1:
		return n
	elif n%2 == 0:
		n = int(n/2)
		return n
	else:
		n = 3*n + 1
		return n

def sizer(n):
	List.append(n)
	while n > 1:
		n = Collatz(n)
		List.append(n)
	return len(List)

biggest = 0
for i in range(1,1000000):
	List = []
	sizer(i)
	if len(List) > biggest:
		winner = [i, len(List)]
		biggest = len(List)

print(winner)

end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )