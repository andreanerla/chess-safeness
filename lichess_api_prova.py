import requests
#import numpy as np
import asyncio
import chess  
import chess.engine
import logging
from dataclasses import dataclass

logging.getLogger().setLevel(logging.INFO) #to display also info in terminal

###############
#TYPES
###############
@dataclass
class Colour:
    colour: str = "black", "white"  


###############
#FUNCS
###############

def average_cp(cp_list: list) -> int:
    #average of a list

    return sum(cp_list) / len(cp_list)


def safeness_calculator_unweighted(cp_list: list, colour: Colour) -> int:
    #calculates the ratio of cp of best move and average cp of its n variations, espressed in %.
    if colour == "black":
        cp_list.reverse()

    logging.info(f"cp_list: {cp_list}")

    safeness_perc = round((average_cp(cp_list) / cp_list[0])  * 100, 2)  
    logging.info(f"safeness_perc: {safeness_perc}")
    return safeness_perc


def uci_moves_to_list(uci_moves: str) -> list:
    str_to_list = uci_moves.split(sep=" ")
    return str_to_list


def cp_score_to_int(variant: dict) -> int:
    #gets a sf variant, returns cp in int 
    cp_int = variant['score'].relative.score()
    return cp_int

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

test_fen = "8/k5p1/1p6/p3P1PP/b7/8/5KP1/8 b - - 0 48"

board = chess.Board(test_fen)
info = engine.analyse(board, chess.engine.Limit(depth=10), multipv=5)

various_evals = [cp_score_to_int(var) for var in info]

safeness_test = safeness_calculator_unweighted(various_evals, colour="black")

engine.quit()

