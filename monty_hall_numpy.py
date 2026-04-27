"""Monte Carlo simulation of the Monty Hall problem using NumPy.

Same game as `monty_hall_random.py` but the triplets are stored as an `(n, 3)`
integer array. Triplet construction is fully vectorised; the per-game stay vs
switch decisions still iterate row-by-row to mirror the original notebook.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


def generate_triplets(n: int) -> np.ndarray:
    """Return an `(n, 3)` array of triplets, each a permutation of `[0, 0, 1]`.

    Vectorised: start with zeros and set a single random column to 1 per row.
    """
    triplets = np.zeros((n, 3), dtype=int)
    ones_indices = np.random.randint(0, 3, size=n)
    triplets[np.arange(n), ones_indices] = 1
    return triplets


def pick_from_triplets(
    triplets: np.ndarray,
) -> Tuple[List[int], List[int], List[List[int]]]:
    """For each row, simulate stay vs switch.

    Returns three parallel lists: prize indicator if staying, prize indicator
    if switching, and the [first, host_open, switched_to] index triples.
    """
    n = triplets.shape[0]
    result_stay: List[int] = []
    result_change: List[int] = []
    picks: List[List[int]] = []

    for i in range(n):
        triplet = triplets[i]

        # Step 1: contestant picks a door uniformly at random
        first_pick = int(np.random.randint(0, 3))
        result_stay.append(int(triplet[first_pick]))

        # Step 2: host opens a door that hides a goat (0) and is not the contestant's pick
        zero_indices = [j for j in range(3) if triplet[j] == 0 and j != first_pick]
        second_pick = int(np.random.choice(zero_indices))

        # Step 3: contestant switches to the only remaining door
        # (the three door indices always sum to 0 + 1 + 2 = 3)
        third_pick = 3 - first_pick - second_pick
        result_change.append(int(triplet[third_pick]))
        picks.append([first_pick, second_pick, third_pick])

    return result_stay, result_change, picks


def main(n: int = 100_000) -> None:
    """Run `n` simulated games and print stay vs switch wins."""
    triplets = generate_triplets(n)
    result_stay, result_change, picks = pick_from_triplets(triplets)

    # Sanity check: every picks-row should be a permutation of (0, 1, 2)
    assert {sum(p) for p in picks} == {3}

    print(f"Trials:        {n}")
    print(f"Stay wins:     {sum(result_stay)}  ({sum(result_stay) / n:.4f})")
    print(f"Switch wins:   {sum(result_change)}  ({sum(result_change) / n:.4f})")


if __name__ == "__main__":
    main()
