# A very basic plugin, used to demonstrate creating plugins inside a test repo
# Extremely useful reference for hooks and items used in them:
# https://docs.pytest.org/en/latest/reference.html
import pytest

marked_tests = []


@pytest.fixture
def exampleplugin_markfixture(request):
    # the mark is applied here, and can be used by later hooks to take action
    # based on the mark. In our case, though, we'll just keep track of what the
    # mark was applied to as a string for use in the terminal reporter later.
    request.applymarker(pytest.mark.exampleplugin_mark)
    node_fullname = '{}/{}'.format(request.node.parent.name, request.node.name)
    marked_tests.append(node_fullname)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.write_sep('*', title='exampleplugin did this!')
    terminalreporter.write_line('The following tests used the '
                                'exampleplugin fixture:')
    terminalreporter.write_line(', '.join(marked_tests))
