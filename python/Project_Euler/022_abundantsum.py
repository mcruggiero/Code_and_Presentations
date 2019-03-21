#022 What is the total of all the name scores in the file?
import time
start = time.clock()
###########

names = open('022_names.txt', "r").read().replace("\"", "").split(",")
names.sort()
print(names)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

Letters = {}
tally = 0

for i in range(1,27):
	Letters[letters[i-1]] = i

for i in range(0,len(names)):
	score = 0
	for j in range(0,len(names[i])):
		score = score + int(Letters[names[i][j]])
	score *=(i+1)
	tally += score
	print((i+1), names[i], tally, score)





###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )