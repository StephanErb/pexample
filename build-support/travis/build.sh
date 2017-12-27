#!/usr/bin/env bash

set -eux
date


# Check import order
./pants fmt.isort :: -- --diff --check-only

# Check style
./pants lint ::

# Run tests
./pants test.pytest :: -- -v

# Check binaries can be build
./pants binary ::

