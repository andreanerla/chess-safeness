#import numpy as np
import logging
from dataclasses import dataclass
from enum import Enum
from numpy import std, mean
from chess import engine, Board, Move
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

def average_cp(cp_list: List[int]) -> float:
    'average of a list'

    return sum(cp_list) / len(cp_list)

def uci_moves_to_list(uci_moves: str) -> list:
    str_to_list = uci_moves.split(sep=" ")
    return str_to_list


def cp_score_to_int(variant: dict) -> int:
    'gets a sf variant, returns cp in int' 
    cp_int = variant['score'].relative.score()
    return cp_int


def colour_from_fen(fen: str) -> Colour:
    colour_index = (fen.index("- -") - 2)
    colour = Colour(fen[colour_index])
    logging.info(f"colour: {colour}")
    return colour 

def evals_ordering(evals: list, colour: Colour) -> list:
    if colour == Colour.black:
        evals.reverse()
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

def board_variation(board: Board, variation: List[Move]) -> Board: #check if it works
    'moves the board according to a variation'
    
    for move in variation:
        board_w_variation = board.push_san(str(move))
    logging.info(f"board_w_variation: {board_w_variation}")
    logging.info(f"board: {board}")
    return board 