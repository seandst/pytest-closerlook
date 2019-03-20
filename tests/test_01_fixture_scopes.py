# demonstration of fixture scopes
# https://docs.pytest.org/en/latest/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session
import pytest

import types

# available fixture scopes are function, class, module, package or session.
# The package scope is currently experimental, so probably don't use it
# unless py.test stops marking it as experimental.

call_counts = types.SimpleNamespace(session=0, module=0, function=0)

# 'session' is the highest scope
# This fixture will be evaluated once per pytest session
@pytest.fixture(scope='session')
def s_scope():
    call_counts.session += 1


# 'module' is a narrower scope than 'session'
# This will only be run once per test module (this file)
@pytest.fixture(scope='module')
def m_scope():
    call_counts.module += 1


# 'function' is the narrowest scope, as well as the default scope
# This fixture will be run once per test function
@pytest.fixture(scope='function')
def f_scope():
    call_counts.function += 1


# This demonstrates that the call count for the f_scope fixture rises with
# each test call, but s_scope and m_scope call counts do not change.
# Parametrization will get a closer look later, but this example also shows us
# that parametrization considers each parametrized test its own test function,
# resulting in the f_scope fixture being re-evaluated for every parameter.
@pytest.mark.parametrize('call_count', range(1, 10))
def test_fixture_scopes(s_scope, m_scope, f_scope, call_count):
    assert call_counts.session == 1
    assert call_counts.module == 1
    assert call_counts.function == call_count


# ...and if we call another function with the three fixtures, we can see that
# the s_scope and m_scope call counts remain at 1, but the function-scoped
# fixture is incremented again.
def test_fixture_scopes_again(s_scope, m_scope, f_scope):
    assert call_counts.session == 1
    assert call_counts.module == 1
    assert call_counts.function == 10


# Function scope is the lowest scope, and higher-scoped fixtures are
# evaluated first. Lower-scoped fixtures can therefore depend on higher-scoped
# fixtures, but higher-scoped fixtures cannot depend on lower-scoped fixtures.

# This won't immediately fail, as the fixture must be used in a test before
# py.test evaluates its fixtures, resulting in a test error.
@pytest.fixture(scope='session')
def broken_scope(f_scope):
    pass


# More on xfail in the next topic...
@pytest.mark.xfail(reason='Test intentionally created with a broken fixture.')
def test_broken_scope(broken_scope):
    pass
