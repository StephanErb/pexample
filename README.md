# pExample: Python with Pants and PEX

This repository features a running example of the [pants](https://www.pantsbuild.org/) build system
and Python packaging with [PEX](https://pex.readthedocs.io/).

[![Build Status](https://travis-ci.org/StephanErb/pexample.svg?branch=master)](https://travis-ci.org/StephanErb/pexample)


## What is Pants?

Pants is a build system for large or rapidly growing code bases. It supports all stages of a typical
build: tool bootstrapping, code generation, third-party dependency resolution, compilation, test
running, linting, bundling and more.

Pants supports Java, Scala, Python, C/C++, Go, Thrift, Protobuf and Android code. Support for other
languages, frameworks, and code generators can be added by authoring plugins through a well defined
module interface.

With pants, you can organize your code via targets for binaries, libraries, and tests. For Python
programmers, pants is especially interesting, as it makes the manipulation and distribution
of hermetically sealed Python environments painless. For example, pants handles dependencies for
you. It never installs anything globally. Instead, it builds the dependencies, caches them, and
assembles them a la carte into execution environments - so called PEXes.


## What is PEX?

A PEX is, roughly, an archive file containing a runnable Python environment. The ideas is based on
[PEP 441](https://www.python.org/dev/peps/pep-0441/). Pants isn't the only PEX-generation tool out
there; but if you have some "common code" used by more than one PEX, Pants makes it easy to manage
everything.


## Getting Started

In this example, everything is controlled via the `./pants` script that will automatically
bootstrap pants and its dependencies.

    # bootstrap
    $ ./pants

Let's start with something simple:

    # List everything pants can do for us
    $ ./pants goals

    # List all registered source roots
    $ ./pants roots

According to the command above, we have tests defined. Let's run them (using the recursive wildcard `::`):

    $ ./pants test tests/python::

The example also comes with a (highly sophisticated) command line client:

    $ ./pants -q run src/python/hello_world/cli:hello_world
    Hello World!

We can also build a self-contained PEX binary with our code, so that it can be used independent of
pants and the build environment:

    $ ./pants binary src/python/hello_world/cli:hello_world

The binary is dropped into `dist/`. Let's run it:

    $ ./dist/hello_world.pex
    Hello World!

    $ ./dist/hello_world.pex --name Stephan
    Hello Stephan!

Mhh, let's make that a bit more exciting:

    $ ./dist/hello_world.pex --name Stephan --mode cow

    ________________
    < Hello Stephan! >
    ----------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/
                   ||----w |
                   ||     ||

Better :)


## Running Tests

As a build system pants is also responsible for running tests:

    # Run all tests (using the recursive wildcard ::)
    $ ./pants test tests::

    # Run one specific test target
    $ ./pants test tests/python/hello_world/messages

Under the hood pants is using `pytest`. We can pass arbitrary arguments to pytest (i.e.,
anything after `--`). For example, we can use `-k` to limit the test execution to tests
containing a particular name:

    # Run tests whose name contains "cow"
    ./pants test tests/python/hello_world/messages -- -k cow

Pants can also leverage SCM information to restrict operations to a set of changed targets and
thus improve turnaround times:

    # NOTE: To follow the commands below you might want to change the content
    #       of `src/python/hello_world/messages/greetings.py`

    # List all changed targets with uncommitted changes
    $ ./pants --changed-parent=HEAD list

    # Run tests for all targets listed above and their direct dependencies
    $ ./pants --changed-parent=HEAD --changed-include-dependees=direct test

    # Run tests for all targets directly or transitively depending on the changed targets
    $ ./pants --changed-parent=HEAD --changed-include-dependees=transitive test

On build servers such as Jenkins it can also be useful to run tests for anything
that changed between branches or since a particular commit:

    # Run tests for anything changed on this branch (compared to master)
    $ ./pants --changed-include-dependees=direct --changed-parent=master test

    # Run tests for anything changed since a commit SHA
    $ ./pants --changed-include-dependees=direct --changed-changes-since=101e8b2562 test


## Python Code Quality Tools

Pants ships with a plugin for `isort` to ensure imports are properly grouped and sorted:

    # check sort order of everything in src/python
    ./pants fmt.isort src/python:: -- --diff --check-only

    # correct sort order for all python files
    ./pants fmt.isort {src,tests}/python::

Pants can also be used to run `pep8`, `pyflakes`, and a few additional quality checks:

    # run stylechecks for all python files
    ./pants lint {src,tests}/python::


## Interactive Python Sessions

It can sometimes be helpful to investigate a build environment within an interactive Python REPL.
Within such a session it is then possible to import a target's code and its dependencies:

    $ ./pants repl src/python/hello_world/messages
    >>> from hello_world.messages.animals import cow
    >>> print cow('Hello Betty')

It is also possible to drop into an interactive session for a PEX binary:

    $ PEX_INTERPRETER=1 ./dist/hello_world.pex
    >>> from hello_world.messages.animals import unicorn
    >>> print unicorn('wow unicorn')


        \
         \
          \\
           \\
             >\/7
        _.-(6'  \
       (=___._/` \
            )  \ |
           /   / |       ________________
          /    > /       < WOW unicorn >
         j    < _\       ----------------
     _.-' :      ``.
     \ r=._\        `.
    <`\\_  \         .`-.
     \ r-7  `-. ._  ' .  `\
      \`,      `-.`7  7)   )
       \/         \|  \'  / `-._
                  ||    .'
                  \\  (
                   >\  >
                ,.-' >.'
               <.'_.''
                 <'


## Under the hood: BUILD Files

A large, well-organized codebase divides into many small components. These components, and the code
dependencies between them, form a directed graph. This graph is then used for various operations,
such as compilation and fine-grained invalidation.

Components in pants are defined using `BUILD` files containing directives (so called targets) such
as:

    python_library(
      name='mytarget',
      sources=globs('*.py'),
      dependencies=[
        '3rdparty/python:click',
        'src/python/hello_world/foo',
        'src/python/hello_world/bar',
      ]
    )

Many programming languages (E.g., Java, Python, Go) have a concept of a package, usually
corresponding to a single filesystem directory. It turns out that this is often the appropriate
level of granularity for targets. It's by no means required, but has proven in practice to be a good
rule of thumb.

To list all build targets in a repository:

    /pants list ::


## References

Most of the content above is directly extracted from the [pants](https://www.pantsbuild.org/) and
[PEX](https://pex.readthedocs.io/) documentation.

Further reading:

* https://www.pantsbuild.org/first_concepts.html
* https://www.pantsbuild.org/python_readme.html
* https://www.pantsbuild.org/3rdparty_py.html
* https://www.pantsbuild.org/build_dictionary.html

Helpful talks:

* [The Pants Build Tool at Twitter](https://www.youtube.com/watch?v=j_4CVpOIWsE)
* [WTF is PEX](https://www.youtube.com/watch?v=NmpnGhRwsu0)
