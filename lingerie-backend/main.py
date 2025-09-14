from flask import jsonify
from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()
app=create_app()

@app.route("/")
def Home():
    return jsonify({"message": "Flask + SQLite backend ready"})

if __name__=="__main__":
    app.run(debug=True)

