#015 What is the sum of the digits of the number 2**1000?
import time
start = time.clock()

a = [0] * 15

a[14] =  "75"
a[13] =  "95 64"
a[12] =  "17 47 82"
a[11] =  "18 35 87 10"
a[10] =  "20 04 82 47 65"
a[9] =  "19 01 23 75 03 34"
a[8] =  "88 02 77 73 07 63 67"
a[7] =  "99 65 04 28 06 16 70 92"
a[6] =  "41 41 26 56 83 40 80 70 33"
a[5] =  "41 48 72 33 47 32 37 16 94 29"
a[4] = "53 71 44 65 25 43 91 52 97 51 14"
a[3] = "70 11 33 28 77 73 17 78 39 68 17 57"
a[2] = "91 71 52 38 17 14 91 43 58 50 27 29 48"
a[1] = "63 66 04 68 89 53 67 30 73 16 69 87 40 31"
a[0] = "04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"

for i in range(0, len(a)):
	a[i] = a[i].split(" ")
	for j in range(0,len(a[i])):
		a[i][j] = int(a[i][j])

print(a)

for i in range(1,len(a)):
	for j in range(0,len(a[i])):
		a[i][j] = a[i][j] + (max(a[i-1][j],a[i-1][j+1] ))
		print(i, a[i], "\n")


print(a)


end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )