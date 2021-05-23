python_library()

# Define a self-contained, relocatable binary that contains a complete Python environment
# (i.e., code and dependencies but not the interpreter itself). See https://pex.readthedocs.io

# By specifying a custom `platforms` list, we build this binary for Mac and Linux so it can be used
# anywhere.

pex_binary(
  name='math_fun',
  entry_point='math_fun.cli.main:main',
  platforms=[
    'current',
    'macosx-10.9-x86_64-cp-38-cp38',
  ]
)

