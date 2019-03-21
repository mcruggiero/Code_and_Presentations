import time
start = time.clock()

number = int(input())
List = []

def is_prime(num):
	if num == 0 or num == 1:
		return False
	for x in range(2,num):
		if num % x == 0:
			return False
		else:
			return True

x = [x for x in range(1,number) if is_prime(x)]

i = 0
while i < len(x):
	if i < 10002:
		print(i + 2, x[i])
		i += 1
	else: 
		break


end = time.clock()
print ("the running time: %s ms" %((end - start)*1000))