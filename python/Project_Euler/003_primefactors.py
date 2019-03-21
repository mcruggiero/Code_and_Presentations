# Problem 003
# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?
import timeit
start = timeit.default_timer()

PF = []
Fact = []

def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True

a = int(input("What number would you like to factor? "))

def primefactor(n):
	nums = 2
	print(n**.5)
	
	while nums < n**.5 + 1 :
		if n % nums == 0 :
			Fact.append(nums)
			Fact.append(int(n / nums))
		nums += 1

	for factor in Fact:
		if isPrime(factor):
			PF.append(factor)


primefactor(a)
print(Fact)
print(20*'#')
print(PF)
stop = timeit.default_timer()
print(stop - start)

