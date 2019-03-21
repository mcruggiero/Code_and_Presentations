def factors(n):    
    result = set()
    for i in range(2, int(n ** 0.5) + 1): #Change the first term to one if you want to include the factor 
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div} #This symbol took me a while to figure. It means set = to union 
    yield 1
    for i in result:
        yield i