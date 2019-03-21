#010 Find the sum of all the primes below two million.

import time
start = time.clock()
a = 0

def isprime(n):
	for m in range(2,int(n ** 0.5) + 1):
		if not n%m:
			return False
	return True

for i in range(2,2000000):
	if isprime(i):
		a = a + i
		print(i, a, "\n")

print(a)
end = time.clock()
print ("the running time: %s ms" %((end - start)))