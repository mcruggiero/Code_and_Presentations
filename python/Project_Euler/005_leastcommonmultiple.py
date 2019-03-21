import time
start = time.clock()
ceiling = int(input("What is the smallest positive number that is evenly divisible by all of the numbers from 1 to X? "))

multiple = 2
for i in range(1 , ceiling + 1):
        if multiple % i == 0:
                continue
        else:
                for j in range(2 , multiple + 1):
                        if (multiple * j) % i == 0:
                                multiple *= j
                                break
print(multiple)

end = time.clock()
print ("the running time: %s ms" %((end - start)*1000))