import itertools

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

    # Get the header titles
    col_headers = [chr(ord('Z') - i) for i in range(num_cols_player2)]
    col_headers.reverse()

    row_letters = [chr(ord('A') + i) for i in range(num_rows_player1)]

    pure_equilibria = []

    for i in range(num_rows_player1):
        for j in range(num_rows_player2):
            try:
                # Check if (i, j) is a Nash equilibrium
                is_nash_equilibrium = all(
                    matrix[0][i][k] >= matrix[0][j][k] for k in range(num_cols_player1)
                ) and all(
                    matrix[1][k][i] >= matrix[1][k][j] for k in range(num_rows_player2)
                )

                if is_nash_equilibrium:
                    pure_equilibria.append((i, j))
            except IndexError:
                print("IndexError occurred. Matrix:", matrix)
                raise

    for equilibrium in pure_equilibria:
        print(f"Player 1 chooses strategy {row_letters[equilibrium[0]]}, Player 2 chooses strategy {col_headers[equilibrium[1]]}")

    return pure_equilibria

def identify_pareto_optimal_solutions(matrix):
    num_rows_player1 = len(matrix[0])
    num_cols_player1 = len(matrix[0][0])

    num_rows_player2 = len(matrix[1])
    num_cols_player2 = len(matrix[1][0])

        # Get the header titles
    col_headers = []
    for i in range(num_cols_player1):
        col_headers.append(chr(ord('Z') - i))
    col_headers.reverse()

    row_letters = []
    for i in range(num_rows_player1):
        row_letters.append(chr(ord('A') + i))
    
    pareto_optimal_solutions = []

    for i in range(num_rows_player1):
        for j in range(num_rows_player2):
            is_pareto_optimal = all(
                matrix[0][i][k] >= matrix[0][j][k] for k in range(num_cols_player1)
            ) and all(
                matrix[1][k][i] >= matrix[1][k][j] for k in range(num_rows_player2)
            )

            if is_pareto_optimal:
                pareto_optimal_solutions.append((i, j))

    for solution in pareto_optimal_solutions:
        print(f"Pareto optimal solution: Player 1 chooses strategy {row_letters[solution[0]]}, Player 2 chooses strategy {col_headers[solution[1]]}")

    return pareto_optimal_solutions

def identify_minimax_strategies(matrix):
    num_rows_player1 = len(matrix[0])
    num_cols_player1 = len(matrix[0][0])

    num_rows_player2 = len(matrix[1])
    num_cols_player2 = len(matrix[1][0])
    
    # Get the header titles
    col_headers = []
    for i in range(num_cols_player1):
        col_headers.append(chr(ord('Z') - i))
    col_headers.reverse()

    row_letters = []
    for i in range(num_rows_player1):
        row_letters.append(chr(ord('A') + i))

    minimax_strategies_player1 = []
    minimax_strategies_player2 = []

    # Identify minimax strategy for Player 1
    for i in range(num_rows_player1):
        max_payoff_player1 = max(matrix[0][i][k] for k in range(num_cols_player1))
        minimax_strategies_player1.append((i, max_payoff_player1))

    # Identify minimax strategy for Player 2
    for j in range(num_rows_player2):
        max_payoff_player2 = max(matrix[1][k][j] for k in range(num_rows_player2))
        minimax_strategies_player2.append((j, max_payoff_player2))

    # Print results
    print("Minimax strategy for Player 1:")
    for strategy in minimax_strategies_player1:
        print(f"Player 1 chooses strategy {row_letters[strategy[0]]}, ensuring a minimum payoff of {strategy[1]} for Player 1.")

    print("\nMinimax strategy for Player 2:")
    for strategy in minimax_strategies_player2:
        print(f"Player 2 chooses strategy {col_headers[strategy[0]]}, ensuring a minimum payoff of {strategy[1]} for Player 2.")

    return minimax_strategies_player1, minimax_strategies_player2

def identify_maximin_strategies(matrix):
    num_rows_player1 = len(matrix[0])
    num_cols_player1 = len(matrix[0][0])

    num_rows_player2 = len(matrix[1])
    num_cols_player2 = len(matrix[1][0])

        # Get the header titles
    col_headers = []
    for i in range(num_cols_player1):
        col_headers.append(chr(ord('Z') - i))
    col_headers.reverse()

    row_letters = []
    for i in range(num_rows_player1):
        row_letters.append(chr(ord('A') + i))
    
    maximin_strategies_player1 = []
    maximin_strategies_player2 = []

    # Identify maximin strategy for Player 1
    for i in range(num_rows_player1):
        min_payoff_player1 = min(matrix[0][i][k] for k in range(num_cols_player1))
        maximin_strategies_player1.append((i, min_payoff_player1))

    # Identify maximin strategy for Player 2
    for j in range(num_rows_player2):
        min_payoff_player2 = min(matrix[1][k][j] for k in range(num_rows_player2))
        maximin_strategies_player2.append((j, min_payoff_player2))

    # Print results
    print("Maximin strategy for Player 1:")
    for strategy in maximin_strategies_player1:
        print(f"Player 1 chooses strategy {row_letters[strategy[0]]}, ensuring a payoff of at least {strategy[1]} for Player 1.")

    print("\nMaximin strategy for Player 2:")
    for strategy in maximin_strategies_player2:
        print(f"Player 2 chooses strategy {col_headers[strategy[0]]}, ensuring a payoff of at least {strategy[1]} for Player 2.")

    return maximin_strategies_player1, maximin_strategies_player2

