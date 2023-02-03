import numpy as np

# Rule number (0-2047)
rule = 30

# Number of generations
generations = 37

# Initial state (0 or 1)
init_state = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)

# Convert rule number to binary
rule_binary = format(rule, '08b')

# Create rule table
rule_table = {
    '111': int(rule_binary[0]),
    '110': int(rule_binary[1]),
    '101': int(rule_binary[2]),
    '100': int(rule_binary[3]),
    '011': int(rule_binary[4]),
    '010': int(rule_binary[5]),
    '001': int(rule_binary[6]),
    '000': int(rule_binary[7]),
}

# Print the initial state
print(' '.join(map(str, init_state)))

# Iterate over the generations
for i in range(generations):
    new_state = np.zeros(init_state.shape[0], dtype=np.uint8)
    # Iterate over each cell
    for j in range(init_state.shape[0]):
        # Get the neighborhood of the current cell
        neighborhood = ''
        if j == 0:
            left, center, right = 0, init_state[j], init_state[j + 1]
        elif j == init_state.shape[0] - 1:
            left, center, right = init_state[j - 1], init_state[j], 0
        else:
            left, center, right = init_state[j - 1], init_state[j], init_state[j + 1]
        neighborhood += str(left) + str(center) + str(right)
        
        # Use the neighborhood to determine the new state of the current cell
        new_state[j] = rule_table[neighborhood]
    init_state = new_state
    print(' '.join(map(str, init_state)))


# TO DO: user input for rules and generations