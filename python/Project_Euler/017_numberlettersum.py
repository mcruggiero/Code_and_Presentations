#015 What is the sum of the digits of the number 2**1000?
import time
start = time.clock()

n2w = {0: "Zero", 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
             6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
            11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
            15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
            19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
            50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
            90: 'Ninety', 100: 'One Hundred', 200: 'Two Hundred', \
            300: 'Three Hundred', 400: 'Four Hundred', 500: 'Five Hundred', \
            600: 'Six Hundred', 700: 'Seven Hundred', 800: 'Eight Hundred', 900: 'Nine Hundred', \
            1000: 'One Thousand'}

for i in range(1,1000):
	if i not in n2w:
		word = str(i)
		if 1 < len(word) < 3:
			tensDi = int(word[0])
			onesDi = int(word[1])
			n2w[i] = n2w[tensDi * 10] + " " + n2w[onesDi]
		elif 2 < len(word):
			hundDi = int(word[0])
			rest = int(word[1:])
			n2w[i] = n2w[hundDi * 100] + " and " + n2w[rest]

print(n2w)

print(20*"#")

count = 0
for i in range(1,1001):
	runner = n2w[i].replace(" ", "")
	count += len(runner)
	print(i, runner, count)



end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )