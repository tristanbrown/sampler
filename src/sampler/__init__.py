"""Sampler package."""
import os

from .constraints import Constraint

example_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../tests/examples"))
