#!/usr/bin/env bash

set -eux
date

# We have tagged a few targets as 'legacy_python'. They require Python 2 even though the rest
# of the repository is Python 2 only. We skip them here to keep the Travis setup simple.


# Check import order
./pants fmt.isort :: -- --diff --check-only

# Check style
./pants --tag=-legacy_python lint ::

# Run tests
./pants --tag=-legacy_python test.pytest :: -- -v

# Check binaries can be build
./pants --tag=-legacy_python binary ::

