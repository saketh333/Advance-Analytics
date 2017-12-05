
from random import Random
import random
from math import sin,sqrt
import math
import numpy as np
# to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)


n = 2 # number of elements in a solution
P = 200 # population size
# min and max values for each element of the solution
min_elements = -500
max_iteration = 500
max_Iterations = 900
max_itr_tostop = 20
localSearchOptima = 420.0
alpha = 0.3

# function to evaluate a solution x
def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i] * sin(sqrt(abs(x[i])))
    val = 418.9829 * d - val
    return val


# create an initial population of P particles
def initialize_population(P):
    population = []

    for i in range(0, P):
        # initialize blank list
        x = []
        # creating initial solution (particle position)
        for i in range(n):
            x.append(myPRNG.uniform(min_elements, max_iteration))

        population.append(x[:])  # adding the particle to the population

    return population


def evaluate_population(population):
    pop = []
    for i in range(0, len(population)):
        val = evaluate(population[i])
        pop.append((population[i],val))

    return pop


# This Function calculates the euclidean distance between the two points
def euclideanDistance(v1, v2):
    sum = 0.0
    i = 0
    count = 0
    for coord_1, coord_2 in (zip(v1, v2)):
        while count < len(coord_1):
            sum += ((coord_1[i] - coord_2[i])**2)
            i += 1
            count += 1
        break
    x = math.sqrt(sum)
    return x

# Function, which deletes the present two edges and reverses the sequence from the deleted edges
def stochasticTwoOpt(curr):
    current_result = curr[:]  # making a deep  and independent copy
    # selecting two random indices in the population
    index1, index2 = (random.randrange(0, len(current_result)), random.randrange(0, len(current_result)))
    to_delete = set([index1])
    if index1 == 0:
        to_delete.add(len(current_result) - 1)
    else:
        to_delete.add(index1 - 1)
    if index1 == len(current_result) - 1:
        to_delete.add(0)
    else:
        to_delete.add(index1 + 1)
    while index2 in to_delete:
        index2 = random.randint(0, len(current_result))
    # Ensuring always index1<index2
    if index2 < index1:
        index1, index2 = index2, index1
    # Reversing the line segment between index1 and index2
    current_result[index1:index2] = reversed(current_result[index1:index2])

    return current_result


def augmentedCost(current_result, penalties, lambdaa):
    distance, augmented = 0, 0
    size = len(current_result)
    for index in range(0, size):
        index1 = index
        if index == size - 1:
            index2 = 0
        else:
            index2 = index + 1

        if index2 < index1:
            index1, index2 = index2, index1
        v1 = current_result[index1]
        v2 = current_result[index2]
        d = euclideanDistance(v1, v2)
        distance += d
        augmented += d + (lambdaa * penalties[index1][index2])
    return distance, augmented


def cost(candidate, penalties, lambdaa):
    cost, augCost = augmentedCost(candidate , penalties, lambdaa)
    return cost, augCost

def calculate_Feature_Utilities(current_result, penalties):
    size = len(current_result)
    #Initializing the list to zeros
    utilities = [0] * size

    for index in range(0, size):
        index1 = index
        if index == size - 1:
            index2 = 0
        else:
            index2 = index + 1
        if index2 < index:
            index1, index2 = index2, index
        c1 = current_result[index1]
        c2 = current_result[index2]
        #Applying the utilities formulae
        utilities[index] = euclideanDistance(c1, c2) / (1 + penalties[index1][index2])

    return utilities


def update_Feature_Penalties(current_result, penalties, utilities):
    size = len(current_result)
    maxUtil = max(utilities)
    for index in range(0, size):
        index1 = index
        if index == size - 1:
            index2 = 0
        else:
            index2 = index + 1
        if index2 < index1:
            index1, index2 = index2, index1
        # Update penalties
        if utilities[index] == maxUtil:
            penalties[index1][index2] += 1
    return penalties


def local_Search(current, lambdaa, penalties, max_itr_tostop):
    count = 0
    while count < max_itr_tostop:
        current_cost, current_augcost = cost(current, penalties, lambdaa)
        candidate_Solution = []
        candidate_Solution = stochasticTwoOpt(current)
        candidate_cost,candidate_augcost = cost(candidate_Solution, penalties, lambdaa)

        #Checking for a larger augmented cost to escape the local minima
        if candidate_augcost < current_augcost:
            # resetting to restart the search
            current = candidate_Solution[:]
            count = 0
        else:
            count += 1
    return current


def GLS(points, max_Iterations, max_itr_tostop, lambdaa):
    # Create a random solution
    current = points[:]
    best = None
    # Initializing the penalties with zeros
    penalties = [[0] * len(points)] * len(points)
    #Stopping criteria
    while max_Iterations > 0:

        # Executing the local search
        current = local_Search(current, lambdaa, penalties, max_itr_tostop)

        # Calculating the feature utilities
        utilities = calculate_Feature_Utilities(current , penalties)

        # Updating the feature penalties
        penalties = update_Feature_Penalties(current , penalties, utilities)

        # Comparing the current candidate cost with the best and update accordingly
        current_cost, current_augcost = cost(current, penalties, lambdaa)
        if best == None :
            current_best, current_best = cost(current, penalties, lambdaa)
            if current_cost < current_best:
                best = current
            max_Iterations = max_Iterations - 1

    return best


pos = initialize_population(P)
eval_population = evaluate_population(pos)
lambdaa = alpha * (localSearchOptima / float(len(eval_population)))
result = GLS(eval_population, max_Iterations, max_itr_tostop, lambdaa)
print(result)


