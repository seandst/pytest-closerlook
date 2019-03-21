# pytest_generate_tests. Buckle up! :D
# https://docs.pytest.org/en/latest/parametrize.html#basic-pytest-generate-tests-example
# You can do some absolutely crazy things inside a pytest_generate_tests
# function. I'll just preface this by saying that test function and fixture
# parametrization is generally the better choice because it's far (FAR) more
# readable, but in cases where the parametrization is particularly complex, you
# may find yourself here. This example builds from the previous example, which
# stacked parametrized fixtures to make a test matrix.


def pytest_generate_tests(metafunc):
    # p_g_t can be defined a few ways, it just has to end up being a callable
    # that takes the metafunc argument. So you can 'def' it, as seen here, or
    # create a library of callables that can be used during testing that
    # centralize common test generation behaviors.
    #
    # Note that there can only be one instance of p_g_t in a test module, so
    # if you need to parametrize different tests in different ways, I recommend
    # separating them into their own modules.

    # metafunc.parametrize takes a few args, but for this case we'll focus on
    # the two positional args, 'argnames', and 'argvalues', plus the 'idlist'
    # kwarg:
    # - 'argnames' is the list of argument names to parametrize.
    # - 'argvalues' is a list of values to assign to those names.
    # - 'idlist' is an optional list of test "ID" strings, which are used in
    #   py.test output to identify the parametrized instance of the test being
    #   run
    # Together, they end up making a matrix of tests:
    #
    #    Test Name           argnames[0]     argnames[1]     argnames[n]...
    #    ---------           -----------     -----------     -------------
    # test_name[idlist[0]]   argvalues[0][0] argvalues[0][1] argvalues[0][n]
    # test_name[idlist[1]]   argvalues[1][0] argvalues[1][1] argvalues[1][n]
    # test_name[idlist[v]]   argvalues[v][0] argvalues[v][1] argvalues[v][n]
    #  ...
    #
    # So, if we wanted to recreate the example above, which uses three fixtures
    # to run tests on three axes of parametrization, we can iterate over the
    # combinations, and build up the parametization matrix that way:
    from itertools import product
    axis_1 = ['a', 'b', 'c']
    axis_2 = ['1', '2', '3']
    axis_3 = [True, False, None]

    # These are the function arguments that will appear to tests as fixtures.
    argnames = ['pgt_axis_1', 'pgt_axis_2', 'pgt_axis_3']

    # This is the list of values that will be assigned to those names. The
    # number of values in each argvalues entry needs to match the number of
    # args in argnames, and will be built up in the following loop.
    argvalues = []
    idlist = []

    # This is the list of IDs, and needs to be the same length as argvalues.
    # It's easiest to build argvalues and idlist together.
    for a1, a2, a3 in product(axis_1, axis_2, axis_3):
        test_values = [a1, a2, a3]
        # If you needed to, you could do conditional tests in here to prevent
        # tests being run with certain parameter combinations. For example,
        # let's say that we know tests won't work when axis 1 is 'c', and axis
        # 3 is None:
        if a1 == 'c' and a3 is None:
            # skip parametrization for this param combo
            continue
        # This should only be done where a given test combination can never
        # work, regardless of the test environment. In cases where the desire
        # is to skip tests based on the test environment (e.g. based on the
        # test platform, hardware available, etc.) tests should be skipped.
        # This method completely prevents collection of a test, and no skip
        # reporting will be done.

        argvalues.append(test_values)
        # default test id is effectively '-'.join(paramvalues), so use a
        # different character here so the effect of idlist is more clear in the
        # test output.
        idlist.append('|'.join(map(str, test_values)))

    # Now we parametrize all tests in this module with metafunc. If needed, we
    # could inspect the item under test via metafunc to only parametrize
    # specific tests, e.g.:
    # if set(argvalues).issubset(set(metafunc.fixturenames)):
    #    metafunc.parametrize(...)
    # See the Metafunc class def for more info:
    # https://docs.pytest.org/en/latest/reference.html#metafunc
    metafunc.parametrize(argnames, argvalues, ids=idlist)


# Any test parametrized by p_g_t needs to accept the argvalues defined in p_g_t
def test_generated_tests(pgt_axis_1, pgt_axis_2, pgt_axis_3):
    pass
