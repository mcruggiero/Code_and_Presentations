#021 Evaluate the sum of all the amicable numbers under 10000.
import time
start = time.clock()
###########

def factorSum(n):    
    result = set()
    for i in range(2, int(n ** 0.5) + 1): #Change the first term to one if you want to include the factor 
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div} #This |= symbol took me a while to figure. It means set = to union 
    List = [1]
    for i in result:
        List.append(i)
    List.sort()
    sum = 0
    for i in List:
    	sum = sum + i
    return sum

sumo = 0
for i in range(0,10000):
	a = factorSum(i)
	if factorSum(a) == i and a != i:
		sumo += i
		print(a,i, sumo)



###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )