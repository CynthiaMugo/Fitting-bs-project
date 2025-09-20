from flask import jsonify
from app import create_app
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_cors import CORS

bycrypt=Bcrypt()
load_dotenv()
app=create_app()
CORS(app)

@app.route("/")
def Home():
    return jsonify({"message": "Flask + SQLite backend ready"})

if __name__=="__main__":
    app.run(debug=True)

