from colors import green
from hello_world.messages.animals import cow, unicorn


def greet(greetee, mode):
    greeting = green("Hello {}!".format(greetee))

    if mode == "cow":
        return cow(greeting)
    elif mode == "unicorn":
        return unicorn(greeting)
    else:
        assert mode == "plain"
        return greeting
