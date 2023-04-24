def lichess_eval_extract(fen: str) -> dict:
    import requests
    api_url = f"https://lichess.org/api/cloud-eval?fen={fen}&depth=22&multiPv=5"
    print(api_url)
    response = requests.get(api_url)
    print(response)
    print(response.json())
    return response.json()
    

lichess_eval_extract("8/6p1/2k4p/5p2/p1p5/P1K1P2P/1P4P1/8 b - - 1 48")
