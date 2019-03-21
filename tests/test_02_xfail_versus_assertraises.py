# xfail, or "expected failure", and a examples of how to use it (or not)
# https://docs.pytest.org/en/latest/skipping.html#xfail-mark-test-functions-as-expected-to-fail
# https://docs.pytest.org/en/latest/assert.html#assertions-about-expected-exceptions
import pytest

import datetime


def i_fail():
    raise RuntimeError('All I can do is fail...')


# The xfail mark can be used to test things that are known to fail.
# This can sometimes be useful, but xfail should generally not be used
# to test failing things, as you lose the ability to catch and examine
# the actual error causing the test failure.
@pytest.mark.xfail(reason='I tested a function known to fail.')
def test_expected_failure():
    i_fail()


# Rather than xfailing things like this, use the pytest.raises helper
def test_examine_raised_exception():
    with pytest.raises(RuntimeError) as excinfo:
        # note that the context value is an ExceptionInfo instance,
        # not the exception itself. That is stored at excinfo.value
        i_fail()
        assert str(excinfo.value) == 'All I can do is fail...'


# If you do find a case where certain preconditions may occasionally cause a
# test to fail, such as when running on an unsupported platform, xfail can be
# called conditionally:
def test_fails_on_thursday():
    # Monday is 0
    if datetime.date.today().weekday() == 3:
        pytest.xfail(reason='I do not pass on Thursday.')


# Of course, if a condition applies to multiple tests, an xfail fixture
# can be created to encapsulate this behavior:
@pytest.fixture
def wednesday_xfail():
    if datetime.date.today().weekday() == 2:
        pytest.xfail(reason='I do not pass on Wednesday.')


@pytest.fixture
def thursday_xfail():
    if datetime.date.today().weekday() == 3:
        pytest.xfail(reason='I do not pass on Thursday.')


# Expected to fail on thursday
def test_fixture_fails_on_thursday(wednesday_xfail, thursday_xfail):
    pass


# This single test is marked with usefixtures, but since marks can be applied
# module-wide with "pytestmark", and entire suite of tests with conditional
# success can be marked to conditionally xfail, if needed.
@pytest.mark.usefixtures('wednesday_xfail', 'thursday_xfail')
def test_marker_fails_on_thursday():
    pass


# That all said, if a test is known not to work under certain conditions, I
# recommend using pytest.mark.skip/pytest.skip instead, to more correctly
# represent the conditional case when a test is known to not work. The main
# point here being that 'xfail' is fun, but probably you should try
# 'pytest.raises' or 'pytest.[mark.]skip' first.
