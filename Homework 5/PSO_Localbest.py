# pso implementation
#particle swarm optimization for Schwefel minimization problem


#need some python libraries
import copy
import math
from random import Random
import time


#to setup a random number generator, we will specify a "seed" value
seed = 123
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)


##---------------------------edited-----------------


#number of dimensions of problem
n = 2

#number of particles in swarm
swarmSize = 1000
#swarmSize = 65

# no of iterations
noIter = 100
# inertia weight
#w = 0.9
wmax = 2
wmin = 0.9
#w = myPRNG.uniform(0,2.9)
# Acceleration constants
c1 = 0.5
c2 = 0.5

# r1 and r2 are generated randomly between (0,1)
r1 = myPRNG.random()
r2 = myPRNG.random()

# dimensions of the problem
lBnd = -500
uBnd = 500

# maximum/minimum velocity vector
vMax = 1
vmin = -1




#Schwefel function to evaluate a real-valued solution x    
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
               

# local best ring
def localbestring(pBest, i):
      # for the first element we are defining before element as the last element
      if i==0:
            prev = swarmSize -1
      # for the other elements before is set to previous element   
      else:
            prev = i -1
      # setting next element for the last element      
      if i == swarmSize - 1:
            next = 0
      # setting next element for other elements      
      else:
            next = i + 1
      # taking local best for the current neighborhood 
      if pBest[i:n] == max(pBest[prev:n], pBest[i:n], pBest[next:n]):
            pBestl = i
      if pBest[prev:n] == max(pBest[prev:n], pBest[i:n], pBest[next:n]):
            pBestl = prev
      if pBest[next:n] == max(pBest[prev:n], pBest[i:n], pBest[next:n]):
            pBestl = next

      return pBestl


def evaluate(x):          
      val = 0
      d = len(x)
      for i in range(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
                                        
      val = 418.9829*d - val         
                    
      return val  

# fuction for defining global best position
def GlobalBestposition(pos):
      gBest = pos[0]
      gBestVal = evaluate(gBest)
      
      # now we need to upadte this value
      for i in range(0, len(pos)):
          current = evaluate(pos[i])
          if current < gBestVal:
             gBestVal  = current
             gBest = pos[i][:]
      return gBest


# To make sure we dont go below our limits
def uP(pos, vel):
      for i in range(n):
            pos[i] = pos[i] + vel[i]
            if pos[i] > uBnd:
                  pos[i] = uBnd - 5*myPRNG.random()
            elif pos[i] < lBnd:
                  pos[i] = lBnd + 5*myPRNG.random()
      return pos

w = []
# v[i+1] = w*v[i] + r1*c1*(pBest - pCurrent) + r2*c2*(gBest - pCurrent)
def UpdatedvelocityVector(pos, pBest, gBest, vprev):
      UpdatedVelocity = []
      curiter = 1
      for i in range(0, len(pos)):
            w = wmax*(wmax - wmin)*(curiter/noIter)
            upVel = w*vprev[i] + c1*r1*(pBest[i] - pos[i]) + r2*c2*(gBest[i] - pos[i])
            if upVel > vMax:
                  upVel = vMax
            if upVel < vmin:
                  upVel = vmin
            UpdatedVelocity.append(upVel)
            curiter = curiter + 1
      return UpdatedVelocity

#the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in range(swarmSize)]      #position of particles -- will be a list of lists
vel = [[] for _ in range(swarmSize)]      #velocity of particles -- will be a list of lists

curValue = [] #value of current position  -- will be a list of real values
pbest = []    #particles' best historical position -- will be a list of lists
pbestVal = [] #value of pbest position  -- will be a list of real values


#initialize the swarm randomly
for i in range(swarmSize):
      for j in range(n):
            pos[i].append(myPRNG.uniform(-500,500))    #assign random value between -500 and 500
            vel[i].append(myPRNG.uniform(-1,1))        #assign random value between -1 and 1
            
      curValue.append(evaluate(pos[i]))   #evaluate the current position
                                                 
pBest = pos[:]  # initialize pbest to the starting position
pBestVal = curValue[:]  # initialize pbest to the starting position
stagnation = 10
done = 0
globalbestslist = []
iteration = 0

for j in range(0, noIter):
      #while done == 0:
      iteration += 1
      globalBest = GlobalBestposition(pos)
      for i in range(swarmSize):
            lbest = localbestring(pBest[i],i)
            vel[i] = UpdatedvelocityVector(pos[i], pBest[i], globalBest, vel[i])
            pos[i] = uP(pos[i], vel[i])
      # updating the particle best value
      for i in range(swarmSize):
            temp = evaluate(pos[i])
            if temp < pBestVal[i]:
                  pBest[i] = pos[i][:]
                  pBestVal[i] = temp

      print("For Current iteration of ", str(iteration) + "   " + "Objective Value: " + str(evaluate(globalBest)) )
      #print(" at the position: " + str(globalBest) )

      #if iteration == noIter:
      #done = 1
                  # #print(evaluate(globalBest))
                  # globalbestslist.append(evaluate(globalBest))
                  # if iteration > stagnation:
                  #       if globalbestslist[iteration - 1] == globalbestslist[iteration - stagnation - 1]:
                  #             done = 1
