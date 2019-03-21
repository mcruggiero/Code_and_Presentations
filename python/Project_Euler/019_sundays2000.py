#019 How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
import time
start = time.clock()
###########
import calendar
import pprint

# a = calendar.monthcalendar(2015, 1)
# pprint.pprint(calendar.monthcalendar(2015, 1))
count = 0

for h in range(1,13):
	print(h)
	for i in range(1901,2001):
		cali = calendar.monthcalendar(i, h)
		for j in range(len(cali)):
			if cali[j][6] == 1:
				count += 1
				print(i, count, cali[j][6])


print(count)
###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )