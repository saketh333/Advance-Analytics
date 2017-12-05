# Student name: Sai srikanth Kola and Saketh
# Date:04/16/2017
from random import Random  # need this for the random number generation -- do not change
import numpy as np
import math
#-------------------------------------------------------
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
        return [-1, -1]  # print ("Oh no! The solution is infeasible!  What to do?  What to do?")   #you will probably want to change this...

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


def UpdatedTemp(maximumtemp, n):
    maximumtemp = maximumtemp / (1 + n)    #cauchy cooling schedule
    return [maximumtemp, n*10]
#def UpdatedTemp(maximumtemp, n):
 #   maximumtemp *= 0.8  # geometric cooling schedule
  #  return [maximumtemp, n * 3]

# create the initial solution
x_curr = []


def initial_solution():
    for i in range(0, n):
        if myPRNG.random() < 0.99:
            x_curr.append(0)
        else:
            x_curr.append(1)
    return x_curr


# varaible to record the number of solutions evaluated
solutionsChecked = 0
x_best = initial_solution()
f_best = f_curr = evaluate(x_curr)[0]
# f_best = f_curr

weigh = []
maximumtemp = 3800  # initial temperature

maxIterations = 300  # iterations

for k in range(1, maxIterations):
    solutionsChecked += 1
    temp, l = UpdatedTemp(maximumtemp, k)  # get a current temperature

    iter = 0  # count iterations
    while iter < l:  # iterate until max iteration
        s = myPRNG.choice(neighborhood(x_curr))  # selection criteria  values from the neighborhood

        if evaluate(s)[0] > f_best:  # if an improvement was found
            x_curr = x_best = s[:]  # set the curreent and best solution
            f_curr = f_best = evaluate(s)[0]  # set the current and best value
            weigh = evaluate(s)
        else:
            delta = evaluate(x_curr)[0] - evaluate(s)[0]  # difference in objective values
            sye = myPRNG.random()  # set theta to a random number

            if sye < math.exp(-1 * delta / temp):  # if theta is less than the prob function
                x_curr = s[:]  # make the move--this is completely random
                f_curr = evaluate(s)[0]  # make the value move

        iter = iter + 1

print("number of solutions checked: ", solutionsChecked)
print("Final Temperature", temp)
print("Best value found", f_best)
print("Best weight and Value", weigh)
print("Item selected", np.sum(x_best))