#012 What is the value of the first triangle number to have over five hundred divisors?

import time
start = time.clock()

prime = []
factors = [1]
count = 0

def Tnum(n):
	return int(n * (n+1) / 2)

def Sieve(n):
	np1 = n + 1
	s = list(range(np1))
	s[1] = 0
	sqrtn = int(round(n**.5))
	for i in range(2, sqrtn + 1): 
		if s[i]:
			s[i*i: np1: i] = [0] * len(range(i*i, np1, i))
			filter(None, s)
	for i in s:
		if i != 0:
			prime.append(i)
	return prime

def Factor(n):
	for i in prime[:int(((n**.5)  + 1))]:
		if n%i == 0:
			factors.append(i)
			factors.append(int(n/i))

	for j in factors:
		for k in factors:
			if ( k%j == 0 and
				int(k/j) not in factors):

				factors.append(int(k/j))

	for j in range(1,len(factors)):
		for k in factors: 
			if (k%factors[j] == 0 and 
				int(k/factors[j]) not in factors):

				factors.append(int(k/j))

	factors.append(n)
	factors.sort()	
	return factors

count = 1
Sieve(9000)


while True:
	tester = Factor(Tnum(count))
	# print(count, Tnum(count), len(tester))
	# print(tester, "\n")
	if len(tester) > 500:
		print(count, Tnum(count), len(tester))
		break
	count += 1
	factors = [1]

end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )