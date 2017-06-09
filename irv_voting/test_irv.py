#/usr/bin/python3
import pytest

def test_algo():
    """
    exercise of the instant runoff with hardcoded scrubbed values
    """
    guys = ["Alice", "Bob", "Carl", "Dale", "Emily"]
    ballots = [
        ["Alice", "Bob", "Carl", "Dale", "Emily"],
        ["Alice", "Dale", "Bob", "Carl", "Emily"],
        ["Bob", "Emily", "Carl", "Alice", "Dale"],
        ["Dale", "Emily", "Bob", "Alice", "Carl"],
        ["Dale", "Alice", "Carl", "Emily", "Bob"],
        ["Bob", "Alice", "Dale", "Emily", "Carl"],
        ["Emily", "Bob", "Alice", "Dale", "Carl"]
    ]

    winner = instant_runoff(ballots, guys)
    print winner
    assert winner == "Alice"
