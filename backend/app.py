from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

def init_db():
    conn = sqlite3.connect("eco.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS puntos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        puntos INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        print("Datos recibidos:", data)  # 👈 DEBUG

        if not data:
            return jsonify({"status": "error", "msg": "No data"}), 400

        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "1234":
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error"})

    except Exception as e:
        print("ERROR:", e)  # 👈 IMPORTANTE
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/puntos", methods=["POST"])
def guardar():
    data = request.json

    conn = sqlite3.connect("eco.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO puntos (username, puntos) VALUES (?, ?)",
                   (data["username"], data["puntos"]))

    conn.commit()
    conn.close()

    return jsonify({"status": "guardado"})

@app.route("/puntos/<username>")
def obtener(username):
    conn = sqlite3.connect("eco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(puntos) FROM puntos WHERE username=?", (username,))
    total = cursor.fetchone()[0] or 0

    conn.close()

    return jsonify({"puntos": total})

if __name__ == "__main__":
    app.run(debug=True)