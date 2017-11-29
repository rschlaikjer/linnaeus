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
    formatted = _format_results(res)
    return jsonify(formatted)


def _format_results(results):
    """
    Turn raw output of classifier into something more friendly    
    """
    ret = []
    for result in results:
        class_id = result['class_name'].split(' ')[0]
        class_name = ' '.join(result['class_name'].split(' ')[1:])
        probability = str(result['probability'])
        obj = {}
        obj["classId"] = class_id
        obj["className"] = class_name 
        obj["probability"] = probability 
        ret.append(obj)
    return ret

if __name__ == '__main__':
    app.run(debug=True)
