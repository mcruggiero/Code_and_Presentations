#014 
import time
start = time.clock()
cache = {1: 1}


def longest_collatz_sequence(t):
    cache = {1: 1}

    def collatz(n):
        if n not in cache:
            cache[n] = collatz(3 * n + 1 if n % 2 else n / 2) + 1

        return cache[n]  # Length of Collatz Chain

    return max(range(1, t), key=collatz)  # Greatest Chain


print (longest_collatz_sequence(10**9))
print (cache)

end = time.clock()
print ("Running time: is about %s s or %s ms" % (round(end - start), (end - start)*1000)  )