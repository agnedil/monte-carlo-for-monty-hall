"""Monte Carlo simulation of the Monty Hall problem using Python's `random` module.

Each trial is one game:
  1. The prize is placed behind one of three doors uniformly at random.
  2. The contestant picks a door uniformly at random.
  3. The host opens one of the remaining doors that hides a goat.
  4. We record both outcomes: keeping the original pick (stay) and switching.

The script prints the empirical stay/switch win counts; the long-run frequencies
should approach 1/3 (stay) and 2/3 (switch).
"""

from __future__ import annotations

import random
from typing import List, Tuple


# A single game state: a list of length 3 with two 0s (goats) and one 1 (prize).
Triplet = List[int]


def generate_triplets(n: int) -> List[Triplet]:
    """Build `n` shuffled `[0, 0, 1]` triplets - one per simulated game."""
    triplets: List[Triplet] = []
    for _ in range(n):
        triplet = [0, 0, 1]
        random.shuffle(triplet)
        triplets.append(triplet)
    return triplets


def pick_from_triplets(
    triplets: List[Triplet],
) -> Tuple[List[int], List[int], List[List[int]]]:
    """For each triplet, simulate stay vs switch.

    Returns three parallel lists: prize indicator if staying, prize indicator
    if switching, and the [first, host_open, switched_to] index triples.
    """
    result_stay: List[int] = []
    result_change: List[int] = []
    picks: List[List[int]] = []

    for triplet in triplets:
        # Step 1: contestant picks a door uniformly at random
        first_pick = random.randint(0, 2)
        result_stay.append(triplet[first_pick])

        # Step 2: host opens a door that hides a goat (0) and is not the contestant's pick
        zero_indices = [i for i, v in enumerate(triplet) if v == 0 and i != first_pick]
        second_pick = random.choice(zero_indices)

        # Step 3: contestant switches to the only remaining door
        # (the three door indices always sum to 0 + 1 + 2 = 3)
        third_pick = 3 - first_pick - second_pick
        result_change.append(triplet[third_pick])
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
