#import numpy as np
import logging
from dataclasses import dataclass
from enum import Enum
from numpy import std, mean
from chess import engine, Board, Move

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

def average_cp(cp_list: list) -> int:
    #average of a list

    return sum(cp_list) / len(cp_list)

def uci_moves_to_list(uci_moves: str) -> list:
    str_to_list = uci_moves.split(sep=" ")
    return str_to_list


def cp_score_to_int(variant: dict) -> int:
    #gets a sf variant, returns cp in int 
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

def safeness_calculator_plain_difference(cp_list: list) -> int:
    logging.info(f"cp_list: {cp_list}")

    plain_diff = cp_list[0] - cp_list[len(cp_list) - 1] 
    logging.info(f"plain_diff: {plain_diff}")

    return plain_diff


def safeness_calculator_unweighted(cp_list: list) -> int:
    #calculates the ratio of cp of best move and average cp of its n variations, espressed in %.

    logging.info(f"cp_list: {cp_list}")
    try:
        safeness_perc = round((average_cp(cp_list) / cp_list[0])  * 100, 2)  
    except ZeroDivisionError:
        safeness_perc = round((average_cp(cp_list) / 0.01)  * 100, 2) #fix

    logging.info(f"numerator; {average_cp(cp_list) / 0.01}")

    logging.info(f"safeness_perc: {safeness_perc}")
    return safeness_perc

def safeness_cx_variance(cp_lint:list[int]) -> float:
    standard_dev = std(cp_lint)
    average = mean(cp_lint)
    cx_variance = standard_dev / average 
    logging.info(f"standard_dev: {standard_dev}")
    logging.info(f"cx_variance: {cx_variance}")
    return cx_variance


###############
#SUCCESSIVE EVALS FUNCS
###############

def variation_from_info(infos: list, var_number: int) -> list[Move]:
    specific_var = infos[var_number]["pv"]
    logging.info(f"specific_var: {specific_var}")
    return specific_var

def board_variation(board: Board, variation: list) -> Board: #check if it works
    board_w_variation = Board.push_san(variation)
    return board_w_variation