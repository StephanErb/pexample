import click
from math_fun.lib import math
from math_fun.lib import version as platform_version


@click.command()
@click.option(
    "--version", default=False, is_flag=True, help="Print version and platform details."
)
@click.option(
    "--n",
    default=[10, 10],
    type=click.INT,
    multiple=True,
    help="Matrix shape to sum up",
)
def main(version, n):
    if version:
        print(platform_version.describe())
    else:
        print(math.random_sum(*n))
