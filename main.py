from typing import Tuple
from langchain import OpenAI, LLMChain
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate
import dotenv
from tictactoe.templates import TEMPLATE
from tictactoe.board import TicTacToeBoard
import streamlit as st


def get_human_move_from_input(board: TicTacToeBoard, tries: int = 1) -> Tuple[int, int]:
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
        board.check_move(human_move)
    except Exception as e:
        print(f"Invalid move ({human_move}). Try again. (Attempt {tries+1}/3)")
        human_move = get_human_move_from_input(board, tries=tries+1)
        
    return human_move

def get_bot_move_from_chain(chain: LLMChain, board: TicTacToeBoard, botmark: str, oppmark: str, tries: int = 1) -> Tuple[int, int]:#
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
    
    bot_move = chain.run(history=str(board.history), board=str(board.board), botmark=botmark, oppmark=oppmark)
    bot_move = eval(bot_move)
    try:
        board.check_move(bot_move)
    except Exception as e:
        print(f"Invalid move ({bot_move}). Bot trying again. (Attempt {tries+1}/3)")
        bot_move = get_bot_move_from_chain(chain, board, botmark, oppmark, tries=tries+1)

    print(f"Bot move: {bot_move}")
    print("-"*50)
    print()
    return bot_move

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


def run_console_app(chain: LLMChain, board: TicTacToeBoard = TicTacToeBoard()):
    human_mark, bot_mark = get_human_and_bot_mark()

    if human_mark == "X":
        move = get_human_move_from_input(board=board)
        board.handle_move(mark=human_mark, move=move)

    board.print_board()

    game_over = False
    while not game_over:
        bot_move = get_bot_move_from_chain(chain, board, bot_mark, human_mark)
        board.handle_move(bot_mark, bot_move)

        board.print_board()

        if board.check_win_or_tie(bot_mark):
            game_over = True
            break
        
        human_move = get_human_move_from_input(board=board)
        board.handle_move(human_mark, human_move)

        board.print_board()

        if board.check_win_or_tie(human_mark):
            game_over = True
            break

def run_web_app(chain: LLMChain):
    if "board" not in st.session_state:
        st.session_state["board"] = TicTacToeBoard()

    st.header("Tic Tac Toe with ChatGPT")
    st.text("You are playing against a bot that uses ChatGPT to play Tic Tac Toe.")

    human_mark = st.text_input("Enter your mark (X or O): ")

    if human_mark != "":
        human_mark = human_mark.upper()
        assert human_mark in ["X", "O"], "Invalid mark. Must be either X or O."
        bot_mark = "X" if human_mark == "O" else "O"
        st.text(f"Your mark: '{human_mark}', Bot mark: '{bot_mark}'")

        if human_mark == "X":
            human_move = st.text_input("You are playing first. Enter your move in the format <row>, <col>.")
        else:
            # bot plays first
            bot_move = get_bot_move_from_chain(chain, st.session_state["board"], bot_mark, human_mark)
            st.session_state["board"].handle_move(bot_mark, bot_move)
            st.text(f"Bot move: {bot_move}")
            st.write(st.session_state["board"].board_ascii())

            human_move = st.text_input("You are playing second. Enter your move in the format <row>, <col>.")
            
        if human_move != "":
            human_move = human_move.split(",")
            human_move = tuple([int(x.strip()) for x in human_move])
            st.session_state["board"].check_move(human_move)
            st.session_state["board"].handle_move(human_mark, human_move)

            # bot plays second
            bot_move = get_bot_move_from_chain(chain, st.session_state["board"], bot_mark, human_mark)
            st.session_state["board"].handle_move(bot_mark, bot_move)
            st.text(f"Bot move: {bot_move}")
            st.text(st.session_state["board"].board_ascii())

if __name__ == "__main__":
    dotenv.load_dotenv("./.env")
    
    # create AI related objects
    prompt = SystemMessagePromptTemplate.from_template(TEMPLATE)
    chat_prompt = ChatPromptTemplate.from_messages([prompt])
    llm = OpenAI(temperature=0.9)
    chain = LLMChain(llm=llm, prompt=chat_prompt)

    # start application
    run_web_app(chain)
    
