"""
This file contains all the type definitions and
aliases for the custom objects in the main script file.
"""

from dataclasses import dataclass
from typing import Callable, Iterable, Literal, NamedTuple, Self

# Toggle to show the list of actions to the goal state
SHOW_ACTIONS = True

# Type alias for an individual train car (*, a, b, c, d, e)
type Car = Literal["*", "a", "b", "c", "d", "e"]

# Type alias for a railyard track identifier [1,6]
type Track = Literal[1, 2, 3, 4, 5, 6]

# Type alias for a connectivity list of a railyard layout
type TrackLayout = dict[Track, list[Track]]


class Train(tuple[Car, ...]):
    """Tuple of a group of train cars on a single track (can be empty)."""

    # Static method that creates a new Train instance
    def __new__(cls, cars: Iterable[Car]) -> Self:
        return super().__new__(cls, tuple(cars))


class State(tuple[Train, ...]):
    """
    Tuple of a railyard's state, where each element is
    the `Train` on the track number at the matching index.
    """

    # Static method that creates a new State instance
    def __new__(cls, trains: Iterable[Iterable[Car]]) -> Self:
        return super().__new__(cls, tuple(Train(t) for t in trains))

    # Return a mutable instance of the State
    def mutate(self) -> list[list[Car]]:
        return [list(t) for t in self]


class Action(NamedTuple):
    """Tuple of a movement action as described by the assignment."""

    direction: Literal["LEFT", "RIGHT"]  # Direction of movement
    track_from: Track  # The track that the moving car is coming from
    track_to: Track  # The track that the moving car is going to

    # Static method to show the action as a string
    def __str__(self) -> str:
        return f"({self.direction:<5} {self.track_from} {self.track_to})"


class ResultPair(NamedTuple):
    """Tuple of a `State`-`Action` pair (used by the `expand` function)"""

    state: State  #
    action: Action


@dataclass
class Node:
    """Dataclass of a search tree node."""

    state: State  # Node's associated State
    action: Action | None  # Node's associated Action (None if root)
    parent: Node | None  # Node's parent Node (None if root)
    cost_actual: int = 0  # Node's actual path cost (g)
    cost_estimated: int = 0  # Node's heuristic estimate path cost (h)

    # Method that returns the node's priority in the heap
    def priority(self) -> int:
        return self.cost_actual + self.cost_estimated

    # Method that returns the node as a HeapEntry instance
    def as_heap_entry(self, tiebreaker: int) -> HeapEntry:
        return HeapEntry(self.priority(), tiebreaker, self)


class HeapEntry(NamedTuple):
    """Tuple of an element in the fringe heap (used with heuristics)."""

    priority: int  # Entry's priority in the heap
    tiebreaker: int  # Entry's identifier used for tiebreakers
    node: Node  # Entry's associated Node


class Yard(NamedTuple):
    """Tuple of a predetermined yard as given by the assignment."""

    number: int  # Railyard's number (1, 2, 3, 4, 5)
    track_layout: TrackLayout  # Layout of the railyard's tracks
    state_init: State  # Initial state of the railyard
    state_goal: State  # Goal state of the railyard


class Solution(NamedTuple):
    """Tuple of a solution to a given yard."""

    yard: Yard  # Solution's associated Yard
    node_count: int  # Solution's expanded node count
    actions: list[Action]  # List of actions to reach yard's goal state


class Findings(NamedTuple):
    """Tuple of a solution's findings (for testing purposes)."""

    solution: Solution  # The solution being tested
    runtime: float  # The elapsed runtime to find the solution
    search_func: SearchFunc  # The search function used to find the solution

    # Static method to show the findings as a string for testing
    def __str__(self) -> str:

        # Show the current yard's number
        test_results: str = f"Yard {self.solution.yard.number}: "

        # Skip if search function cannot process the yard
        if not self.solution.node_count:
            return test_results + "Skipping due to memory limits"

        # Show the runtime and expanded node count
        test_results += f"{(self.runtime):0>9,.6f}s | "
        test_results += f"Node count: {self.solution.node_count:,}".ljust(20)

        # Check if no solution was found, as indicated by an empty action list
        if not self.solution.actions:
            test_results += " | No solution."

        # Don't show the action list if using SA, the list can be VERY long
        elif self.search_func.__name__ == "simulated_annealing_search":
            test_results += f" | Action count: {len(self.solution.actions):,}"

        # Show list of actions to get to goal state (toggled by SHOW_ACTIONS)
        elif SHOW_ACTIONS:
            for action in self.solution.actions:
                test_results += f"\n\t{action}"

        # Return the resulting string
        return test_results


# Type alias for a callable search function
type SearchFunc = Callable[[Yard, bool], Solution]
