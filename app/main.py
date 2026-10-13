
from flask import Flask, jsonify, request
import chess
import chess.pgn
import io

app = Flask(__name__)

OPENINGS = {
    "e4 e5 Nf3 Nc6 Bb5": {
        "name": "Ruy Lopez",
        "eco": "C60",
    },
    "e4 e5 Nf3 Nc6 Bc4": {
        "name": "Italian Game",
        "eco": "C50",
    },
    "e4 c5": {
        "name": "Sicilian Defense",
        "eco": "B20",
    },
}


@app.get("/")
def index():
    return jsonify({
        "application": "Chess Opening Explorer",
        "version": "1.0.0",
        "endpoints": ["/health", "/api/opening"],
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/opening")
def find_opening():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected a JSON object"}), 400

    moves = data.get("moves")

    if not isinstance(moves, str) or not moves.strip():
        return jsonify({"error": "Provide moves as a non-empty string"}), 400

    board = chess.Board()
    normalized_moves = []

    try:
        for san in moves.split():
            move = board.parse_san(san)
            normalized_moves.append(board.san(move))
            board.push(move)
    except ValueError:
        return jsonify({"error": "Invalid move sequence"}), 400

    opening = None

    # Match the longest known opening prefix.
    for length in range(len(normalized_moves), 0, -1):
        prefix = " ".join(normalized_moves[:length])
        if prefix in OPENINGS:
            opening = OPENINGS[prefix]
            break

    return jsonify({
        "moves": normalized_moves,
        "fen": board.fen(),
        "opening": opening,
        "move_count": len(normalized_moves),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
