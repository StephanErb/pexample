from __future__ import print_function

import click
from hello_world.messages.greeting import greet


@click.command()
@click.option('--name', default='World', help='The person to greet.')
@click.option('--mode', default='plain', type=click.Choice(['plain', 'cow', 'unicorn']))
def main(name, mode):
    print(greet(name, mode))
