"""
This file contains all the functions defined in the assignment problems.
"""

from heapq import heappop, heappush
from math import exp
from random import choice, random

from definitions import (
    Action,
    HeapEntry,
    Node,
    ResultPair,
    Solution,
    State,
    TrackLayout,
    Yard,
)
from utilities import backtrack, test_search_func


def possible_actions(track_layout: TrackLayout, state: State) -> list[Action]:
    """
    FOR PROBLEM 1

    Consumes a yard connectivity list `track_layout` and a `state`.

    Produces a list of all possible actions in the given `track_layout`
    from the given `state`.
    """

    # Initialize the action list
    actions: list[Action] = []

    # Iterate through each track and their respective neighbors
    for track_x, track_x_neighbors in track_layout.items():
        for track_y in track_x_neighbors:

            # Prevent processing the same connections
            # as the connectivity list is bi-directional
            if track_x >= track_y:
                continue

            # Get the trains on both tracks (minus 1 accounting for 0th index)
            train_x = state[track_x - 1]
            train_y = state[track_y - 1]

            # Skip if the engine is in neither train
            if "*" not in train_x and "*" not in train_y:
                continue

            # Record LEFT move (FROM y TO x)
            if train_y:
                actions.append(Action("LEFT", track_y, track_x))

            # Record RIGHT move (FROM x TO y)
            if train_x:
                actions.append(Action("RIGHT", track_x, track_y))

    # Return the resulting list of possible actions
    return actions


def result(state: State, action: Action) -> ResultPair:
    """
    FOR PROBLEM 2

    Consumes a yard `state` and a movement `action`.

    Produces a corresponding state-action pair in a `ResultsPair` tuple that
    will result after carrying out the given `action` in the given `state`.
    """

    # Convert the input state to a mutable list
    state_mutable = state.mutate()

    # Handle LEFT move
    if action.direction == "LEFT":

        # Pop and store the leftmost car on the `from` track
        moving_car = state_mutable[action.track_from - 1].pop(0)

        # Assign the moving car to be the rightmost car on the `to` track
        state_mutable[action.track_to - 1].append(moving_car)

    # Handle RIGHT move
    elif action.direction == "RIGHT":

        # Pop and store the rightmost car on the `from` track
        moving_car = state_mutable[action.track_from - 1].pop()

        # Assign the moving car to be the leftmost car on the `to` track
        state_mutable[action.track_to - 1].insert(0, moving_car)

    # Return the state converted back to a tuple and the corresponding action
    return ResultPair(State(state_mutable), action)


def expand(state: State, track_layout: TrackLayout) -> list[ResultPair]:
    """
    FOR PROBLEM 3

    Consumes a yard `state` and a yard connectivity list `track_layout`.

    Produces a list of state-action pairs as `ResultPair` tuples that can be
    reached using all possible action from `state` on the `track_layout`.
    """

    # Get all possible actions that can be reached from the state
    actions: list[Action] = possible_actions(track_layout, state)

    # Create a list of state-action pairs for each possible action and return it
    return [result(state, a) for a in actions]


def blind_tree_search(yard: Yard, _: bool = False) -> Solution:
    """
    FOR PROBLEM 4

    Consumes a `yard` to solve. (unused bool to comply with unit test args)

    Produces a solution to the given `yard` using a breadth-first, blind
    (uninformed) tree search algorithm.
    """

    # Terminate if given YARD-1 or YARD-2 as it will overflow on memory
    if yard.number in [1, 2]:
        return Solution(yard, 0, [])

    # Initialize the expanded node count
    node_count: int = 0

    # Initialize the current node variable as the root node
    node: Node = Node(yard.state_init, None, None)

    # Initialize the fringe list with the root node inside
    fringe: list[Node] = [node]

    # Loop while the fringe has entries in it
    while fringe:

        # Pop the first element of the fringe and assign it as the current node
        node = fringe.pop(0)

        # Increment the expanded node count
        node_count += 1

        # Check if the current node's state matches the goal state
        if node.state == yard.state_goal:

            # Return a solution containing the yard, expanded node
            # count, and a list of actions tracing back to the root node
            return Solution(yard, node_count, backtrack(node))

        # Iterate through each state-action pair expanded
        # from the current node's state and the yard's layout
        for result in expand(node.state, yard.track_layout):

            # Create and append a new node to the fringe using the
            # result's state, action, and the current node as its parent
            fringe.append(Node(result.state, result.action, node))

    # This point in the function can only be reached if no solution was found,
    # which is indicated by the empty action list in this returned solution
    return Solution(yard, node_count, [])


def heuristic(state: State, state_goal: State) -> int:
    """
    FOR PROBLEM 6

    Consumes a yard `state` and a yard goal state `state_goal`.

    Produces an integer of the estimated cost (h) to reach `state_goal`.
    """

    # Initialize the total estimated cost (h)
    cost_estimated: int = 0

    # Iterate through each track of the given state of the yard
    for i in range(len(state)):

        # Get the trains from both the current track and the goal track
        train, train_goal = state[i], state_goal[i]

        # Iterate through each car in both trains
        for j in range(len(train)):

            # Skip this car if it's the engine
            if train[j] == "*":
                continue

            # Skip this car if both are true:
            # 1. The current train is at most the same length as the goal train
            # 2. Both trains have the same car at the current index
            if j < len(train_goal) and train[j] == train_goal[j]:
                continue

            # Increase the cost based on the position of this car
            cost_estimated += len(train) - j
            break

    # Return the calculated heuristic cost
    return cost_estimated


