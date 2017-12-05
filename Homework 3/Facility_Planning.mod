# Sets I: Districts and J: FireHouse
set I;
set J;

# Parameters for Distance, Population, Budget, Fixed cost, Variable cost 
param D{I, J} >=0;  # Distance b/w district <- i,site <- j
param P{I} >=0;  	# Population of district i
param B >= 0; 		# Allocated budget
param F{J} >=0; 	# Fixed cost for building/maintaining site J
param V{J} >=0; 	# Variable cost for building site J


# Binary Variables
var y{J}    binary; #its value is 1 if site j is selected or else 0
var x{I, J} binary; #its value is 1 if district i is assigned to site j or else 0
var z       binary; 

# Variables for Population, Maximum distance and Total cost
var s{J} integer;   # Population assigned to site j
var MaxD >= 0;      # Maximum distance among all the districts and the sites
var TC >= 0;        # Total cost

# Objective Function
minimize Distance_Between_I_J: MaxD;

# Constraints

# Assigning district to 1 firehouse
subject to only_one_site {i in I}: sum{j in J} x[i,j] = 1;
# making sure that a district is not assigned to unused site
subject to unused_site {j in J}: (sum{i in I} x[i,j]) <= y[j]*45;
# Either sites 1 and 2 / sites 3 and 4 are selected
subject to either_Site12 : y[1]+y[2] >= 2*z;
subject to either_Site34 : y[3]+y[4] >= 2*(1-z);
# Population at a particular district
subject to population {j in J}: s[j] = sum{i in I} x[i,j]*P[i];
# cost associated with building a fire house at a site
subject to TotalCost : sum{j in J} (F[j]*y[j]+V[j]*s[j]) = TC;
# making sure that we are within budget
subject to WithinBudget : sum{j in J} (F[j]*y[j]+V[j]*s[j]) <= B;
# Maximum distance
subject to Distance {i in I}: MaxD >= sum{j in J} D[i,j]*x[i,j];