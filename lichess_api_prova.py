import requests
import numpy as np
import chess  
import logging

logging.getLogger().setLevel(logging.INFO) #to display also info in terminal

###############
#FUNCS
###############

def lichess_eval_extract(fen: str) -> dict:
    api_url = f"https://lichess.org/api/cloud-eval?fen={fen}&depth=22&multiPv=5"
    print(api_url)
    response = requests.get(api_url)
    print(response)
    # print(response.json())
    return response.json()
    
def response_unpacking(response: dict) -> dict:
    #takes the response dict with the various variations 
    parsed_dict = response["pvs"] 
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

###############
###############

fen = "8/6p1/2k4p/5p2/p1p5/P1K1P2P/1P4P1/8 b - - 1 48"

eval_test = lichess_eval_extract(fen)

board = chess.Board(fen)
logging.info(f"board: {board}")

json_response = response_unpacking(eval_test)

json_res_first = json_response[1]
print(f"json_res_first: {json_res_first}")

temp_res = total_cp_unweighted(json_res_first)
print(temp_res)

moves_list = uci_moves_to_list(json_res_first["moves"])
logging.info(f"moves_list: {moves_list}")

best_var = chess.Move.from_uci(moves_list[0])
logging.info(f"best_var: {best_var}")

board.push(best_var) #best_var
logging.info(f"board_2: {board}")

best_var_fen = board.fen()
logging.info(f"best_var_fen: {best_var_fen}")
