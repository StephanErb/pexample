# pExample: Python with Pants and PEX

This repository features a running example of the [pants](https://www.pantsbuild.org/) build system
and Python packaging with [PEX](https://pex.readthedocs.io/).



## What is Pants?

Pants is a build system for large or rapidly growing code bases. It supports all stages of a typical
build: tool bootstrapping, code generation, third-party dependency resolution, compilation, test
running, linting, bundling and more.

The latest version of pants is currently focused on Python, with support for other languages coming
(back) soon.

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
    $ ./pants --version

Let's start with something simple:

    # List everything pants can do for us
    $ ./pants help goals

    # List all registered source roots
    $ ./pants roots

According to the command above, we have tests defined. Let's run them (using the recursive wildcard `::`):

    $ ./pants test tests/python::

The example also comes with a (highly sophisticated) command line client:

    $ ./pants run src/python/hello_world/cli:hello_world
    Hello World!

We can also build a self-contained PEX binary with our code, so that it can be used independent of
pants and the build environment:

    $ ./pants package src/python/hello_world/cli:hello_world

The binary is dropped into `dist/`. Let's run it:

    $ ./dist/src.python.hello_world.cli/hello_world.pex
    Hello World!

    $ ./dist/src.python.hello_world.cli/hello_world.pex --name Stephan
    Hello Stephan!

Mhh, let's make that a bit more exciting:

    $ ./dist/src.python.hello_world.cli/hello_world.pex --name Stephan --mode cow

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
    $ ./pants test ::

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
    $ ./pants --changed-since=HEAD list

    # Run tests for all targets listed above and their direct dependencies
    $ ./pants --changed-since=HEAD --changed-dependees=direct test

    # Run tests for all targets directly or transitively depending on the changed targets
    $ ./pants --changed-since=HEAD --changed-dependees=transitive test

On build servers such as Jenkins it can also be useful to run tests for anything
that changed between branches or since a particular commit:

    # Run tests for anything changed on this branch (compared to master)
    $ ./pants --changed-since=origin/master --changed-dependees=transitive test


## Python Code Quality Tools

Pants ships with a plugins such as `isort`, `black`, and `flake8` to ensure code is consistent:

    # Run quality checks on everything
    ./pants lint :: 

    # correct sort order and formatting for everything
    ./pants fmt ::

We can also run mypy to check (optional) Python types:

    # Run mypy on everything
    ./pants typecheck ::


## Interactive Python Sessions

It can sometimes be helpful to investigate a build environment within an interactive Python REPL.
Within such a session it is then possible to import a target's code and its dependencies:

    $ ./pants repl src/python/hello_world/messages
    >>> from hello_world.messages.animals import cow
    >>> print(cow('Hello Betty'))

It is also possible to drop into an interactive session for a PEX binary:

    $ PEX_INTERPRETER=1 ./dist/src.python.hello_world.cli/hello_world.pex
    >>> from hello_world.messages.animals import unicorn
    >>> print(unicorn('wow unicorn'))


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
such as compilation and fine-grained cache invalidation.

Components in pants are defined using `BUILD` files containing directives (so called targets) such
as:

    python_library(
      name='mytarget',
      dependencies=[
        '3rdparty/python:external_dep',
        'src/python/foobar/my_explicit_dependency',
      ]
    )

Fortunately for us, pants detects imported Python packages automatically, so we don't need to specify
those dependencies manually!

Many programming languages (E.g., Java, Python, Go) have a concept of a package, usually
corresponding to a single filesystem directory. It turns out that this is often the appropriate
level of granularity for targets. It's by no means required, but has proven in practice to be a good
rule of thumb.

To make it simpler to follow these best practices, pants can even auto-generate `BUILD` files:

    ./pants tailor

To list all build targets in a repository:

    ./pants list ::

### BUILD Example: Binaries
 
PEX files in Pants are declared via the `pex_binary` target type.  Commonly used optiones include the
binary name and the dependencies, but also the interpreter compatibility as well as the target platform.
This allows users to build binaries for different Python versions and operating systems:

    pex_binary(
      name='math_fun',
      entry_point='math_fun.cli.main:main',
      platforms=[
        'current',
        'macosx-10.9-x86_64-cp-38-cp38',
      ]
    )

### Build Example: Source Distributions

In addition to PEX files, Pants can also generate source distributions. Source distributions can be installed
via `pip` and uploaded to PyPi.org. All you need is a `python_distribution`:

    python_distribution(
      name='wheel',
      dependencies=[':lib'], # reference libraries to include
      provides=setup_py(
        name='math_fun',
        version='0.0.24', # can also be dynamic. BUILD files are just Python
        description='Math lib as a source distribution',
        classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python',
        ]   
      ),  
      setup_py_commands=["bdist_wheel", "sdist"]
    )

Pants can the be used to generate the source distribution. Similar to binaries, those will be placed in the `dist` folder:

    $ ./pants package src/python/math_fun/lib:wheel
    $ ls dist/math_fun-0.0.24.tar.gz
    

## References 

Most of the content above is directly extracted from the [pants](https://www.pantsbuild.org/) and
[PEX](https://pex.readthedocs.io/) documentation.

Further reading:

* https://www.pantsbuild.org/docs/how-does-pants-work
* https://www.pantsbuild.org/docs/concepts
* https://www.pantsbuild.org/docs/python
* https://github.com/pantsbuild/example-python

Helpful talks:

* [The Pants Build Tool at Twitter](https://www.youtube.com/watch?v=j_4CVpOIWsE)
* [WTF is PEX](https://www.youtube.com/watch?v=NmpnGhRwsu0)
