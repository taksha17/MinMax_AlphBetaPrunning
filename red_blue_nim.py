import argparse
import random

def eval_function(red, blue):
    """
    This function returns the evaluation of the current state of the game based on the number of red and blue marbles left.
    """
    return 2 * red + 3 * blue

def minimax(red, blue, depth, is_max_turn, alpha, beta, memo):
    # Check if the result for the current state is already in the memoization table.
    state = (red, blue, depth, is_max_turn)
    if state in memo:
        return memo[state]

    # Perform a depth-limited MinMax search with alpha-beta pruning to determine the best move for the computer player.
    if red == 0 or blue == 0:
        value = eval_function(red, blue)
    elif depth == 0:
        value = 0
    elif is_max_turn:
        best_value = float('-inf')
        for i in range(2):
            if i == 0 and red > 0:
                value = minimax(red - 1, blue, depth - 1, False, alpha, beta, memo)
            elif i == 1 and blue > 0:
                value = minimax(red, blue - 1, depth - 1, False, alpha, beta, memo)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
    else:
        best_value = float('inf')
        for i in range(2):
            if i == 0 and red > 0:
                value = minimax(red - 1, blue, depth - 1, True, alpha, beta, memo)
            elif i == 1 and blue > 0:
                value = minimax(red, blue - 1, depth - 1, True, alpha, beta, memo)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break

    # Store the result in the memoization table and return the value.
    memo[state] = value
    return value

def computer_move(red, blue, depth, memo={}):
    # Determine the best move for the computer player using the MinMax algorithm with alpha-beta pruning and memoization.
    state = (red, blue, depth)
    if state in memo:
        return memo[state]

    print("Computer is taking their turn.")
    best_value = float('-inf')
    best_pile = None
    for i in range(2):
        if i == 0 and red > 0:
            value = minimax(red - 1, blue, depth, False, float('-inf'), float('inf'), memo)
        elif i == 1 and blue > 0:
            value = minimax(red, blue - 1, depth, False, float('-inf'), float('inf'), memo)
        if value > best_value:
            best_value = value
            best_pile = i
    if best_pile == 0:
        red -= 1
        print("Computer now takes a red marble.")
    elif best_pile == 1:
        blue -= 1
        print("Computer now takes a blue marble.")

    memo[state] = (red, blue)
    return red, blue

def human_move(red, blue):
    """
    Prompt the human player for their move and perform it.
    """
    pile = input("Your turn. Choose a pile to remove a marble from (red/blue): ")
    while pile not in ["red", "blue"]:
        pile = input("Invalid input. Choose a pile to remove a marble from (red/blue): ")
    if pile == "red" and red > 0:
        red -= 1
    elif pile == "blue" and blue > 0:
        blue -= 1
    return red, blue


def play_game(red, blue, depth, first_player):
    """
    Starts a game of Red-Blue Nim.
    """
    print("Starting game with red={}, blue={}, first_player={}, depth={}".format(red, blue, first_player, depth))
    if first_player == "human":
        turn = 0
    else:
        turn = 1
    while red > 0 and blue > 0:
        if turn % 2 == 0:
            red, blue = human_move(red, blue)
        else:
            red, blue = computer_move(red, blue, depth)
        print("Current state: red = {}, blue = {}".format(red, blue))
        turn += 1
    if red == 0:
        score = 3 * blue
        print("You win! Final score: {}".format(score))
    elif blue == 0:
        score = 2 * red
        print("Computer wins! Final score: {}".format(score))



def main():
    parser = argparse.ArgumentParser(description='Red-Blue Nim game.')
    parser.add_argument('--red', type=int, default=3, help='Number of red marbles to start the game with.')
    parser.add_argument('--blue', type=int, default=4, help='Number of blue marbles to start the game with.')
    parser.add_argument('--depth', type=int, default=3, help='The depth of the search tree for the computer player.')
    parser.add_argument('--firstplayer', type=str, choices=['human', 'computer'], default='human', help='The player to take the first turn.')
    args = parser.parse_args()

    red = args.red
    blue = args.blue
    depth = args.depth
    first_player = args.firstplayer

    # Start the game with the specified settings.
    play_game(red, blue, depth, first_player)


if __name__ == "__main__":
    main()


