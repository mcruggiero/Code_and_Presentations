#023 Find the sum of all the positive integers 
# which cannot be written as the sum of two abundant numbers.

import time
start = time.clock()
###########

def divisors(n):
    result = set()
    for i in range(2, int(n ** 0.5) + 1): #Change the first term to one if you want to include the factor 
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div} #This symbol took me a while to figure. It means set = to union 
    yield 1
    for i in result:
        yield i

def is_abundant(n):
	if n < 12:
		return False
	return sum(divisors(n)) > n

def is_abundant_sum(n):
	for i in abundants:
		if i > n:  # assume "abundants" is ordered
			return False
		if (n - i) in abundants_set:
			return True
	return False

abundants = list(x for x in range(1, 28123 + 1) if is_abundant(x))
abundants_set = set(abundants)
test = set()
sumo = 0

for x in range(1, 28123 + 1):
	if is_abundant_sum(x) is False:
		sumo += x
		print(x, sumo)

		test = test | {x}
###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )