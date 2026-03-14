"""
This file contains helper and testing functions for use in main script file.
"""

from time import perf_counter

from definitions import Action, Findings, Node, SearchFunc, Solution, Yard
from yards import ALL_YARDS


def backtrack(node: Node) -> list[Action]:
    """
    Consumes a search tree `node`.

    Produces a list of actions that correspond to each step tracing back up
    the search tree from the given `node` to the root node.
    """

    # Initialize the list of actions
    actions: list[Action] = []

    # Traverse up the tree to the root node starting from the given node, this
    # loop will exit upon reaching the root node (which has no action or parent)
    while node.action and node.parent:

        # Append the current node's action to the action list
        actions.append(node.action)

        # Move up the tree by reassigning the node to its parent
        node = node.parent

    # Reverse the list's order to match going from initial state to goal state
    actions.reverse()

    # Return the resulting list of actions
    return actions


def test_yard(search_func: SearchFunc, yard: Yard, informed: bool) -> None:
    """
    Test the given `yard` using the given function `search_func` and pass on
    whether it should be informed or not with `informed`. The runtime,
    expanded node count, and action list will be printed out after.
    """

    # Ensure the yard's initial and goal states have the same number of tracks
    assert len(yard.state_init) == len(yard.state_goal)

    # Mark the runtime's start
    time_start: float = perf_counter()

    # Call the given search function and store its solution
    solution: Solution = search_func(yard, informed)

    # Mark the runtime's stop
    time_stop: float = perf_counter()

    # Print out the solution's testing information
    print(Findings(solution, time_stop - time_start, search_func))


def test_search_func(search_func: SearchFunc, informed: bool) -> None:
    """
    Test each predefined yard using the given function `search_func`
    and pass on whether it should be informed or not with `informed`.
    """

    # Substring showing whether the function is informed or not
    is_informed = "informed" if informed else "uninformed"

    # Print the function's name and the informed substring
    print(f"\nRunning tests for {search_func.__name__} ({is_informed})\n")

    # Test the function on each (allowable) predefined yard
    for yard in ALL_YARDS:
        test_yard(search_func, yard, informed)
