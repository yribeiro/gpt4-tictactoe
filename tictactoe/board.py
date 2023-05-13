
import copy
from typing import List


class TicTacToeBoard:
    """
    Represents a Tic-Tac-Toe board.
    """

    def __init__(self) -> None:
        self._history: List[str] = []
        self._board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    @property
    def board(self) -> List[List[str]]:
        """
        Returns:
            list: current board state.
        """
        return copy.deepcopy(self._board)
    
    @property
    def history(self) -> List[str]:
        """
        Returns:
            list: history of moves.
        """
        return copy.deepcopy(self._history)

    def check_move(self, move: tuple):
        """
        Check if a move is valid.

        Args:
            move (tuple): move to check.
        """
        assert len(move) == 2, "Invalid move. Must be in the format (<ROW>, <COL>)"
        assert move[0] in [1, 2, 3], "Invalid move. <ROW> must be between 1 and 3 inclusive."
        assert move[1] in [1, 2, 3], "Invalid move. <COL> must be between 1 and 3 inclusive."
        assert self._board[move[0]-1][move[1]-1] == " ", "Invalid move. Square is already occupied."

    def check_win(self, mark: str) -> bool:
        """
        Check if a player has won.

        Args:
            mark (str): mark to check.

        Returns:
            bool: True if player has won, False otherwise.
        """
        for i in range(3):
            if self._board[i][0] == mark and self._board[i][1] == mark and self._board[i][2] == mark:
                return True
            if self._board[0][i] == mark and self._board[1][i] == mark and self._board[2][i] == mark:
                return True
        if self._board[0][0] == mark and self._board[1][1] == mark and self._board[2][2] == mark:
            return True
        if self._board[0][2] == mark and self._board[1][1] == mark and self._board[2][0] == mark:
            return True
        return False

    def check_tie(self) -> bool:
        """
        Check if the game is a tie.

        Args:
            board (list): board state.

        Returns:
            bool: True if game is a tie, False otherwise.
        """
        for i in range(3):
            for j in range(3):
                if self._board[i][j] == " ":
                    return False
        return True

    def check_win_or_tie(self, mark: str) -> bool:
        """
        Check if a player has won or if the game is a tie.

        Args:
            board (list): board state.
            mark (str): mark to check.

        Returns:
            bool: True if player has won or if the game is a tie, False otherwise.
        """
        if self.check_win(mark):
            print(f"{mark} wins!")
            return True
        if self.check_tie():
            print("Tie!")
            return True
        return False
    
    def handle_move(self, mark: str, move: tuple):
        """
        Handle a move.

        Args:
            mark (str): Mark to place on the board.
            move (tuple): Move with x and y coordinates.
        """
        self._board[move[0]-1][move[1]-1] = mark
        self._history.append(f"{mark}: ({move[0]}, {move[1]})")

    def print_board(self):
        """
        Print the board.
        """
        print()
        print("Board:")
        for row in self._board:
            row_str = f" {row[0]} | {row[1]} | {row[2]} "
            print("-"*len(row_str))
            print(row_str)
        print("-"*len(row_str))
        print()

    def board_ascii(self) -> str:
        """
        Returns:
            str: board as ASCII art.
        """
        board = ""
        for row in self._board:
            row_str = f" {row[0]} | {row[1]} | {row[2]} "
            board += "-"*len(row_str) + "\n"
            board += row_str + "\n"
        board += "-"*len(row_str) + "\n"
        return board