def a_star_search(yard: Yard, informed: bool) -> Solution:
    """
    FOR PROBLEM 6

    Consumes a `yard` to solve and a boolean `informed` flag.

    Produces a solution to the given `yard` using an A* algorithm.
    """

    # Terminate if uninformed and given YARD-1 as it will overflow on memory
    if not informed and yard.number == 1:
        return Solution(yard, 0, [])

    # Initialize the expanded node count and entry count (for heap tiebreaking)
    node_count: int = 0
    entry_count: int = 0

    # Initialize the current node as the root node
    node: Node = Node(yard.state_init, None, None)

    # Calculate the root node's heuristic estimated cost
    node.cost_estimated = heuristic(node.state, yard.state_goal)

    # Initialize the fringe as a heap with the root node inside
    fringe: list[HeapEntry] = [node.as_heap_entry(entry_count)]

    # Initialize the graph if the `informed` flag was passed
    graph: dict[State, int] = {node.state: node.cost_actual} if informed else {}

    # Loop while the fringe has entries in it
    while fringe:

        # Pop the smallest item off the heap (determined by the entry's
        # priority and tiebreaker values) and assign it as the current node
        _, _, node = heappop(fringe)

        # Increment the expanded node count
        node_count += 1

        # Check if the current node's state matches the goal state
        if node.state == yard.state_goal:

            # Return a solution containing the yard, expanded node
            # count, and a list of actions tracing back to the root node
            return Solution(yard, node_count, backtrack(node))

        # Iterate through each state-action pair expanded
        # from the current node's state and the yard's layout
        for result in expand(node.state, yard.track_layout):

            # Increment the current node's new actual path cost and store it
            cost_new = node.cost_actual + 1

            # Perform graph operations if the `informed` flag was passed
            if informed:

                # Skip if the current result's state is
                # already reached with a lower or equal cost
                if result.state in graph and cost_new >= graph[result.state]:
                    continue

                # Store the result's state in the graph with the new path cost
                graph[result.state] = cost_new

            # Create a new node as a child of the current node
            node_child = Node(result.state, result.action, node)

            # Assign the new actual path cost to the child node's path cost
            node_child.cost_actual = cost_new

            # Calculate the child node's estimated cost using the heuristic func
            node_child.cost_estimated = heuristic(
                node_child.state, yard.state_goal
            )

            # Increment the entry count tracker
            entry_count += 1

            # Push the child node to the fringe as a heap entry
            heappush(fringe, node_child.as_heap_entry(entry_count))

    # This point in the function can only be reached if no solution was found,
    # which is indicated by the empty action list in this returned solution
    return Solution(yard, node_count, [])


def simulated_annealing_search(yard: Yard, _: bool = False) -> Solution:
    """
    FOR PROBLEM 7

    Consumes a `yard` to solve. (unused bool to comply with unit test args)

    Produces a solution to the given `yard` using simulated annealing.
    """

    # Initialize the node count and annealing temperature
    node_count: int = 0
    temperature: float = 100.0

    # Initialize variables for 'reheating' to prevent getting stuck
    stuck_count: int = 0
    cost_last: int = -1

    # Initialize the current node as the root node
    node: Node = Node(yard.state_init, None, None)

    # Calculate the root node's heuristic estimated cost
    node.cost_estimated = heuristic(node.state, yard.state_goal)

    # Loop while the temperature is above the threshold
    while temperature > 0.001:

        # Increment the expanded node count
        node_count += 1

        # Check if the current node's state matches the goal state
        if node.state == yard.state_goal:

            # Return a solution containing the yard, expanded node
            # count, and a list of actions tracing back to the root node
            return Solution(yard, node_count, backtrack(node))

        # Get all possible results expanded from the current node
        results: list[ResultPair] = expand(node.state, yard.track_layout)

        # Break the loop if the results list is empty
        if not results:
            break

        # Pick an random state-action pair from the results list
        result = choice(results)

        # Calculate the result's estimated cost using the heuristic func
        result_cost_estimated = heuristic(result.state, yard.state_goal)

        # Calculate Delta E using the difference of the
        # estimated costs from the current node and result
        delta_energy = node.cost_estimated - result_cost_estimated

        # Accept the probability check if Delta E is greater than
        # zero or if the random simulated annealing check passes
        if delta_energy > 0 or random() < exp(delta_energy / temperature):

            # Reassign the current node to the result's state
            # and action with the previous node as its parent
            node = Node(result.state, result.action, node)

            # Calculate the current node's heuristic estimated cost
            node.cost_estimated = result_cost_estimated

            # Increment the current node's actual path cost
            node.cost_actual += 1

        # Increase the stuck count if the last cost hasn't changed
        if node.cost_estimated == cost_last:
            stuck_count += 1

        # Reset the stuck count and reassign the last cost if not
        else:
            stuck_count = 0
            cost_last = node.cost_estimated

        # Boost the temperature if the stuck count
        if stuck_count > 4_000:
            temperature += 50.0
            stuck_count = 0

        # Cool down the temperature
        temperature *= 0.99975

    # This point can only be reached if no solution was
    # found or the temperature reached 0, which is indicated
    # by the empty action list in this returned solution
    return Solution(yard, node_count, [])


def main() -> None:
    """Main function calling each test case."""

    print("\nStarting tests...")

    # Perform all tests
    test_search_func(blind_tree_search, False)
    test_search_func(a_star_search, False)
    test_search_func(a_star_search, True)
    test_search_func(simulated_annealing_search, False)

    print("\nTests complete.")


# Call main() if main.py was executed as a script
if __name__ == "__main__":
    main()
