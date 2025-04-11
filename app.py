from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
game_state = {
    "board": [""] * 9,
    "current_player": "X",
    "winner": None
}

def check_winner(board):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        idx = int(request.form["cell"])
        if game_state["board"][idx] == "" and game_state["winner"] is None:
            game_state["board"][idx] = game_state["current_player"]
            game_state["winner"] = check_winner(game_state["board"])
            if not game_state["winner"]:
                game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
        return redirect(url_for("index"))
    return render_template("index.html", state=game_state)

@app.route("/restart")
def restart():
    game_state["board"] = [""] * 9
    game_state["current_player"] = "X"
    game_state["winner"] = None
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)

