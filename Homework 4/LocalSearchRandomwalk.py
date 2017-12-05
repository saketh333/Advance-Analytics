# Student name: Sai srikanth Kola and Saketh
# Date:04/16/2017
from random import Random  # need this for the random number generation -- do not change
import numpy as np

seed = 5113
myPRNG = Random(seed)
# number of elements in a solution
n = 100
# create an "instance" for the knapsack problem
value = []
for k in range(0, n):
    value.append(myPRNG.uniform(10, 100))
weights = []
for j in range(0, n):
    weights.append(myPRNG.uniform(5, 20))

# define max weight for the knapsack
maxWeight = 5 * n

# monitor the number of solutions evaluated
solutionsChecked = 0


# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalvalue = np.dot(a, b)  # compute the value of the knapsack selection
    totalweight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalweight > maxWeight:

        return [-1, -1]
    else:
        return [totalvalue, totalweight]  # returns a list of both total value and total weight


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

initial = 0
def initial_solution():
    x = [0] * 100 # i recommend creating the solution as a list
    restart = 10         # variable to adjust

    if initial == 1:
        for i in range(0,restart):

            x[i] = 1
            myPRNG.shuffle(x)

    return x


x_curr = initial_solution()  # x_curr will hold the current solution
x_best = x_curr[:]  # x_best will hold the best solution
f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]
done = 0
location=0
rand_num = 0.75
solutions = []

while done == 0:
    solutions.append(f_best)
    Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr
    step= myPRNG.uniform(0,1) #probabilty = 0.5 to select 0 and probability = 0.5 to select 1
    if step < rand_num:
        for s in Neighborhood:  # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # and store its evaluation
    else:
        walk = 0
        while walk == 0:
            solutionsChecked = solutionsChecked + 1
            rand_index = myPRNG.randint(0,98)
            s = Neighborhood[rand_index]
            if evaluate(s)[0] >= 0:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # and store its evaluation
                walk = 1

    if f_best == f_curr:  # if there were no improving solutions in the neighborhood
            done = 1
    else:
        x_curr = x_best[:]  # else: move to the neighbor solution and continue
        f_curr = f_best[:]  # evaluate the current solution
print("the final location is ",location)
print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print("Weight is: ", f_best[1])
print("Total number of items selected: ", np.sum(x_best))
print("Best solution: ", x_best)
