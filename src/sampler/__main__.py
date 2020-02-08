"""Main module for running the sampler."""
import argparse
import csv
from sampler import Constraint, Gibbs

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str, help="Input filepath.")
parser.add_argument('output_file', type=str, help="Output filepath.")
parser.add_argument('n_results', type=int, help="Number of samples.")
args = parser.parse_args()

def run():
    """Main method to run the app."""
    constr = Constraint(args.input_file)
    gibbs = Gibbs(constr)
    samples = gibbs.sample(int(args.n_results))
    result = [' '.join([str(i) for i in vector]) for vector in samples]
    result = '\n'.join(result)
    with open(args.output_file, 'w') as f:
        f.write(result)

if __name__ == "__main__":
    run()
