#009 There exists exactly one Pythagorean triplet for which a + b + c = 1000.
#    Find the product abc.
import time
start = time.clock()

a = 1
b = 1
c = 1

for i in range(1,1000):
	for j in range(i+1,1000):
		a = i**2 + j**2
		if ( a ** .5 == int(a ** .5) and i + j + int(a**.5) == 1000) :
			print(i,j,int(a**.5), i + j + int(a**.5))
			print(i*j*int(a**.5))

end = time.clock()
print ("the running time: %s ms" %((end - start)*1000))