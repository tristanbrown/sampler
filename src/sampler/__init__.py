"""Sampler package."""
import os

from .constraints import Constraint
from .gibbs import Gibbs

example_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../tests/examples"))
