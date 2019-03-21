# Problem 004
# A palindromic number reads the same both ways. 
# The largest palindrome made from the product of two 2-digit numbers is 
# 9009 = 91 × 99. Find the largest palindrome 
# made from the product of two 3-digit numbers.

import timeit
start = timeit.default_timer()
List = []

def test5(n):
	n = str(n)
	if (len(str(n)) == 5 and 
		n[0] == n[4] and 
		n[1] == n[3]):
		return(True)
	else:
		return(False)

def test6(n):
	n = str(n)
	if (len(str(n)) == 6 and 
		n[0] == n[5] and 
		n[1] == n[4] and 
		n[2] == n[3]):
		return(True)
	else:
		return(False)

def PalFactor(n):
	for i in range(100,999):
		if n % i == 0 and 100 < n/i < 999:
			return ([i,int(n/i)])
		else:
			False

for i in range(100*100, 999*999):
	if test5(i) or test6(i):
		List.append(i)

List.reverse()

for i in List:
	if PalFactor(i):
		print(i, PalFactor(i))
		break

# print(List)
stop = timeit.default_timer()
print(stop - start)

