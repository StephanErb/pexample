# Define a library containing everything within this folder/package
# (by default) that other targets can depend on.

# The setup_py addition below adds additional information to enable
# the generation of source distributions, e.g. for uploads to PyPi.

python_library(
  dependencies=[
    '3rdparty/python:numpy',
  ],
  compatibility=['CPython>=2.7,<3', 'CPython>=3.4'],
  provides=setup_py(
    name='math_fun',
    version='0.0.24', # can also be dynamic. BUILD files are just Python
    description='Math lib as a source distribution',
    zip_safe=True,
    classifiers=[
      'Intended Audience :: Developers',
      'Programming Language :: Python',
    ]
  )
)
