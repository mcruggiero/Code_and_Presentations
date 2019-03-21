#024 what is the longest recurring cycle in its decimal fraction part? 

import time
start = time.clock()
###########
def Sieve(limit):
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

def Poly(a,b, count):
	for n in range(count):
		yield (n**2) + a * n + b

def Poly_Primer(size):
	Prime_List = set()
	bs = []
	for x in Sieve(5000):
		Prime_List |= {x}	# This is the list that is returned from Sieve
		if x < 1000:
			bs.append(x)
	for a in range(-size,size + 1):
		for b in bs:
			Poly_List = []		
			for x in Poly(a,b, 1000): # Here we calculate the polynomial
				Poly_List.append(x)
			i = 0
			for number in range(1,len(Poly_List)):
				if Poly_List[number] in Prime_List:
					yield [int(i + 1) , a, b]
					i += 1
				else:
					break
lists = []
i = 0
for x in Poly_Primer(1000):
	if int(x[0]) > i:
		i = x[0]
		print(x)


# This is not the best way to make this calculation. I should just make a brute force test. 
###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )