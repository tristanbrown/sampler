"""A Gibbs sampler."""
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import sympy as sp

class Gibbs():
    """Samples vectors uniformly from the space defined by the constraints."""
    def __init__(self, constraints):
        self.global_domain = sp.Interval(0, 1)  # Unit hypercube contains all solutions.
        self.constraint = constraints
        self.samples = []

    def sample(self, n_results, workers=8):
        """Samples n vectors."""
        start = time.time()
        if workers <= 1:
            self.samples = self._sample(n_results)
        else:
            n_per = -(-n_results // workers)
            with ProcessPoolExecutor(max_workers=workers) as executor:
                samples = executor.map(self._sample, workers * [n_per])
            self.samples = [sample for subset in samples for sample in subset][:n_results]
        end = int(time.time() - start)
        print(f"Generated {len(self.samples)} samples in {end} seconds.")

    def _sample(self, n_results):
        samples = [self.constraint.example]
        while len(samples) < n_results + 1:
            samples.append(self.sample_vector(samples[-1]))
        return samples[1:]

    def sample_vector(self, vector):
        """Sample each component of a vector, in random order."""
        vector = vector.copy()  # Don't modify the original vector.
        idxs = np.arange(len(vector))
        np.random.shuffle(idxs)
        for idx in idxs:
            vector[idx] = self.sample_comp(vector, idx)
        return vector

    def sample_comp(self, vector, idx):
        """Sample one component of the vector."""
        vector[idx] = 't'
        boundaries = self.get_domain(vector)
        if len(boundaries) == 2:
            return np.random.uniform(*boundaries)
        raise ValueError(f"Handling of this domain shape not yet implemented: {boundaries}")

    def get_domain(self, vector):
        """Combine the constraints into a single domain."""
        domain = self.global_domain
        for cond in self.constraint.exprs:
            new_constraint = self.solve_constraint(cond, vector)
            if new_constraint is not True:
                domain = sp.Intersection(domain, new_constraint)
        return list(domain.boundary)

    def solve_constraint(self, cond, vector):
        """Solve the constraint with a vector to give the resulting set."""
        x = sp.IndexedBase('x')
        expr = eval(cond)
        for i, j in enumerate(vector):
            expr = expr.subs(x[i], j)
        if expr == True:
            return True
        simplified = sp.solve(expr)
        return simplified.as_set()

    def verify(self):
        """Verify that all of the associated samples are valid."""
        valid = [self.constraint.apply(sample) for sample in self.samples]
        return all(valid)

    def samples_out(self, path):
        """Write the sampled vectors to an output file."""
        result = [' '.join([str(i) for i in vector]) for vector in self.samples]
        result = '\n'.join(result)
        with open(path, 'w') as f:
            f.write(result)

    def clear(self):
        """Clear all samples."""
        self.samples = []
