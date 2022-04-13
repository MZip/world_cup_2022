from cup import Cup
from collections import Counter

cup = Cup()


runs = []
#n=100_000
#n=10_000
n=1_000
for i in range(n):
    cup = Cup()
    winner = cup.simulate()
    print(f"{i+1}/{n}") #, end="\r"
    runs.append(winner)
print(Counter(runs))