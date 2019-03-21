#024 What is the index of the first term in the Fibonacci sequence to contain 1000 digits?

import time
start = time.clock()
###########

#def Fibonacci(n):
#    if n == 1:
#        return 1
#    elif n == 2:
#    	return 1
#    else:
#    	return Fibonacci(n - 1) + Fibonacci(n - 2)

Fibonacci = {1: 1,2: 1}

for i in range(3,4000000):
	Fibonacci[i] = Fibonacci[i-1] + Fibonacci[i-2]
	if Fibonacci[i] > 10**(1000-1):
		print(Fibonacci[i])
		print(i)
		break



###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )