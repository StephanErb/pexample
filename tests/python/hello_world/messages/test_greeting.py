from hello_world.messages.greeting import greet


def test_greeting_mentions_addressee():
    """Fancy formatting should not omit the person we're greeting."""
    for mode in ["plain", "cow", "unicorn"]:
        assert "foo" in greet("foo", mode)


def test_cow_ears():
    """The cow should have two ears."""
    assert "^__^" in greet("Betty", "cow")
