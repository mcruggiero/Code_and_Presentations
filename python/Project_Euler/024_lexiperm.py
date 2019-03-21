#024 What is the millionth lexicographic 
#　permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

import time
start = time.clock()
###########

Strip = "ABC"
List = set()

for i in range(0,len(Strip)):
	List |= {Strip[i]}

Result = List
Results = set()

for n in List:
	for i in Result:
		if n != i:
			Results |= {n + i}
			Results |= {i + n}

print(Results)




###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )