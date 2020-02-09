=======
Sampler
=======
A sampler for constrained vector space.

Install
=======

    pip install -r requirements_dev.txt

Usage
=====

    sampler <input_file> <output_file> <n_results>

Tests
=====

    pytest -sv

Description
===========
Generates the requested number of sample vectors, according to the constraints
described in the input file, and prints them to an output file. The samples are 
uniformly distributed, within the constrained vector space of the
unit hypercube. 

Each sample is generated using a Gibbs sampling method. Given the ith sample in
a vector of dimension k, X_i, the (i+1)th sample X_(i+1) is generated as such,
from X_i:

1. The jth vector component x_i,j is randomly selected, and set to the variable t. 
2. All vector components are plugged into the constraint inequalities, which are
   solved for t (using sympy).
3. The boundaries of the resulting domain for t are used as an interval for uniform
   random sampling, using numpy. 
4. The resulting sampled value for t is set in the vector as x_(i+1),j.
5. The resulting vector is used as the input for step 1, recursing until all
   x_i values have been converted to x_(i+1) values, giving X_(i+1). 

Discussion
==========
This sampler returns a correct set of vectors, spread uniformly throughout the
constrained vector space. However, it suffers from a performance deficit. The
reason for this is that sympy cannot solve multivariate systems of inequalities.
This means that sympy can only be used for symbolic manipulation after the constraints
have been appropriately substituted to create a univariate system of inequalities.
Hence, sympy solves the constraint inequalities k*n times, taking excessive
time, especially for high-dimensional vectors. 

If an alternate means of symbolic manipulation could be found that could handle
multivariate systems of inequalities, then the symbolic manipulation could happen
just once for each dimension, and the k*n sampling steps would only require substituting
values, making them much faster. 
