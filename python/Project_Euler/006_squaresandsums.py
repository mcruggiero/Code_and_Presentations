import time
start = time.clock()

sums = 0
squares = 0
end = int(input())

for use in range(1,end + 1):
    sums = 0
    squares = 0
    print("Number ", use)
    for i in range (1, use + 1):
        sums += i * i
        squares += i

    print(sums)
    print(squares)
    print(squares * squares)
    print("Answer ", squares * squares - sums)
    print(20*'#')


end = time.clock()
print ("the running time: %s ms" %((end - start)*1000))

## Or I could have been smart and remembered sumation formulas sum(n,i) = N * (N+1) / 2 derp