#/usr/bin/python3
import pytest
import irv

def test_algo1():
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

    winner = irv.instant_runoff(ballots, guys)
    print winner
    assert winner == "Alice"

def test_algo2():
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
        ["Alice", "Bob", "Dale", "Emily", "Carl"],
        ["Emily", "Bob", "Alice", "Dale", "Carl"]
    ]

    winner = irv.instant_runoff(ballots, guys)
    print winner
    assert winner == "Alice"

def test_algo3():
    """
    exercise of the instant runoff with hardcoded scrubbed values
    """
    guys = ["Alice", "Bob", "Carl", "Dale", "Emily"]
    ballots = [
        ["Alice", "Bob", "Carl", "Dale", "Emily"],
        ["Alice", "Dale", "Bob", "Carl", "Emily"],
        ["Emily", "Alice", "Carl", "Bob", "Dale"],
        ["Emily", "Dale", "Alice", "Bob", "Carl"],
        ["Dale", "Alice", "Carl", "Emily", "Bob"],
        ["Emily", "Bob", "Dale", "Alice", "Carl"],
        ["Emily", "Alice", "Bob", "Dale", "Carl"],
        ["Carl", "Bob", "Alice", "Dale", "Emily"]
    ]

    winner = irv.instant_runoff(ballots, guys)
    print winner
    assert winner == "Alice"
