# widgets problem
reset;

# options

options solver cplex;

# decision variables

var w2 >=0; # W2 Supplier
var wrs >= 0; # WRS Supplier
var wu >= 0; # WU Supplier

var wow1 >=0; # WOW SUpplier
var wow2 >=0;
var wow3 >=0;

# Binary variables

var yWu binary; # For adding fixed cost to objective if we buy from WU
var z binary; # Will make sure we buy atleast 7500 from this supplier
var y1 binary; # WOW supplier restrictions
var y2 binary;

# Big M variable

param M = 123456789;

# Objective

var cost = 4.25*w2 + 3.15*wrs + 1.90*wu + yWu*15000 + 5.50*wow1 + 3.50*wow2 + 2*wow3;

minimize Objective: cost;

# Constraints

# Supply constraints of 4 manufactures
subject to manufacture1: w2 <= 10000;
subject to manufacture2: wrs <= 15000;
subject to manufacture3: wu <= 9000;
subject to manufacture4: wow1 + wow2 + wow3 <= 25000;

# Demand from the suppliers
subject to demand: w2 + wrs + wu + wow1 + wow2 + wow3 >= 32000;

# Binary constraints WRS
subject to binary_manufacture2: wrs<= 7499 + M*z;
subject to binary_manufacture22: wrs >= 7500 + M*(1-z);

# Binary constraints WU
subject to binary_manufacture3: wu + yWu >= 0;
subject to binary_manufacture32: wu <= M*yWu;

# Binary Constraints WOW
subject to binary_manufacture4: wow1 >= 5000*y1;
subject to binary_manufacture41: wow1 <= 5000;
subject to binary_manufacture42: wow2 <= 7500*y1;
subject to binary_manufacture421: wow2 >= 7500*y2;
subject to binary_manufacture43: wow3 <= 12500*y2;

# To solve the following code

solve;

# To display output
display cost;
display w2, wrs, wu, wow1, wow2, wow3, yWu, z, y1, y2;