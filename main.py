from typing import Tuple
from langchain import OpenAI, LLMChain
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate
import dotenv
from tictactoe.templates import TEMPLATE

def check_move(board: list, move: tuple):
    """
    Check if a move is valid.

    Args:
        board (list): board state.
        move (tuple): move to check.
    """
    assert len(move) == 2, "Invalid move. Must be in the format (<ROW>, <COL>)"
    assert move[0] in [1, 2, 3], "Invalid move. <ROW> must be between 1 and 3 inclusive."
    assert move[1] in [1, 2, 3], "Invalid move. <COL> must be between 1 and 3 inclusive."
    assert board[move[0]-1][move[1]-1] == " ", "Invalid move. Square is already occupied."

def check_win(board: list, mark: str) -> bool:
    """
    Check if a player has won.

    Args:
        board (list): board state.
        mark (str): mark to check.

    Returns:
        bool: True if player has won, False otherwise.
    """
    for i in range(3):
        if board[i][0] == mark and board[i][1] == mark and board[i][2] == mark:
            return True
        if board[0][i] == mark and board[1][i] == mark and board[2][i] == mark:
            return True
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        return True
    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        return True
    return False

def check_tie(board: list) -> bool:
    """
    Check if the game is a tie.

    Args:
        board (list): board state.

    Returns:
        bool: True if game is a tie, False otherwise.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True

def check_win_or_tie(board: list, mark: str) -> bool:
    """
    Check if a player has won or if the game is a tie.

    Args:
        board (list): board state.
        mark (str): mark to check.

    Returns:
        bool: True if player has won or if the game is a tie, False otherwise.
    """
    if check_win(board, mark):
        print(f"{mark} wins!")
        return True
    if check_tie(board):
        print("Tie!")
        return True
    return False

def get_human_move_from_input(board: list, tries: int = 1) -> Tuple[int, int]:
    """
    Get a move from the user.

    Args:
        board (list): board state.
        tries (int, optional): Number of tries so far. Defaults to 1.

    Raises:
        Exception: Exceeded maximum number of tries.

    Returns:
        Tuple[int, int]: move with x and y coordinates.
    """
    if tries > 3:
        raise Exception("Exceeded maximum number of tries.")

    try:
        human_move = input("Enter your move (<row>, <col>): ")
        human_move = human_move.split(",")
        human_move = tuple([int(x.strip()) for x in human_move])
        check_move(board, human_move)
    except Exception as e:
        print(f"Invalid move ({human_move}). Try again. (Attempt {tries+1}/3)")
        human_move = get_human_move_from_input(board, tries=tries+1)
        
    return human_move

def get_bot_move_from_chain(chain: LLMChain, history: list, board: list, botmark: str, oppmark: str, tries: int = 1) -> Tuple[int, int]:#
    """
    Get a move from the bot.

    Args:
        chain (LLMChain): Langchain chain containing the model.
        history (list): History of moves on the board.
        board (list): Board state.
        botmark (str): Mark for the tic tac toe bot.
        oppmark (str): Mark for the opponent.
        tries (int, optional): Number of tries so far. Defaults to 1.

    Raises:
        Exception: Unable to find a valid move.

    Returns:
        Tuple[int, int]: move with x and y coordinates.
    """
    print("-"*50)
    print(f"Bot is thinking... (Attempt {tries+1}/3)")
    
    if tries > 3:
        raise Exception("Unable to find a valid move.")
    
    bot_move = chain.run(history=str(history), board=str(board), botmark=botmark, oppmark=oppmark)
    bot_move = eval(bot_move)
    try:
        check_move(board, bot_move)
    except Exception as e:
        print(f"Invalid move ({bot_move}). Bot trying again. (Attempt {tries+1}/3)")
        bot_move = get_bot_move_from_chain(chain, history, board, botmark, oppmark, tries=tries+1)

    print(f"Bot move: {bot_move}")
    print("-"*50)
    print()
    return bot_move

def handle_move(history: list, board: list, mark: str, move: tuple):
    """
    Handle a move.

    Args:
        history (list): History of the board moves.
        board (list): Board state.
        mark (str): Mark to place on the board.
        move (tuple): Move with x and y coordinates.
    """
    board[move[0]-1][move[1]-1] = mark
    history.append(f"{mark}: ({move[0]}, {move[1]})")

def get_human_and_bot_mark()-> Tuple[str, str]:
    """
    Get the human and bot marks.

    Returns:
        Tuple[str, str]: human and bot marks.
    """
    human_mark = input("Enter your mark (X or O): ")
    human_mark = human_mark.upper()
    assert human_mark in ["X", "O"], "Invalid mark. Must be either X or O."
    bot_mark = "X" if human_mark == "O" else "O"
    return human_mark, bot_mark

def print_board(board: list):
    """
    Print the board.

    Args:
        board (list): board state.
    """
    print()
    print("Board:")
    for row in board:
        row_str = f" {row[0]} | {row[1]} | {row[2]} "
        print("-"*len(row_str))
        print(row_str)
    print("-"*len(row_str))
    print()


if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    
    prompt = SystemMessagePromptTemplate.from_template(TEMPLATE)
    chat_prompt = ChatPromptTemplate.from_messages([prompt])

    llm = OpenAI(temperature=0.9)
    chain = LLMChain(llm=llm, prompt=chat_prompt)

    history = []
    board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]

    human_mark, bot_mark = get_human_and_bot_mark()

    if human_mark == "X":
        move = get_human_move_from_input(board=board)
        handle_move(history, board, human_mark, move)

    print_board(board)

    game_over = False
    while not game_over:
        bot_move = get_bot_move_from_chain(chain, history, board, bot_mark, human_mark)
        handle_move(history, board, bot_mark, bot_move)

        print_board(board)

        if check_win_or_tie(board, bot_mark):
            game_over = True
            break
        
        human_move = get_human_move_from_input(board=board)
        handle_move(history, board, human_mark, human_move)

        print_board(board)

        if check_win_or_tie(board, human_mark):
            game_over = True
            break