def save_strategies(matrix, strategy_function):
    return strategy_function(matrix)

def experiment_with_strategies(matrix, player1_strategies, player2_strategies, player1_title, player2_title):
    num_rows_player1 = len(matrix[0])
    num_cols_player2 = len(matrix[1][0])

    col_headers = [chr(ord('Z') - i) for i in range(num_cols_player2)]
    col_headers.reverse()

    row_letters = [chr(ord('A') + i) for i in range(num_rows_player1)]

    # Iterate through all combinations of strategies and print results
    for player1_strategy_index, player2_strategy_index in itertools.product(player1_strategies, player2_strategies):
        # Ensure that player1_strategy_index and player2_strategy_index are integers
        player1_strategy_index = player1_strategy_index[0] if isinstance(player1_strategy_index, tuple) else player1_strategy_index
        player2_strategy_index = player2_strategy_index[0] if isinstance(player2_strategy_index, tuple) else player2_strategy_index

        # Print the title of where each player got their strategy
        print(f"\nExperimenting with strategies:")
        print(f"Player 1 strategy ({player1_title}): {row_letters[player1_strategy_index]}")
        print(f"Player 2 strategy ({player2_title}): {col_headers[player2_strategy_index]}")

        # Calculate payoffs for the chosen strategies
        payoff_player1 = matrix[0][player1_strategy_index][player2_strategy_index]
        payoff_player2 = matrix[1][player1_strategy_index][player2_strategy_index]

        # Print the resulting payoffs
        print(f"Payoff for Player 1: {payoff_player1}")
        print(f"Payoff for Player 2: {payoff_player2}")

def main():
    
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
        pure_strategy_equilibria = save_strategies(matrix, identify_pure_strategy_equilibria)
        print("\nIdentify Pareto Optimal Solutions")
        pareto_optimal_solutions = save_strategies(matrix, identify_pareto_optimal_solutions)
        print("\nIdentify Minimax Strategies")
        minimax_strategies_player1, minimax_strategies_player2 = save_strategies(matrix, identify_minimax_strategies)
        print("\nIdentify Maximin Strategies")
        maximin_strategies_player1, maximin_strategies_player2 = save_strategies(matrix, identify_maximin_strategies)
        
        strategy_combinations = [
        (pure_strategy_equilibria, pure_strategy_equilibria, "pure_strategy_equilibria", "pure_strategy_equilibria"),
        (pure_strategy_equilibria, pareto_optimal_solutions, "pure_strategy_equilibria", "pareto_optimal_solutions"),
        (pure_strategy_equilibria, minimax_strategies_player2, "pure_strategy_equilibria", "minimax_strategies_player2"),
        (pure_strategy_equilibria, maximin_strategies_player2, "pure_strategy_equilibria", "maximin_strategies_player2"),
        (pareto_optimal_solutions, pure_strategy_equilibria, "pareto_optimal_solutions", "pure_strategy_equilibria"),
        (pareto_optimal_solutions, pareto_optimal_solutions, "pareto_optimal_solutions", "pareto_optimal_solutions"),
        (pareto_optimal_solutions, minimax_strategies_player2, "pareto_optimal_solutions", "minimax_strategies_player2"),
        (pareto_optimal_solutions, maximin_strategies_player2, "pareto_optimal_solutions", "maximin_strategies_player2"),
        (minimax_strategies_player1, pure_strategy_equilibria, "minimax_strategies_player1", "pure_strategy_equilibria"),
        (minimax_strategies_player1, minimax_strategies_player2, "minimax_strategies_player1", "minimax_strategies_player2"),
        (maximin_strategies_player1, pure_strategy_equilibria, "maximin_strategies_player1", "pure_strategy_equilibria"),
        (maximin_strategies_player1, pareto_optimal_solutions, "maximin_strategies_player1", "pareto_optimal_solutions"),
        (maximin_strategies_player1, minimax_strategies_player2, "maximin_strategies_player1", "minimax_strategies_player2"),
        (maximin_strategies_player1, maximin_strategies_player2, "maximin_strategies_player1", "maximin_strategies_player2"),
        ]
        
        for player1_strategies, player2_strategies, player1_title, player2_title in strategy_combinations:
            experiment_with_strategies(matrix, player1_strategies, player2_strategies, player1_title, player2_title)
            
main()