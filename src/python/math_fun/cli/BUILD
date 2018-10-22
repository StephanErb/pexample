# Define a self-contained, relocatable binary that contains a complete Python environment
# (i.e., code and dependencies but not the interpreter itself). See https://pex.readthedocs.io

python_library(
  name='_cli',
  dependencies=[
    '3rdparty/python:click',
    'src/python/math_fun/lib'
  ],
  compatibility=['CPython>=2.7,<3', 'CPython>=3.4']
)


# By specifying a custom `platforms` list, we build this binary for Mac and Linux so it can be used
# anywhere.

python_binary(
  name='math_fun',
  entry_point='math_fun.cli.main:main',
  dependencies=[
    ':_cli',
  ],
  platforms=[
    'current',
    'linux-x86_64',
    'macosx-10.6-x86_64',
  ]
)

# We also build a custom Python 2 version of the binary. To make this work we need to overwrite
# the intepreter `compatibility` argument on the binary and all libraries that the binary depends
# on. `compatibility defaults to the interpreter constraint defined in the toplevel `pants.ini`.

python_binary(
  name='math_fun_py2',
  entry_point='math_fun.cli.main:main',
  dependencies=[
    ':_cli',
  ],
  platforms=[
    'current',
    'linux-x86_64',
    'macosx-10.6-x86_64',
  ],
  compatibility=['CPython>=2.7,<3'],
  tags=['legacy_python']
)
