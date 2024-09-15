class ShipPlacer:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size

    def can_place_ship(self, grid, row, col, size, orientation):
        if orientation == 'H':
            if col + size > self.grid_size:
                return False
            for i in range(size):
                if grid[row][col + i] != 0:
                    return False
            if row > 0 and any(grid[row - 1][col + i] != 0 for i in range(size)):
                return False
            if row < self.grid_size - 1 and any(grid[row + 1][col + i] != 0 for i in range(size)):
                return False
            if col > 0 and grid[row][col - 1] != 0:
                return False
            if col + size < self.grid_size and grid[row][col + size] != 0:
                return False
        else:
            if row + size > self.grid_size:
                return False
            for i in range(size):
                if grid[row + i][col] != 0:
                    return False
            if col > 0 and any(grid[row + i][col - 1] != 0 for i in range(size)):
                return False
            if col < self.grid_size - 1 and any(grid[row + i][col + 1] != 0 for i in range(size)):
                return False
            if row > 0 and grid[row - 1][col] != 0:
                return False
            if row + size < self.grid_size and grid[row + size][col] != 0:
                return False
        return True

    def add_ship_to_grid(self, grid, row, col, size, orientation):
        if orientation == 'H':
            for i in range(size):
                grid[row][col + i] = 1
        else:
            for i in range(size):
                grid[row + i][col] = 1
