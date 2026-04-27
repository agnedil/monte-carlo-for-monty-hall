# Monte Carlo Simulation of the Monty Hall Problem

Two small simulators that empirically confirm the (famously counter-intuitive)
answer to the [Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem):
**always switch.**

## The problem

You are on a game show with three closed doors. Behind one door is a car;
behind the other two are goats. The rules:

1. You pick a door.
2. The host — who knows where the car is — opens one of the other two doors,
   always revealing a goat.
3. The host asks whether you want to keep your original door or switch to the
   remaining closed one.

Should you switch? Intuition says it shouldn't matter (two doors left, one
prize, "50/50"). It does matter:

- Stay: you win **1/3** of the time.
- Switch: you win **2/3** of the time.

The asymmetry is created by the host's knowledge: the door he opens is *not*
random, so the door he leaves closed carries information about where the car
is.

## The proposed solution

Rather than reason through conditional probabilities, we run the experiment
many times and count outcomes (Monte Carlo). One trial is one game:

1. Build a triplet that encodes the door layout — a list of length 3 with two
   `0`s (goats) and one `1` (car).
2. Pick a starting index uniformly at random — the contestant's first pick.
3. Pick one of the other indices that points to a `0` — the host's reveal.
4. The remaining index is the "switch" pick.

For each trial we record whether the *first* index lands on the `1` (stay
win) and whether the *third* index lands on the `1` (switch win). With
`n = 100,000` trials the empirical frequencies converge to the theoretical
1/3 and 2/3.

## Repo structure

```
Monty-Hall-Monte-Carlo/
├── monty_hall_random.py     # standard-library implementation (random module)
├── monty_hall_numpy.py      # NumPy implementation
├── requirements.txt
└── README.md
```

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt    # only needed for the NumPy version

python monty_hall_random.py
python monty_hall_numpy.py
```

Sample output:

```
Trials:        100000
Stay wins:     33227  (0.3323)
Switch wins:   66773  (0.6677)
```

## Difference between the two implementations

| Aspect              | `monty_hall_random.py`            | `monty_hall_numpy.py`                              |
|---------------------|-----------------------------------|----------------------------------------------------|
| RNG                 | `random` (Mersenne Twister)       | `numpy.random` (default BitGenerator: PCG64)       |
| Triplet storage     | list of Python lists              | `(n, 3)` `int` `ndarray`                           |
| Triplet generation  | `random.shuffle` per game (loop)  | vectorised: zeros + one random column set to 1     |
| Per-game decision   | Python loop                       | Python loop over rows (kept as in the notebook)    |
| Dependencies        | standard library only             | `numpy`                                            |
| Memory              | ~3× per-int Python overhead       | one contiguous `int` array                         |

Functionally the two scripts simulate the same game and produce statistically
equivalent results.

## Implications

- **Vectorised generation pays off only when it stays vectorised.** The NumPy
  version generates triplets without a Python loop, which is much faster for
  large `n`. But the per-game stay/switch logic still iterates row by row,
  so the overall speed-up over the `random` version is modest. To get the
  full benefit you would also need to vectorise the host's reveal — for
  example, by computing first picks as an `(n,)` array, identifying the
  prize column per row, and using boolean masks to derive the switch
  outcome without a Python loop.

- **`random` is fine for small simulations and embedded use.** It needs no
  dependencies, ships with Python, and at `n = 100,000` the runtime
  difference is small.

- **Reproducibility differs.** `random` and `numpy.random` are seeded
  independently. If you need byte-for-byte reproducible output, set the
  matching seed (`random.seed(...)` or `np.random.seed(...)` /
  `np.random.default_rng(seed)`) in whichever script you are running.

- **Statistical, not analytical.** Monte Carlo gives an empirical estimate
  with error of order `1/sqrt(n)`. With 100,000 trials the standard error on
  the win rate is roughly 0.0015, so the empirical numbers can wobble by a
  few hundred wins between runs while still being consistent with 1/3 and
  2/3.

- **The answer depends on host behaviour, not the implementation.** If the
  host opened a door at random (sometimes revealing the car) the 1/3 vs 2/3
  split would disappear. The host's deterministic "always reveal a goat"
  rule is what makes switching strictly better — both scripts encode this
  by sampling the host's door from the goat indices that exclude the
  contestant's pick.
