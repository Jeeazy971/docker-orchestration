from flask import Flask , jsonify
import os
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello():
    db_user = os.environ.get("DB_USER", "user")
    db_password = os.environ.get("DB_PASSWORD", "password")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "mydb")

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
