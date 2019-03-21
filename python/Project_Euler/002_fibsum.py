a = int(input("number to stop at? "))

def firstn(n):
	i = 1
	j = 2
	num = i + j
	while num < n:
		i = j
		j = num
		num = num + i
		print(num)
		if (num % 2 == 0 and num < n):
			yield num

sum_of_first_n = sum(firstn(a)) + 2
print(sum_of_first_n)