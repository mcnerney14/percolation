import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt

from quick_union import QuickUnion


def matrix_id_to_list_id(x_y: Tuple[int, int], row_length: int) -> int:
    x, y = x_y
    return y + x * row_length


def list_id_to_matrix_id(list_id: int, row_length: int) -> Tuple[int, int]:
    x = list_id // row_length
    y = list_id % row_length
    return (x, y)


class Grid(object):
    def __init__(self, grid_size=3):
        ''' We define an initial matrix with every cell closed
        ie) closed_matrix = 1 for True
        we also build a network of connected cells to determine
        if there is a path for water to percolate from the top
        of our grid to the bottom '''
        self.grid_size = grid_size
        self.num_elements = grid_size * grid_size
        self.closed_matrix = np.ones((self.grid_size, self.grid_size),
                                     dtype=np.int16)
        self.connected_cells = QuickUnion(self.grid_size ** 2)

    def open_random_cell(self):  # -> Tuple[int, int]:
        ''' Each time function is called, it opens one cell (change from 1 to 0)
        in our closed_matrix and returns the coordinates of this random cell '''
        out_arr = np.argwhere(self.closed_matrix)
        # from my array of non-zero indices, select one element in a random order
        rand_cell = out_arr[np.random.choice(out_arr.shape[0], 1, replace=False)]
        # change one cell from output of rand_cell to 0
        x = rand_cell[0, 0]
        y = rand_cell[0, 1]
        self.closed_matrix[x, y] = 0
        x_y = (x, y)
        return x_y

    def check_open_neighbors(self, x_y: Tuple[int, int]) -> List[Tuple[int, int]]:
        ''' We take one tuple of matrix coordinates (presumably from open_random_cell)
        then if any cell above, below, left, or right or our one open cell is
        also open (value of 0) we add it to our list of open neighbors '''
        open_neighbors = []
        x, y = x_y
        grid_size = self.grid_size

        if x >= 0 and y - 1 >= 0:
            if self.closed_matrix[x][y - 1] == 0:
                open_neighbors.append((x, y - 1))
        if x >= 0 and y + 1 < grid_size:
            if self.closed_matrix[x][y + 1] == 0:
                open_neighbors.append((x, y + 1))
        if x - 1 >= 0 and y >= 0:
            if self.closed_matrix[x - 1][y] == 0:
                open_neighbors.append((x - 1, y))
        if x + 1 < grid_size and y >= 0:
            if self.closed_matrix[x + 1][y] == 0:
                open_neighbors.append((x + 1, y))
        return open_neighbors

    def visualization_heat_plot(self):
        plt.imshow(self.closed_matrix, cmap='cool', interpolation='nearest')
        plt.show()

    def union_neighbors_with_random_cell(self, neighbors_matrix_id: List[Tuple[int, int]],
                                         cell_matrix_id: Tuple[int, int]):
        ''' We take in our List of open_neighbors (with matrix ids) and our one
        random cell (with matrix id), convert all these values to a list id
        because our quick_union class operates with list IDs not matrix values.
        then we connect our open neighbors together to our random cell '''
        cell_list_id = matrix_id_to_list_id(cell_matrix_id, self.grid_size)
        for i in range(len(neighbors_matrix_id)):
            neighbor_list_id = matrix_id_to_list_id(neighbors_matrix_id[i], self.grid_size)
            self.connected_cells.union(cell_list_id, neighbor_list_id)
        # print(self.connected_cells.ids)
        # print(self.connected_cells.size)


def run_percolation(grid_size: int, iterations: int):
    ''' In order to see when a grid percolates, we need to
    1) make a grid and open open a random cell
    2) check which neighbors are 'open neighbors' with the tuple that is
    returned from open random cells
    3) union neighbors with random cell if they are open, passing in our
    open_neighbors matrix and one random cell
    4) print a visualization of our grid
    5) see how many cells must open before our grid can percolate '''
    grid = Grid(grid_size)
    for i in range(iterations):
        cell = grid.open_random_cell()  # cell is a Tuple
        open_neighbors = grid.check_open_neighbors(cell)
        grid.union_neighbors_with_random_cell(open_neighbors, cell)
        grid.visualization_heat_plot()
        if grid.connected_cells.connection_percolates():
            percentage = i / (grid_size * grid_size)
            print(f'we percolated when {percentage} of total cells are open')


if __name__ == "__main__":
    run_percolation(6, 20)
