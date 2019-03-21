#015 What is the sum of the digits of the number 2**1000?
import time
start = time.clock()

a = 2**1000
print(a)
b = str(a)
count = 0

for i in range(len(b)):
	print(i)
	count += int(b[i])

print(count)

end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )