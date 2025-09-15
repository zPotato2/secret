import json
import hashlib

def parse_grid(content):
    lines = content.strip().split("\n")
    grid = []

    for line in lines:
        row = []
        for char in line.strip().split():
            if "💣" in char:
                row.append(1)
            elif "💎" in char:
                row.append(0)
        if row:
            grid.append(row)

    return grid if len(grid) == 5 and all(len(r) == 5 for r in grid) else None

def hash_grid(grid):
    flat = ''.join(str(cell) for row in grid for cell in row)
    return hashlib.md5(flat.encode()).hexdigest()

def find_repeat(current_grid, log_file='mines_logs.json'):
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        current_hash = hash_grid(current_grid)
        for entry in logs:
            if entry.get("hash") == current_hash:
                return entry
    except:
        pass
    return None
