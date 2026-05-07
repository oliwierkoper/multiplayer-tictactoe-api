from fastapi import FastAPI
import json
from pydantic import BaseModel

FILE_NAME="games.json"

app=FastAPI()

class Move(BaseModel):
    position: int

def load_data():
    try:
        with open(FILE_NAME,"r") as file:
            data=json.load(file)
            return data
    except FileNotFoundError:
        return []
        
def save_data(x):
    data=load_data()
    data.append(x)
    with open(FILE_NAME,"w") as file:
        json.dump(data,file)

@app.post("/games")
def game():
    games=load_data()
    if not games:
        new_id = 1
    else:
        new_id = games[-1]["id"]+1
    new_game={
        "id": new_id,
        "board": ["", "", "", "", "", "", "", "", ""],
        "current_player": "X",
        "winner": None,
        "is_finished": False
    }
    save_data(new_game)
    return new_game
@app.post("/games/{id}/move")
def move(id: int, move: Move):
    games = load_data()
    if not games:
        return{
            "error": "no games found"
        }
    for i in games:
        if i["id"] == id:
            if i["is_finished"]:
                return{
                    "error": "game is already finished"
                }
            if move.position not in range(0,9):
                return{
                    "error": "wrong move"
                }
            if i["board"][move.position] != "":
                return{
                    "error": "wrong move"
                }
            i["board"][move.position] = i["current_player"]
            if i["current_player"] == "X":
                i["current_player"] = "O"
            else:
                i["current_player"] = "X"
            with open(FILE_NAME,"w") as file:
                json.dump(games,file)
            return i 
    return{
        "error": "game not found"
    }

