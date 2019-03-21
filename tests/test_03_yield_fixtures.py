# "yield" fixtures let you take action in a fixture both before and after a
# test. The pytest docs cover these really well, but they're cool enough to
# warrant a specific callout.
# https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
import pytest

finally_ran = False
# While using the documented yield/addfinalizer mechanisms works, and using the
# existing interfaces in pytest is preferred, this is another thing you can do
# with yield fixtures that might not be immediately obvious.
@pytest.fixture
def yield_finally():
    global finally_ran
    try:
        # do pre-test fixture stuff here, and yield the result
        yield 'foo'
        # Also there's a bomb in here. This will actually cause weird test
        # reporting, since the test failure happens *after* the test runs.
        raise RuntimeError("Don't do this...")
    finally:
        # But regardless of what happens in the test, the finally clause
        # always runs
        finally_ran = True


@pytest.mark.xfail(reason='I used a fixture with a bomb in it...')
def test_yield_finally(yield_finally):
    assert yield_finally == 'foo'


def test_finally_ran():
    assert finally_ran


# I was asked what happens if you yield more than once, and I actually have no
# idea. Let's see!
@pytest.fixture
def yield_twice():
    yield 'oh'
    yield 'no'


@pytest.mark.xfail(reason='Yeah, pytest totally hates this.')
def test_yield_twice(yield_twice):
    pass
