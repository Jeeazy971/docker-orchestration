from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)


@app.route("/")
def hello():
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "mydb")
    db_user_file = os.getenv("DB_USER_FILE", "/run/secrets/db_user")
    db_password_file = os.getenv(
        "DB_PASSWORD_FILE", "/run/secrets/db_password")

    with open(db_user_file) as f:
        db_user = f.read().strip()
    with open(db_password_file) as f:
        db_password = f.read().strip()

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return jsonify({"message": "Hello from Flask with DB connection OK!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
