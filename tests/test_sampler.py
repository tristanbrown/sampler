"""Some basic tests for the Gibbs sampler."""
import os
import pytest

import sampler

def generate_example(filename):
    constr = sampler.Constraint(os.path.join(sampler.example_dir, filename))
    return sampler.Gibbs(constr)

@pytest.fixture(scope="class")
def ex_example():
    return generate_example('example.txt')

@pytest.fixture(scope="class")
def ex_alloy():
    return generate_example('alloy.txt')

@pytest.fixture(scope="class")
def ex_form():
    return generate_example('formulation.txt')

@pytest.fixture(scope="class")
def ex_mix():
    return generate_example('mixture.txt')

class TestGibbsSampler():

    def test_sampling(self, ex_example, ex_alloy, ex_form, ex_mix):
        ex_example.sample(40)
        ex_alloy.sample(7)
        ex_form.sample(15)
        ex_mix.sample(101)
        assert True

    def test_number(self, ex_example, ex_alloy, ex_form, ex_mix):
        assert len(ex_example.samples) == 40
        assert len(ex_alloy.samples) == 7
        assert len(ex_form.samples) == 15
        assert len(ex_mix.samples) == 101

    def test_valid(self, ex_example, ex_alloy, ex_form, ex_mix):
        assert ex_example.verify()
        assert ex_alloy.verify()
        assert ex_form.verify()
        assert ex_mix.verify()
