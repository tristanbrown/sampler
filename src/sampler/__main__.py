"""Main module for running the sampler."""
import argparse
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
    gibbs.sample(int(args.n_results))
    gibbs.samples_out(args.output_file)

if __name__ == "__main__":
    run()
