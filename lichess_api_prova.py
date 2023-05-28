from helper import engine_init, variation_from_analysis, safeness_std, evals_ordering, colour_from_fen, list_cp_score_to_int, board_from_pgn_mainline_game, std_avg_node_variation, info_retrieval  
from helper import Colour
from chess import engine, Board, pgn
import chess 

if __name__ == "__main__":

    eng = engine_init()
    game = chess.pgn.Game()

    test_fen = "8/k7/1p5p/p3P1P1/b7/8/5KP1/8 w - - 0 49"
    draw_fen = "8/7k/8/7P/8/8/3K4/8 w - - 0 1"
    king_gambit_fen = "rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"

    board = board_from_pgn_mainline_game(pgn = game)    
    info = info_retrieval(board = board, eng = eng)
    various_evals = list_cp_score_to_int(info = info) 
    colour = colour_from_fen(test_fen)
    ordered_evals = evals_ordering(various_evals, colour)
    safeness_std_res = safeness_std(ordered_evals)
    var_1 = variation_from_analysis(info, 1, 6)
    node_var_1 = std_avg_node_variation(variation = var_1, game = game, info = info, eng = eng)


    eng.quit()

