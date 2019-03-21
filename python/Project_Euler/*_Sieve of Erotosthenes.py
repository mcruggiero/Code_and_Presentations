import time
start = time.clock()

n = int(input("Number to stop looking for primes: "))
prime = []

# def Sieve(n):
# 	np1 = n + 1
# 	s = list(range(np1))
# 	s[1] = 0
# 	sqrtn = int(round(n**.5))
# 	for i in range(2, sqrtn + 1): 
# 		if s[i]:
# 			s[i*i: np1: i] = [0] * len(range(i*i, np1, i))
# 			filter(None, s)

# 	for i in s:
# 		if i != 0:
# 			prime.append(i)

# 	return prime

# Sieve(n)
# print(prime)

def Sieve2(limit):
    yield 2
    if limit < 3: return
    lmtbf = (limit - 3) // 2
    buf = [True] * (lmtbf + 1)
    for i in range((int(limit ** 0.5) - 3) // 2 + 1):
        if buf[i]:
            p = i + i + 3
            s = p * (i + 1) + i
            buf[s::p] = [False] * ((lmtbf - s) // p + 1)
    for i in range(lmtbf + 1):
        if buf[i]: yield (i + i + 3)

for x in Sieve(n):
	print(x)




######################################
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )