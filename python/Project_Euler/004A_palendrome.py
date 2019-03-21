# Problem 004
# A palindromic number reads the same both ways. 
# The largest palindrome made from the product of two 2-digit numbers is 
# 9009 = 91 × 99. Find the largest palindrome 
# made from the product of two 3-digit numbers.

#This will never work in any reasonable amount of time 100! ~ 9X10^157


import timeit
start = timeit.default_timer()

ptop = 100
bottom = 100
counter = 0
List = [ ]

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

while ptop < 1000 :
 	bottom = 100 + counter

 	while bottom < 1000 :
 		test = ptop * bottom

 		if ( test5(test) or test6(test)):
 			List.append([test,ptop, bottom])

 		bottom += 1

 	bottom += 1
 	counter += 1




print(List)

stop = timeit.default_timer()
print(stop - start)

