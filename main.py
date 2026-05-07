from fastapi import FastAPI
import json
from pydantic import BaseModel

FILE_NAME="games.json"

app=FastAPI()

class Move(BaseModel):
    position: int

def check_winner(board):
    if board[0]==board[1]==board[2] != "":
        return board[0]
    if board[3]==board[4]==board[5] != "":
        return board[3]
    if board[6]==board[7]==board[8] != "":
        return board[6]
    if board[0]==board[3]==board[6] != "":
        return board[0]
    if board[1]==board[4]==board[7] != "":
        return board[1]
    if board[2]==board[5]==board[8] != "":
        return board[2]
    if board[0]==board[4]==board[8] != "":
        return board[0]
    if board[2]==board[4]==board[6] != "":
        return board[2]
    return None

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
            if check_winner(i["board"]) != None:
                i["winner"]=check_winner(i["board"])
                i["is_finished"]=True
                with open(FILE_NAME,"w") as file:
                    json.dump(games,file)
                return i
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