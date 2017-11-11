from flask import Flask
from flask import request
from flask import jsonify
import json
from classifier.classifier import Classifier

app = Flask(__name__)

@app.route('/classify')
def classify():
    filename = request.args.get("filename")
    c = Classifier()
    res = c.classify_image(filename)
    return jsonify({"results":res})

if __name__ == '__main__':
    app.run(debug=True)
