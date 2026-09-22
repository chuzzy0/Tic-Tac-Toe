from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple game state
board = [""] * 9
current_player = "X"
winner = None


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
  return jsonify(
      {"board": board, "currentPlayer": current_player, "winner": winner}
  )


@app.route("/api/move", methods=["POST"])
def make_move():
  global current_player, winner
  data = request.json
  index = data.get("index")

  if winner or board[index] != "":
    return jsonify(
        {"board": board, "currentPlayer": current_player, "winner": winner}
    )

  board[index] = current_player

  # Check win patterns
  wins = [
      (0, 1, 2),
      (3, 4, 5),
      (6, 7, 8),
      (0, 3, 6),
      (1, 4, 7),
      (2, 5, 8),
      (0, 4, 8),
      (2, 4, 6),
  ]
  for a, b, c in wins:
    if board[a] and board[a] == board[b] and board[a] == board[c]:
      winner = board[a]
      break

  if not winner and "" not in board:
    winner = "Tie"

  if not winner:
    current_player = "O" if current_player == "X" else "X"

  return jsonify(
      {"board": board, "currentPlayer": current_player, "winner": winner}
  )


@app.route("/api/reset", methods=["POST"])
def reset_game():
  global board, current_player, winner
  board = [""] * 9
  current_player = "X"
  winner = None
  return jsonify(
      {"board": board, "currentPlayer": current_player, "winner": winner}
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)