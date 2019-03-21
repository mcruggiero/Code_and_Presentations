#019 Find the sum of the digits in the number 100!
import time
start = time.clock()
###########

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

test = str(factorial(100))
sumo = 0

for i in test:
	i = int(i)
	sumo += i
	print(i, sumo)


###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )