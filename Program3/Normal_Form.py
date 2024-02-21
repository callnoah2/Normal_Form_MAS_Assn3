import numpy as np

def read_payoff_matrix(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting values from the input lines
    rows, columns = map(int, lines[0].split())
    row_rewards = list(map(int, lines[1].split()))
    col_rewards = list(map(int, lines[2].split()))

    # Creating the matrix
    matrix = [[[0] * columns for _ in range(rows)] for _ in range(2)]

    # Filling in the matrix with row rewards
    for i in range(rows):
        matrix[0][i] = row_rewards[i * columns: (i + 1) * columns]

    # Filling in the matrix with column rewards
    for i in range(rows):
        matrix[1][i] = col_rewards[i * columns: (i + 1) * columns]

    return matrix



def identify_strictly_dominated_strategies(matrix):
    num_rows = len(matrix[0])
    num_cols = len(matrix[0][0])

    # Get the header titles
    col_headers = []
    for i in range(num_cols):
        col_headers.append(chr(ord('Z') - i))
    col_headers.reverse()

    row_letters = []
    for i in range(num_rows):
        row_letters.append(chr(ord('A') + i))

    row_dominated = [False] * num_rows
    col_dominated = [False] * num_cols

  # Check for strictly row dominance
    for i in range(num_rows):
        for j in range(num_rows):
            if i != j and not row_dominated[i]:
                row_i_strict_dom = all(matrix[0][i][k] <  matrix[0][j][k] for k in range(num_cols))
                if row_i_strict_dom:
                    row_dominated[i] = True

    # Check for strictly column dominance
    for k in range(num_cols):
        for l in range(num_cols):
            if k != l and not col_dominated[k]:
                col_k_strict_dom = all(all(matrix[1][i][k] < matrix[1][i][l] for i in range(num_rows)) for k in range(num_cols))
                if col_k_strict_dom:
                    col_dominated[k] = True

    print("Row player strictly dominated strategies:", [row_letters[i] for i, dominated in enumerate(row_dominated) if dominated])
    print("Column player strictly dominated strategies:", [col_headers[k] for k, dominated in enumerate(col_dominated) if dominated])

    return row_dominated, col_dominated

def identify_weakly_dominated_strategies(matrix):
    num_rows = len(matrix[0])
    num_cols = len(matrix[0][0])

    # Get the header titles
    col_headers = [chr(ord('Z') - i) for i in range(num_cols)]
    col_headers.reverse()

    row_letters = [chr(ord('A') + i) for i in range(num_rows)]

    row_dominated = [False] * num_rows
    col_dominated = [False] * num_cols

    # Check for weakly row dominance
    for i in range(num_rows):
        for j in range(num_rows):
            if i != j and not row_dominated[i]:
                row_i_weak_dom = all(matrix[0][i][k] <= matrix[0][j][k] for k in range(num_cols))
                if row_i_weak_dom:
                    row_dominated[i] = True

    # Check for weakly column dominance
    for k in range(num_cols):
        for l in range(num_cols):
            if k != l and not col_dominated[k]:
                col_k_weak_dom = all(matrix[1][i][k] <= matrix[1][i][l] for i in range(num_rows))
                if col_k_weak_dom:
                    col_dominated[k] = True

    print("Row player weakly dominated strategies:", [row_letters[i] for i, dominated in enumerate(row_dominated) if dominated])
    print("Column player weakly dominated strategies:", [col_headers[k] for k, dominated in enumerate(col_dominated) if dominated])

    return row_dominated, col_dominated

def identify_pure_strategy_equilibria(matrix):
    num_rows_player1 = len(matrix[0])
    num_cols_player1 = len(matrix[0][0])

    num_rows_player2 = len(matrix[1])
    num_cols_player2 = len(matrix[1][0])

    pure_equilibria = []

    for i in range(num_rows_player1):
        for j in range(num_rows_player2):
            try:
                # Check if (i, j) is a Nash equilibrium
                is_nash_equilibrium = all(
                    matrix[0][i][k] >= matrix[0][j][k] for k in range(min(num_cols_player1, num_cols_player2))
                ) and all(
                    matrix[1][k][i] >= matrix[1][k][j] for k in range(min(num_rows_player1, num_rows_player2))
                )

                if is_nash_equilibrium:
                    pure_equilibria.append((i, j))
            except IndexError:
                print("IndexError occurred. Matrix:", matrix)
                raise

    for equilibrium in pure_equilibria:
        print(f"Player 1 chooses strategy {equilibrium[0]}, Player 2 chooses strategy {equilibrium[1]}")

    return pure_equilibria

def print_normal_form_table(matrix):
    num_rows = len(matrix[0])
    num_cols = len(matrix[0][0])
    
    # Get the header titles
    headers = []
    
    for i in range(num_cols):
       headers.append(chr(ord('Z') - i))
    
    # Reformat letters list
    headers.reverse()
    
    # Print the column headers
    print('   |', end = ' ')
    for letter in headers:
        print("   ",letter, '    |', end = ' ')
    
    print(" ")

   # list of row letters
    row_letters = []
    
    for i in range(num_rows):
        row_letters.append(chr(ord('A') + i))
        
    # print table
    for i in range(num_rows):
        print(row_letters[i], end = " ")
        for j in range(num_cols):
            print(" | ", end = " ")
            for k in range(num_rows):
                print(matrix[k][i][j], " ", end = " ")
        print("|")
    

file_pathA = "Program3/data/prog3A.txt"
file_pathB = "Program3/data/prog3B.txt"
file_pathC = "Program3/data/prog3C.txt"
my_file = "Program3/data/myProg3File.txt"

files = [file_pathA, file_pathB, file_pathC, my_file]

for path in files:
    matrix = read_payoff_matrix(path)
    print("\n", path.strip("Program3/data"))
    print("\nmatrix\n", matrix)
    print("\nTable")
    print_normal_form_table(matrix)
    print("\n Identify Strictly Dominated Strategies")
    identify_strictly_dominated_strategies(matrix)
    print("\n Identify Weakly Dominated Strategies")
    identify_weakly_dominated_strategies(matrix)
    print("\n Identify Pure Strategy Equilibria")
    identify_pure_strategy_equilibria(matrix)