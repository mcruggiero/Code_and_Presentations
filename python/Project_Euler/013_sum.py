#013 Work out the first ten digits of the sum of the following one-hundred 50-digit numbers.

import time
start = time.clock()

results = []
sumo = 0
with open('013_list.txt') as inputfile:
    for line in inputfile:
        results.append(line.strip())

for i in range(0, len(results)):
	sumo += int(results[i])

print(sumo)
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )