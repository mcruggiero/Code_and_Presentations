a = int(input())

def firstn(n):
	i = 1
	j = 2
	num = i + j
	while num < n:
		i = j
		j = num
		num = num + i
		print(num)
		if num % 2 == 0:
			yield num

sum_of_first_n = sum(firstn(a))
print(sum_of_first_n)