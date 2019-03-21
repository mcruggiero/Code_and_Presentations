#015 How many such routes are there through a 20×20 grid?
import time
start = time.clock()

def factorial(n):
     if n == 0:
         return 1
     else:
         return n * factorial(n-1)

def Binomial(n,k):
	return int(factorial(n)/(factorial(k)*factorial(n-k)))

print(Binomial(40,20))

end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )