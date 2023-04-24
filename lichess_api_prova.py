import requests
import numpy as np

def lichess_eval_extract(fen: str) -> dict:
    api_url = f"https://lichess.org/api/cloud-eval?fen={fen}&depth=22&multiPv=5"
    print(api_url)
    response = requests.get(api_url)
    print(response)
    # print(response.json())
    return response.json()
    
def response_unpacking(response: dict) -> dict:
    parsed_dict = response["pvs"] 
    return parsed_dict

eval_test = lichess_eval_extract("8/6p1/2k4p/5p2/p1p5/P1K1P2P/1P4P1/8 b - - 1 48")

json_response = response_unpacking(eval_test)
print(f"json_response: {json_response}")

json_res_first = json_response[1]
print(f"json_response_first: {json_res_first}")

# for k,v in response.items():
    # print(f"key: {k}, value: {v}")

def unweighted_algo(response_json: list[dict] | dict) -> dict:
    total_cp = 0
 
    if isinstance(response_json, dict):
        return response_json["cp"]
    else:
        for d in response_json:
            total_cp += d["cp"]

    return total_cp 


temp_res = unweighted_algo(json_res_first)
print(temp_res)
