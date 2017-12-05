# Student name: Sai srikanth Kola and Saketh
# Date:04/16/2017
# need some python libraries
import copy
from random import Random  # need this for the random number generation -- do not change
import numpy as np
import itertools as itr

# to setup a random number generator, we will specify a "seed" value
# need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

# to get a random number between 0 and 1, use this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

# number of elements in a solution
n = 100

# create an "instance" for the knapsack problem
value = []
for i in range(0, n):
    value.append(myPRNG.uniform(10, 100))

weights = []
for i in range(0, n):
    weights.append(myPRNG.uniform(5, 20))

# define max weight for the knapsack
maxWeight = 5 * n

# change anything you like below this line ------------------------------------

# monitor the number of solutions evaluated
solutionsChecked = 0


# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalValue = np.dot(a, b)  # compute the value of the knapsack selection
    totalWeight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        # print("Oh no! The solution is infeasible!  What to do?  What to do?")  # you will probably want to change this...
        return [-1, -1]
    return [totalValue, totalWeight]  # returns a list of both total value and total weight


# here is a simple function to create a neighborhood
# 1-flip neighborhood of solution x
def neighborhood(x):
    nbrhood = []

    for i in range(0, n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    return nbrhood


# 2-flip neighborhood of solution x
def neighborhood2(x):
    nbrhood = []
    temp_nhbr = []
    for i, j in itr.combinations(range(0, 100), 2):
        temp_nhbr = x[:]
        temp_nhbr[i] = 1
        temp_nhbr[j] = 1
        nbrhood.append(temp_nhbr)
    return nbrhood


def neighborhood3(x):
    nbrhood = list()
    for i, j, k in itr.combinations(range(0, 100), 3):
        tempx = x[:]
        tempx[i] = 1 if tempx[i] == 0 else 0
        tempx[j] = 1 if tempx[j] == 0 else 0
        tempx[k] = 1 if tempx[k] == 0 else 0
        nbrhood.append(tempx)
    return nbrhood


def localSearch(location):
    solutionsChecked = 0
    x_best = location[:]
    f_curr = evaluate(location)
    f_best = f_curr[:]

    loop = False
    while loop == False:
        Neighborhood = neighborhood(location)
        for s in Neighborhood:  # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # and store its evaluation
        if f_best == f_curr:
            loop = True
        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]
    return x_best


# create the initial solution
def initial_solution():
    x = [0] * 100  # i recommend creating the solution as a list
    return x


# varaible to record the number of solutions evaluated
x_curr = initial_solution()  # x_curr will hold the current solution
x_best = x_curr[:]  # x_best will hold the best solution
f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]

# begin local search overall logic ----------------
done = 0
finish = 0

while finish == 0:
    K = 1
    while K < 4:
        if K == 1:
            Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

        elif K == 2:
            Neighborhood = neighborhood2(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

        elif K == 3:
            Neighborhood = neighborhood3(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

        s = myPRNG.choice(Neighborhood)
        S = localSearch(s)
        solutionsChecked = solutionsChecked + 1
        if evaluate(S)[0] > f_best[0]:
            x_best = S[:]  # find the best member and keep track of that solution
            f_best = evaluate(S)[:]  # and store its evaluation
            K = 1

        else:
            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evalute the current solution
            K = K + 1

            if solutionsChecked >= 2000:  # if there were no improving solutions in the neighborhood
                finish = 1
                K = 5
        print("\nTotal number of solutions checked: ", solutionsChecked)
        print("Best value found so far: ", f_best)

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print("Weight is: ", f_best[1])
print("Total number of items selected: ", np.sum(x_best))
print("Best solution: ", x_best)