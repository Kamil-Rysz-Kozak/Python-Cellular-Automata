"""
Program done by Kamil R. Kozak
You may modify, share and monetize as long as you attribute it properly it or smth...
Cellular Automaton with self-modifying rules
Needs optimization and whole these, so any help will be welcome.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

neighbourhood_matrix = np.array([[0, 1, 1], [1, 0, 1], [0, 0, 1]])

#Function that gets neighbourhood matrix for each cell. Set default neighbourhood matrix to 0. [TO BE TESTED]
def get_surrounding_matrix(binary_grid, i, j):
    rows, cols = binary_grid.shape
    surrounding_matrix = np.zeros((3, 3), dtype=np.uint8)
    for ii in range(i - 1, i + 2):
        for jj in range(j - 1, j + 2):
            if 0 <= ii < rows and 0 <= jj < cols:
                surrounding_matrix[ii - i + 1, jj - j + 1] = binary_grid[ii, jj]
    return surrounding_matrix

#Converts array of 0s and 1s to number.
def binary_array_to_number(binary_array):
    decimal_number = 0
    for index, value in enumerate(binary_array[::-1]):
        if value:
            decimal_number += 2**index
    return decimal_number+1                 #Had to add 1 so there is no zero-neighbour survival later in CA. Or, what's worse, 0-neighbour cell BIRTH.

#Function that returns rows of a matrix as separate numpy arrays.
def convert_2d_array_to_binary_rows(matrix):
    num_rows, num_cols = matrix.shape
    binary_rows = np.empty(num_rows, np.uint8)
    for i in range(num_rows):
        row = matrix[i, :]
        binary_rows[i] = binary_array_to_number(row)
    return binary_rows

#Same as the above, but with columns.
def convert_2d_array_to_binary_columns(matrix):
    columns = [column for column in matrix.T]
    binary_columns = [np.array(column, dtype=int) for column in columns]
    return [binary_array_to_number(binary_column) for binary_column in binary_columns]

#As the name suggets. Function that computes rules for every cell individually for next step.
def compute_rules(matrix):
    survival = convert_2d_array_to_binary_rows(matrix)
    birth = convert_2d_array_to_binary_columns(matrix)
    survival = np.unique(np.concatenate((survival, birth)))
    return survival, birth

#Compares alive neighbours to survival/birth and returns if it satisfies it.
def check_array(a, x):
    for i in range(len(a)):
        if x != a[i]:
            continue
        else:
            return 1
    else:
        return 0

#print(compute_rules(neighbourhood_matrix))         [TEST ONLY]

def update(frame, img, grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            #Get neighbourhood matrix for cell
            neighbourhood_matrix = get_surrounding_matrix(grid, i, j)
            #Compute rules for the cell
            survival, birth = compute_rules(neighbourhood_matrix)                           
            #Compute the number of alive neighbors
            alive_neighbors = (grid[i, (j-1)%grid.shape[1]] + grid[i, (j+1)%grid.shape[1]] +
                               grid[(i-1)%grid.shape[0], j] + grid[(i+1)%grid.shape[0], j] +
                               grid[(i-1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i-1)%grid.shape[0], (j+1)%grid.shape[1]] +
                               grid[(i+1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i+1)%grid.shape[0], (j+1)%grid.shape[1]])
            #Update cells according to rules in each of them
            if grid[i, j] == 1 and (check_array(survival, alive_neighbors) == 1):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and (check_array(birth, alive_neighbors) == 1):
                new_grid[i, j] = 1
    #Update the grid for the next iteration
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

def main():
    grid = np.random.choice([0, 1], (100, 100))
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid), frames=24, interval=100)
    plt.show()

if __name__ == '__main__':
    main()
