from hashlib import new
from typing import List
from flask import Flask, jsonify, request
from joblib import load
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'

@app.route("/regression", methods=['GET', 'POST'])
def regression():
    if request.method == 'POST':

        key = request.form['key']
        key = key.split(",")

        new_key = np.array(key)
        y = new_key.astype(np.float)
    
        model = load("regression_model.joblib")

        predict = model.predict([y])

        print(predict)

        return jsonify({"predictions": predict.tolist()})
    else:
        return 'working'

if __name__ == '__main__':
    app.run(debug=True)