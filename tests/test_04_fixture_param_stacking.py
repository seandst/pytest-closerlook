# A quick look at more advanced parametrization. Basic parametrization is
# covered in https://docs.pytest.org/en/latest/parametrize.html. This
# example will highlight the value of fixture parametrization.
# https://docs.pytest.org/en/latest/fixture.html#fixture-parametrize
import pytest


# while tests themselves can be parametrized easily enough, if you wanted to
# parametrize multiple tests with some test matrix, you'd want to bring in a
# parametrized fixture. "Basic" fixture parametrization can handle a single
# param:
@pytest.fixture(scope='session', params=['a', 'b', 'c'])
def axis_1(request):
    return request.param


# ...but you can also stack parametrized fixtures to create a multi-axis
# matrix:
@pytest.fixture(scope='module', params=['1', '2', '3'])
def axis_2(request, axis_1):
    # It's not necessary to combine the axes in this way; each fixture could
    # potentially just return its own param, and tests using these fixtures
    # could then use all 3 fixtures to be properly parametrized. However,
    # encapsulating this inside the fixture takes the burden of correctly
    # implementating fixture call order away from test writers.
    return axis_1, request.param


@pytest.fixture(scope='function', params=[True, False, None])
def axis_3(request, axis_2):
    return axis_2[0], axis_2[1], request.param


# The fixtures can also nest scopes, as demonstrated here, with each axis
# declared in increasingly narrow scope. Fixtures can be defined inside test
# files, like this one, but can of course be defined at any level in
# confest.py files or pytest plugins (a later topic).
def test_multi_axis(axis_1, axis_2, axis_3):
    pass


def test_multi_axis_single_fixture(axis_3):
    pass
