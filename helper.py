#import numpy as np
import logging
from dataclasses import dataclass
from enum import Enum
from numpy import std, mean
from chess import engine, engine, Board, Move, pgn
import chess
from typing import List 

logging.getLogger().setLevel(logging.INFO) #to display also info in terminal

###############
#TYPES
###############
@dataclass(frozen=True)
class Colour(Enum):
    black = "b"
    white = "w"


###############
#FUNCS
###############

def engine_init() -> engine.SimpleEngine:
    'initializes stockfish engine'

    eng = engine.SimpleEngine.popen_uci("/usr/games/stockfish")
    logging.info(f"type(eng: {type(eng)}")

    return eng

def info_retrieval(board: Board, eng: engine.SimpleEngine) -> List[dict]:
    'infos from a board position, including eval at depth 15 and 5 variants'

    res = eng.analyse(board, chess.engine.Limit(depth=15), multipv=5)
    
    return res

def average_cp(cp_list: List[int]) -> float:
    'average of a list'

    return sum(cp_list) / len(cp_list)

def uci_moves_to_list(uci_moves: str) -> list:
    str_to_list = uci_moves.split(sep=" ")
    return str_to_list


def list_cp_score_to_int(info: List[dict]) -> List[int]:         
    'gets infos, returns list of cps' 

    list_cp_int = [var['score'].relative.score() for var in info]
    logging.info(f"cp_int: {list_cp_int}")
    return list_cp_int


def colour_from_fen(fen: str) -> Colour:
    colour_index = (fen.index("- -") - 2)
    colour = Colour(fen[colour_index])
    logging.info(f"colour: {colour}")
    return colour 

def evals_ordering(evals: list, colour: Colour) -> list:
    if colour == Colour.black:
        evals.reverse()
    logging.info(f"evals: {evals}")
    return evals


###############
#SAFENESS EVALUATION FUNCS
###############

def safeness_calculator_plain_difference(cp_list: List[int]) -> int:
    logging.info(f"cp_list: {cp_list}")

    plain_diff = cp_list[0] - cp_list[len(cp_list) - 1] 
    logging.info(f"plain_diff: {plain_diff}")

    return plain_diff


def safeness_calculator_unweighted(cp_list: List[int]) -> float:
    'calculates the ratio of cp of best move and average cp of its n variations, espressed in %.'

    logging.info(f"cp_list: {cp_list}")
    try:
        safeness_perc = round((average_cp(cp_list) / cp_list[0])  * 100, 2)  
    except ZeroDivisionError:
        safeness_perc = round((average_cp(cp_list) / 0.01)  * 100, 2) #fix

    logging.info(f"numerator; {average_cp(cp_list) / 0.01}")

    logging.info(f"safeness_perc: {safeness_perc}")
    return safeness_perc

def safeness_std(cp_list:List[int]) -> float:
    'calculates standard variation'

    standard_dev = std(cp_list)
    logging.info(f"standard_dev: {standard_dev}")
    return standard_dev

def safeness_cx_variance(cp_list:List[int]) -> float:
    'calculates coefficient of variance'

    standard_dev = std(cp_list)
    average = mean(cp_list)
    cx_variance = standard_dev / average 
    logging.info(f"standard_dev: {standard_dev}")
    logging.info(f"cx_variance: {cx_variance}")
    return cx_variance


def board_from_pgn_mainline_game(pgn: pgn.Game) -> Board:
    'returns board from a pgn mainline game'

    board = pgn.board()
    for move in pgn.mainline_moves():
        board.push(move)
    
    logging.info(f"board: {board}")
    return board


###############
#SUCCESSIVE EVAL FUNCS
###############

#def variation_from_analysis(infos: list, var_number: int, moves_number: int) -> List[Move]: #why doesn't it check the return type?
#    'selects a specific var from infos list. '
#
#    specific_var = infos[var_number]["pv"][moves_number + 1]
#    logging.info(f"specific_var: {specific_var}")
#    return specific_var

def variation_from_analysis(infos: list, var_number: int, number_of_moves: int) -> List[Move]: #why doesn't it check the return type?
    'selects a specific var from infos list. '

    specific_var = infos[var_number]["pv"][0 : number_of_moves]
    logging.info(f"specific_var: {specific_var}")    

    return specific_var

def std_avg_node_variation(variation: List[Move], game: pgn.Game, info: List[dict], eng: engine.SimpleEngine) -> int:
    '''
    adds a variation node from a list of moves
    
    P.S. should be broke up in two functions
    '''

    for m in variation:
        if "node" not in locals():
            node = game.add_variation(m)
        else:
            node = node.add_variation(m)
            board = node.board()
            logging.info(f"node.board(): {node.board()}")

            infos = info_retrieval(board = board, eng = eng)
            logging.info(f"infos: {infos}")

            cps = list_cp_score_to_int(infos)
            logging.info(f"cps: {cps}")

            std = safeness_std(cps)
            logging.info(f"std: {std}")

            
            
    

    return node


#def board_variation(board: Board, variation: variation_from_analysis) -> Board: #check if it works
#    'moves the board according to a variation'
#    
#    for move in variation:
#        board_w_variation = board.push_san(str(move))
#    logging.info(f"board_w_variation: {board_w_variation}")
#    logging.info(f"board: {board}")
#    return board 
