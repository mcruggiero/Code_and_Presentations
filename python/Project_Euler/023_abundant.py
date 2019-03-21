#022 What is the total of all the name scores in the file?
import time
start = time.clock()
###########
def is_abundant(n):
    max_divisor = int(n / 2) + 1
    sum = 0
    for x in range(1, max_divisor):
        if n % x == 0:
            sum += x  
    return sum > n

abundants = list(x for x in range(1, 28123) if is_abundant(x))

sums = 0
for i in range(12, 28123):
    for abundant in abundants:
        if abundant >= i and is_abundant(i + abundant):
            sums += i
print(sums)

###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )