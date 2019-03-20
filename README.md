# A closer look at py.test

This repository contains a closer look at some of pytest's concepts, including
fixture scopes, paramet(e)rization, and plugins. The concepts here are all
documented in the [py.test docs](https://docs.pytest.org/en/latest/), but
(as the name would imply) this serves to take a closer look at some of those
concepts.

## The environment

These tests were written on python 3.7, using py.test 4.3.1

## Running the tests

```
py.test
```

pytest.ini has been configured to run more verbosely than it does
by default, so that some of the examples can be seen working in
the test output. The examples themselves are heavily commented to
explain what's being done and why.

## Where's the stuff?

Follow the comments in the test modules, located in the
`tests` directory.

## Handy references

Details on most of pytest's interfaces:
* https://docs.pytest.org/en/latest/reference.html

Writing plugins and hooks:
* https://docs.pytest.org/en/latest/writing_plugins.html

Test collection and generation:
* https://docs.pytest.org/en/latest/example/parametrize.html
