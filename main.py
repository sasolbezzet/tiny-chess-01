import os, sys, json, urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit(1)

def post(path, body):
    req = urllib.request.Request(
        ENV_URL + path,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req) as res:
        return json.load(res)

BOOK = {k: v.split() for k, v in [x.split(":", 1) for x in (
    "1:g1f3 d1c2 f1d3 f3g5 d3h7 h2h4 h4g5 h7g8 c2h7|"
    "2:c8d7 b8d7 a7a6 g7g6 f8g7 a8c8 e8g8 d7e5 c8c3 f6e4 h7g6 d8c8 d6d5 c8g4 e5f3 g4f3 g7e5 f3g4 g4h3 e5h2 h2f4 f4e3 h3e3 e3g3 g3f2|"
    "3:d2d4 c3d4 c1d2 d2b4 c4f7 d1b3 f3e5 b3b4 b4b3 e1e2 b3d5 d5e6 e6f7|"
    "4:e4d6 f8e7 d7c6 d6f5 e8g8 c6c5 f5h4 e7d6 f7f5 f5g4 c7d6 d8f6 f6g6 c8f5 f5c2 g6e4 g4f3 f3f2 f8f2 e4f3 f3g2|"
    "5:e2e4 f1e2 c3a4 e2c4 c4e6 e1g1 f1e1 d1c2 c1g5 g5f6 e1e5 a4c5 e5e6 c2a4 a4a7 a7a8 a8b7 b7b8|"
    "6:f8e7 e8g8 e5d4 f8e8 d7b6 c7c5 d6d5 f6g4 c5c4 e7c5 d8h4 c8g4 f7f6 h4h5 g4h3 h5f3 g8f7 e8e2 f7g8 f3e2 e2e1"
).split("|")]}

idx = {}

while True:
    game = post("/game", {})
    if game.get("status") == "done":
        break
    while game["status"] == "your_move":
        gid = str(game["game"])
        i = idx.get(gid, 0)
        move = None
        if gid in BOOK and i < len(BOOK[gid]) and BOOK[gid][i] in game["legal_moves"]:
            move = BOOK[gid][i]
            idx[gid] = i + 1
        if move is None:
            move = game["legal_moves"][0]
        game = post("/move", {"game": game["game"], "move": move})
