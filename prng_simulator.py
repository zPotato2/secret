import random
from datetime import datetime, timedelta

def generate_grid(seed, size=5, mines=3):
    random.seed(seed)
    grid = [[0 for _ in range(size)] for _ in range(size)]

    all_cells = [(i, j) for i in range(size) for j in range(size)]
    mine_positions = random.sample(all_cells, mines)

    for x, y in mine_positions:
        grid[x][y] = 1

    return grid

def grids_match(grid1, grid2):
    return all(grid1[i][j] == grid2[i][j] for i in range(5) for j in range(5))

def try_bruteforce_seed(observed_grid, window=15, size=5, mines=3):
    now = datetime.utcnow()
    for seconds in range(-window, window + 1):
        seed_time = now - timedelta(seconds=seconds)
        seed = int(seed_time.timestamp())
        test_grid = generate_grid(seed, size=size, mines=mines)
        if grids_match(test_grid, observed_grid):
            print(f"🔓 PRNG matched with seed {seed}")
            return test_grid
    return None
