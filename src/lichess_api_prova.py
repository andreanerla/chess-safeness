from helper import engine_init, variation_from_analysis, safeness_std, evals_ordering, colour_from_fen, list_cp_score_to_int, board_from_pgn_mainline_game, std_from_board, info_retrieval, game_add_variation
from chess import Board
import chess 

if __name__ == "__main__":

    eng = engine_init()
    sharp_fen = "8/k7/1p5p/p3P1P1/b7/8/5KP1/8 w - - 0 49"
    draw_fen = "8/7k/8/7P/8/8/3K4/8 w - - 0 1"
    king_gambit_fen = "rnbqkbnr/pppp1ppp/8/4p3/4PP2/8/PPPP2PP/RNBQKBNR b KQkq - 0 2"
    ruy_lopez_fen = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"

    board = Board()
    board.set_fen(king_gambit_fen)
    game = chess.pgn.Game()
    game.setup(board = board)
    #board = board_from_pgn_mainline_game(pgn = game)    
    info = info_retrieval(board = board, eng = eng)
    various_evals = list_cp_score_to_int(info = info) 
    colour = colour_from_fen(sharp_fen)
    ordered_evals = evals_ordering(various_evals, colour)
    safeness_std_res = safeness_std(ordered_evals)
    var_1 = variation_from_analysis(info, 1, 6)
    #node_var_1 = std_avg_node_variation(variation = var_1, game = game, infos = info, eng = eng)
    board_var_1 = game_add_variation(variation = var_1, game = game, infos = info, eng = eng) 
    
    eng.quit()

