#024 What is the millionth lexicographic 
#　permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

import time
start = time.clock()
###########

def combinations(iterable, r):
# combinations('ABCD', 2) --> AB AC AD BC BD CD
# combinations(range(4), 3) --> 012 013 023 123
	pool = tuple(iterable)
	n = len(pool)
	if r > n:
		return
	indices = list(range(r))
	yield tuple(pool[i] for i in indices)
	while True:
		for i in reversed(range(r)):
			if indices[i] != i + n - r:
				break
		else:
			return
		indices[i] += 1
		for j in range(i+1, r):
			indices[j] = indices[j-1] + 1
			yield tuple(pool[i] for i in indices)

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

#for x in combinations("ABCD", 3):
	#print(x)
List = []

for x in permutations("0123456789", r=None):
	List.append(x)

print(List[999999])


###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )