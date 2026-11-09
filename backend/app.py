
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "devops_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432")
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Multi-Service Application is running!",
        "status": "success"
    })


@app.route("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "database": "PostgreSQL",
            "status": "connected"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/interns")
def get_interns():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, role FROM interns")
        records = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "role": row[2]
            }
            for row in records
        ])

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

