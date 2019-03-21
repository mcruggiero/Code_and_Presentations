#THis answer is all FUBAR so I will try another iteratiron

import time
start = time.clock()

end = int(input())
List = []
PList = []

def isprime(n):

	for m in range(2,int(n ** 0.5) + 1):
		print(n, m, int(n%m))
		if not n%m:
			return False
	return True

print(20*"#")

for i in range(2,end):
	if isprime(i):
		List.append(i)

for i in range(0,len(List)):
	print(i+1,List[i], "\n")
	PList.append([[i+1],List[i]])


end = time.clock()
print ("the running time: %s ms" %((end - start)*1000))