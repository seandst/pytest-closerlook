# pytest plugins
# A pytest plugin can be pretty much any module that gets loaded by pytest, and
# implements any of its hooks:
# https://docs.pytest.org/en/latest/writing_plugins.html

# In a way, every conftest.py in your project is a pytest plugin, and since
# conftest.py files are automatically loaded, they can be used to load and
# register a project's pytest plugins by name from there. To avoid confusion,
# though, pytest will issue warnings (and eventually no longer support) if
# pytest plugins are declared in any non-root conftest.py:
# https://docs.pytest.org/en/latest/writing_plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file

# If there is a desire to make a library of pytest plugins available, that can
# be done by using the pytest entry points to declare plugins.
# Multiple plugins can easily be made available in a single repository:
# https://docs.pytest.org/en/latest/writing_plugins.html#making-your-plugin-installable-by-others

# To declare plugins at runtime, you can specify the importable python
# reference to them in the root conftest.py:
# https://docs.pytest.org/en/latest/writing_plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file

# In this example, though, we'll assume (because it's generally true) that
# any generic task you'd normally want to do in a testing framework, such as
# mocking, coverage reporting, etc., is implemented in either pytest itself or
# a plugin that has already been written and is available on pypi.
# This example only highlights writing pytest plugin in-repo for
# project-specific testing behavior, and uses a plugin loaded from the root
# conftest.py


# The example plugin defines a fixture that marks tests running a specific
# fixture, and then sifts through the end-of-testing report to print out which
# tests were marked by the fixture.
def test_example_plugin(exampleplugin_markfixture):
    pass
