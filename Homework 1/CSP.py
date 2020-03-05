import sys
import itertools

junk, a,b,c =sys.argv
abc = a+b+c
print
unique_letters = []
for x in abc:
    if x not in unique_letters: 
        unique_letters.append(x)
solutions = []
all_letters = list(itertools.chain(a,b,c))
all_unique = []

for i in all_letters:
    if i not in all_unique:
        all_unique.append(i)

for perm in itertools.permutations(range(10),len(unique_letters)):
    possible = dict()
    sum_a=0
    sum_b=0
    sum_c=0
    for i in range(len(unique_letters)):
        possible[unique_letters[i]] = perm[i]
        if len(possible) == len(unique_letters):
            for j in range(len(a)):
                sum_a+=possible[a[j]] * (10**j)
                for k in range(len(b)):
                    sum_b+=possible[b[k]] * (10**k)
                    for l in range(len(c)):
                        sum_c+=possible[c[l]] * (10**l)
                    if(sum_c==sum_a+sum_b):
                        solutions.append(possible)