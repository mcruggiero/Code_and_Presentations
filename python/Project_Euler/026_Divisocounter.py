#024 what is the longest recurring cycle in its decimal fraction part? 

import time
start = time.clock()
###########

def Long_Division(Numerator, Divisor, Count):
	Term = 0
	Num = Numerator
	Div = Divisor
	while Term < Count:
		if Div > Num:
			yield 0
			Num = Num * 10
			Term += 1
		elif Num % Div == 0:
			yield int(Num/Div)
			Term = Count
		else: 
			yield int((Num - Num%Div)/Div)
			Num = (Num%Div) * 10
			Term += 1

def Zero_Strip(x):
	i = 0
	Candidate = []
	List = []
	for x in Long_Division(1,x,10000):
		List.append(x)
	while True:
		if List[i] == 0:
			i += 1
		else:
			Candidate = List[i:]
			return Candidate

def List_Counter(x):
	Stip_List = []
	Last_List = []
	a = 0
	for number in Zero_Strip(x):
		Stip_List.append(number)
	for i in range(0,len(Stip_List)):
		Last_List.append(Stip_List[i])
		Candidate = []
		Candidate = Stip_List[i +1+2:2*(i+1)+2]
		if Last_List == Candidate:
			yield [len(Last_List)]
			break

biggest = 0
for i in range(1,1001):
		for x in List_Counter(i):
			if int(x[0]) >= biggest:
				print(i,x)
				biggest = x[0]


# for x in List_Counter(889):
# 	print(x)
###########
end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start, 3), (end - start)*1000)  )