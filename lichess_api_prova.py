from helper import variation_from_analysis, board_variation, safeness_std, evals_ordering, colour_from_fen, cp_score_to_int  
from helper import Colour
from chess import engine, Board, pgn
import chess
import logging

if __name__ == "__main__":

    engine = engine.SimpleEngine.popen_uci("/usr/games/stockfish")

    with open("test_pgn.txt") as t_pgn:
        test_pgn = chess.pgn.read_game(t_pgn)

    test_fen = "8/k7/1p5p/p3P1P1/b7/8/5KP1/8 w - - 0 49"
    draw_fen = "8/7k/8/7P/8/8/3K4/8 w - - 0 1"
    king_gambit_fen = "rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"

    board = Board(test_fen)
    logging.info(f"board: {board}")
    game = pgn.Game()
    info = engine.analyse(board, chess.engine.Limit(depth=15), multipv=5)
    various_evals = [cp_score_to_int(var) for var in info]
    colour = colour_from_fen(test_fen)
    ordered_evals = evals_ordering(various_evals, colour)
    logging.info(f"ordered_evals: {ordered_evals}")
    safeness_std_res = safeness_std(ordered_evals)
    var_1 = variation_from_analysis(info, 1, 1)
    board_variation_1 = board_variation(board, var_1) 
    variation = pgn.GameNode.add_variation(board, move=board_variation_1)
    logging.info(variation)

    engine.quit()

