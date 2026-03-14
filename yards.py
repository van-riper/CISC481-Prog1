"""
This file contains all the predefined yards from the assignment description.

If you want to make more yards to test on the main program, write the layout,
initial state, and goal state to thisfile in the same format as the other yards,
then make a `Yard` object containing the corresponding layout and states, and
include it in the `ALL_YARDS` tuple at the bottom of this file.
"""

from definitions import State, TrackLayout, Yard

### YARD 1 ###

TRACK_LAYOUT_1: TrackLayout = {
    1: [2, 3],
    2: [1, 6],
    3: [1, 5],
    4: [5],
    5: [3, 4, 6],
    6: [2, 5],
}

STATE_INIT_1: State = State(
    (
        ("*",),
        ("e",),
        (),
        ("b", "c", "a"),
        (),
        ("d",),
    )
)

STATE_GOAL_1: State = State(
    (
        ("*", "a", "b", "c", "d", "e"),
        (),
        (),
        (),
        (),
        (),
    )
)

YARD_1: Yard = Yard(1, TRACK_LAYOUT_1, STATE_INIT_1, STATE_GOAL_1)


### YARD 2 ###

TRACK_LAYOUT_2: TrackLayout = {
    1: [2, 5],
    2: [1, 3, 4],
    3: [2],
    4: [2],
    5: [2],
}

STATE_INIT_2: State = State(
    (
        ("*",),
        ("d",),
        ("b",),
        ("a", "e"),
        ("c",),
    )
)

STATE_GOAL_2: State = State(
    (
        ("*", "a", "b", "c", "d", "e"),
        (),
        (),
        (),
        (),
    )
)

YARD_2: Yard = Yard(2, TRACK_LAYOUT_2, STATE_INIT_2, STATE_GOAL_2)


### YARD 3 ###

TRACK_LAYOUT_3: TrackLayout = {
    1: [2, 3],
    2: [1],
    3: [1],
}

STATE_INIT_3: State = State(
    (
        ("*",),
        ("a",),
        ("b",),
    )
)

STATE_GOAL_3: State = State(
    (
        ("*", "a", "b"),
        (),
        (),
    )
)

YARD_3: Yard = Yard(3, TRACK_LAYOUT_3, STATE_INIT_3, STATE_GOAL_3)


### YARD 4 ###

TRACK_LAYOUT_4: TrackLayout = {
    1: [2, 3, 4],
    2: [1],
    3: [1],
    4: [1],
}

STATE_INIT_4: State = State(
    (
        ("*",),
        ("a",),
        ("b", "c"),
        ("d",),
    )
)

STATE_GOAL_4: State = State(
    (
        ("*", "a", "b", "c", "d"),
        (),
        (),
        (),
    )
)

YARD_4: Yard = Yard(4, TRACK_LAYOUT_4, STATE_INIT_4, STATE_GOAL_4)


### YARD 5 ###

TRACK_LAYOUT_5: TrackLayout = TRACK_LAYOUT_4

STATE_INIT_5: State = State(
    (
        ("*",),
        ("a",),
        ("c", "b"),
        ("d",),
    )
)

STATE_GOAL_5: State = State(
    (
        ("*", "a", "b", "c", "d"),
        (),
        (),
        (),
    )
)

YARD_5: Yard = Yard(5, TRACK_LAYOUT_5, STATE_INIT_5, STATE_GOAL_5)


# Tuple containing all the predefined yards
ALL_YARDS: tuple[Yard, ...] = (
    YARD_1,
    YARD_2,
    YARD_3,
    YARD_4,
    YARD_5,
)
