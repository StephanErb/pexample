# Define a library containing everything within this folder/package
# (by default) that other targets can depend on.
python_sources()

# The setup_py addition below adds additional information to enable
# the generation of source distributions, e.g. for uploads to PyPi.
python_distribution(
    name="wheel",
    dependencies=[":lib"],  # reference library above
    provides=python_artifact(
        name="math_fun",
        version="0.0.24",  # can also be dynamic. BUILD files are just Python
        description="Math lib as a source distribution",
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python",
        ],
    ),
    sdist=True,
    wheel=True,
)
