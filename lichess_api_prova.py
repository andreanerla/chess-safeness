import requests
#import numpy as np
import asyncio
import chess  
import chess.engine
import logging

logging.getLogger().setLevel(logging.INFO) #to display also info in terminal

###############
#FUNCS
###############
    
def response_unpacking(response: dict) -> dict:
    #takes the response dict with the various variations 
    parsed_dict = response["pv"] 
    return parsed_dict

def total_cp_unweighted(response_json: list[dict] | dict) -> dict:
    #calculates the total cp of a certain move with its n variations.
     
    total_cp = 0
 
    if isinstance(response_json, dict):
        return response_json["cp"]
    else:
        for d in response_json:
            total_cp += d["cp"]

    return total_cp 

def uci_moves_to_list(uci_moves: str) -> list:
    str_to_list = uci_moves.split(sep=" ")
    return str_to_list


def cp_score_to_int(cp: str) -> int:
    pass


engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

test_fen = "8/k5p1/1p6/p3P1PP/b7/8/5KP1/8 b - - 0 48"

board = chess.Board(test_fen)
info = engine.analyse(board, chess.engine.Limit(depth=10), multipv=5)

#for variant in info:
#    logging.info(f"Score:{variant}")

info_score = info[1]['score'].relative.score()
logging.info(f"json_res_first: {info_score}")
logging.info(type(info_score))

engine.quit()
