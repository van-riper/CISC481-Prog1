# CISC481 Programming Assignment 1 Writeup

This is the writeup for my submission of programming assignment 1 in CISC481.


## Search Space Calculation

The search space for $c$ cars on $t$ tracks is equal to:

$$
\frac{(c+t-1)!}{(t-1)!}
$$

For example, on YARD-1, let $c=6,\ t=6$,

$$
\frac{(6+6-1)!}{(6-1)!} = \frac{11!}{5!} = 332,640
$$

So, the search space on YARD-1 is 332,640 possible states.


## Heuristic Admissibility

The heuristic I wrote is admissible because it represents the minimum amount of
actions needed to solve the yard without overestimating the cost. It identifies
the deepest misplaced car on a track and calculates the cost to move that car
and everything shunted in front of it, as the cars in front must be cleared
before the foundation can be corrected. Since each of these cars must take at
least one move to reach the goal, the heuristic provides a guaranteed lower
bound of the true remaining cost.


## A* Algorithm Tests

A* demonstrates that combining a deeply informed heuristic with graph memory is
the most efficient approach. By storing reached states, it prunes 90% of the
Yard 1 search space, solving it in just 35,577 nodes and finding the optimal
22-action path in roughly one second.


## Simulated Annealing Tests

Simulated Annealing functions as a stochastic explorer that prioritizes low
memory usage over path optimality. Because it makes randomized moves based on
temperature, it often produces thousands of redundant actions, like the 62,094
moves in Yard 1. It requires "re-heating" strategies to escape local optimal
that deterministic algorithms like A* avoid entirely.


## Sample Output

```
$ python main.py

Starting tests...

Running tests for blind_tree_search (uninformed)

Yard 1: Skipping due to memory limits
Yard 2: Skipping due to memory limits
Yard 3: 00.000161s | Node count: 7
        (LEFT  2 1)
        (LEFT  3 1)
Yard 4: 00.004054s | Node count: 155
        (LEFT  2 1)
        (LEFT  3 1)
        (LEFT  3 1)
        (LEFT  4 1)
Yard 5: 00.102141s | Node count: 2,698
        (LEFT  2 1)
        (LEFT  3 1)
        (RIGHT 1 2)
        (LEFT  3 1)
        (LEFT  2 1)
        (LEFT  4 1)

Running tests for a_star_search (uninformed)

Yard 1: Skipping due to memory limits
Yard 2: 06.482420s | Node count: 132,765
        (LEFT  2 1)
        (RIGHT 1 5)
        (RIGHT 1 2)
        (LEFT  4 2)
        (LEFT  3 2)
        (LEFT  4 2)
        (LEFT  2 1)
        (LEFT  2 1)
        (LEFT  2 1)
        (LEFT  5 1)
        (RIGHT 1 2)
        (LEFT  5 1)
        (LEFT  2 1)
        (LEFT  2 1)
Yard 3: 00.000159s | Node count: 3
        (LEFT  2 1)
        (LEFT  3 1)
Yard 4: 00.000203s | Node count: 5
        (LEFT  2 1)
        (LEFT  3 1)
        (LEFT  3 1)
        (LEFT  4 1)
Yard 5: 00.002257s | Node count: 52
        (LEFT  2 1)
        (LEFT  3 1)
        (RIGHT 1 2)
        (LEFT  3 1)
        (LEFT  2 1)
        (LEFT  4 1)

Running tests for a_star_search (informed)

Yard 1: 01.079758s | Node count: 35,577
        (RIGHT 1 2)
        (RIGHT 2 6)
        (RIGHT 2 6)
        (LEFT  6 5)
        (RIGHT 4 5)
        (LEFT  5 3)
        (RIGHT 4 5)
        (RIGHT 4 5)
        (LEFT  5 3)
        (LEFT  5 3)
        (RIGHT 5 6)
        (LEFT  6 2)
        (LEFT  6 2)
        (LEFT  6 2)
        (LEFT  2 1)
        (LEFT  3 1)
        (LEFT  3 1)
        (LEFT  3 1)
        (LEFT  2 1)
        (RIGHT 1 3)
        (LEFT  2 1)
        (LEFT  3 1)
Yard 2: 00.074594s | Node count: 2,617
        (LEFT  2 1)
        (RIGHT 1 5)
        (RIGHT 1 2)
        (LEFT  4 2)
        (LEFT  3 2)
        (LEFT  4 2)
        (LEFT  2 1)
        (LEFT  2 1)
        (LEFT  2 1)
        (LEFT  5 1)
        (RIGHT 1 2)
        (LEFT  5 1)
        (LEFT  2 1)
        (LEFT  2 1)
Yard 3: 00.000102s | Node count: 3
        (LEFT  2 1)
        (LEFT  3 1)
Yard 4: 00.000155s | Node count: 5
        (LEFT  2 1)
        (LEFT  3 1)
        (LEFT  3 1)
        (LEFT  4 1)
Yard 5: 00.000946s | Node count: 31
        (LEFT  2 1)
        (LEFT  3 1)
        (RIGHT 1 2)
        (LEFT  3 1)
        (LEFT  2 1)
        (LEFT  4 1)

Running tests for simulated_annealing_search (uninformed)

Yard 1: 01.779682s | Node count: 78,287   | Action count: 62,094
Yard 2: 00.415754s | Node count: 19,795   | Action count: 19,604
Yard 3: 00.000135s | Node count: 5        | Action count: 4
Yard 4: 00.032626s | Node count: 1,405    | Action count: 1,402
Yard 5: 00.111153s | Node count: 5,101    | Action count: 5,098

Tests complete.
```
