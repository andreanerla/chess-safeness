#import numpy as np
import logging
from dataclasses import dataclass
from enum import Enum

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


def safeness_calculator_plain_difference(cp_list: list, colour: Colour) -> int:
    logging.info(f"cp_list: {cp_list}")

    plain_diff = cp_list[0] - cp_list[len(cp_list) - 1] 
    logging.info(f"plain_diff: {plain_diff}")

    return plain_diff


def safeness_calculator_unweighted(cp_list: list, colour: Colour) -> int:
    #calculates the ratio of cp of best move and average cp of its n variations, espressed in %.

    logging.info(f"cp_list: {cp_list}")
    try:
        safeness_perc = round((average_cp(cp_list) / cp_list[0])  * 100, 2)  
    except ZeroDivisionError:
        safeness_perc = round((average_cp(cp_list) / 0.01)  * 100, 2) #fix

    logging.info(f"numerator; {average_cp(cp_list) / 0.01}")

    logging.info(f"safeness_perc: {safeness_perc}")
    return safeness_perc


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