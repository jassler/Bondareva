# All about balanced collections

Python 3 and the package sympy must be installed for this to work.

`find_grand_coalition.py` and `find_min_balanced.py` can be started on their own, they'll guide the user to input the relevant data.

`balanced_subcollections.py` can be called with command line arguments.

## Find all minimal collections
For a given collection `B` figure out all minimal subcollections it is made of (if any).

If `B = {{1}, {1,2}, {2,3}, {2,3,4}, {3,4}}`, call `balanced_subcollections.py` with the following arguments:

```
$ python balanced_subcollections.py [1] [1,2] [2,3] [2,3,4] [3,4]
{{1}, {2,3,4}} => (1, 1)
{{3,4}, {1,2}} => (1, 1)
```

With `find_min_balanced.py` you can enter your coalitions line by line and additionaly find out, if your collection is weakly balanced, minimal balanced, balanced, or not balanced.

```
Coalition #1: 1
Coalition #2: 1,2
Coalition #3: 2,3
Coalition #4: 2,3,4
Coalition #5: 3,4
Coalition #6:
δ_{2,3,4} = -δ_{3,4} + 1
δ_{2,3} = 0
δ_{1,2} = δ_{3,4}
δ_{1} = -δ_{3,4} + 1
It is weakly balanced
Do you want to find all minimal balanced collections?
Y/n: Y
Trying to find all minimal balanced collections
{{1}, {2,3,4}} => (1, 1)
{{3,4}, {1,2}} => (1, 1)
```

## Find minimal collections for an n-player game
```
$ python balanced_subcollections.py -p 3
{{1,2,3}} => (1)
{{1}, {2,3}} => (1, 1)
{{1,3}, {2}} => (1, 1)
{{3}, {1,2}} => (1, 1)
{{2}, {3}, {1}} => (1, 1, 1)
{{1,2}, {1,3}, {2,3}} => (1/2, 1/2, 1/2)
```

## Find minimum payoff for a players to form a grand coalition
Given a game (N;v) with v(S) given for all v(S) subset of N except N. It then calculates what v(N) has to be for the players to form a grand coalition.

Simply start `find_grand_coalition.py` and it'll guide you through.

```
$ python grand_coalition.py
Number of players participating: 3
v() = 0
v(1) = 1
v(2) = 3
v(3) = 2
v(1, 2) = 4
v(1, 3) = 3
v(2, 3) = 4

v(1, 2, 3) >= 6.0
--- Due to the following calculations ---
v(1, 3) + v(2)     = 6.0
v(3) + v(1, 2)     = 6.0
v(2) + v(3) + v(1) = 6.0
v(1, 3) + v(2)     = 6.0
v(3) + v(1, 2)     = 6.0
```