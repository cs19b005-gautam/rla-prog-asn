import math

def get_state_space(n):
    state_space = []
    state_space.append(list('0'*(n**2)))
    def swapper(l, start, curr):
        for i in range(start, curr):
            if l[i] == l[curr]:
                return 0
        return 1


    def findPermutations(l, index, n):
        if index >= n:
            state_space.append(l.copy())
            return

        for i in range(index, n):

            check = swapper(l, index, i)
            if check:
                l[index], l[i] = l[i], l[index]
                findPermutations(l, index + 1, n)
                l[index], l[i] = l[i], l[index]

    max_tries = 1+math.floor((n**2)/2)
    for i in range(1,max_tries):
        o = '2'
        x = '1'
        l = list('0'*(n**2))
        num = 0
        for j in range(0,i):
            l[j] = '1'
            num = j
        for j in range(num+1, num+1+i):
            if(j<n**2 -1):
                l[j] = '2'
                num = j
        findPermutations(l, 0, n**2)
    return state_space