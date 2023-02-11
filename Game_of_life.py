import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update(frame, img, grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # Compute the number of alive neighbors
            alive_neighbors = (grid[i, (j-1)%grid.shape[1]] + grid[i, (j+1)%grid.shape[1]] +
                               grid[(i-1)%grid.shape[0], j] + grid[(i+1)%grid.shape[0], j] +
                               grid[(i-1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i-1)%grid.shape[0], (j+1)%grid.shape[1]] +
                               grid[(i+1)%grid.shape[0], (j-1)%grid.shape[1]] + grid[(i+1)%grid.shape[0], (j+1)%grid.shape[1]])
            # Update the cell based on the rules of the Game of Life
            if grid[i, j] == 1 and (alive_neighbors < 2 or alive_neighbors > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and alive_neighbors == 3:
                new_grid[i, j] = 1
    # Update the grid for the next iteration
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

def main():
    grid = np.random.choice([0, 1], (100, 100))
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    anim = animation.FuncAnimation(fig, update, fargs=(img, grid), frames=100, interval=100)
    plt.show()

if __name__ == '__main__':
    main()