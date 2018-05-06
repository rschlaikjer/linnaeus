import json
import os
import tempfile

from flask import Flask, request, jsonify

from classifier.classifier import Classifier

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    tmpfd, tmpfile = tempfile.mkstemp()
    request.get_data()
    os.write(tmpfd, request.data)
    try:
        c = Classifier()
        res = c.classify_image(tmpfile)
        formatted = _format_results(res)
        return jsonify(formatted)
    finally:
        os.close(tmpfd)


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
    app.run(debug=True, host='0.0.0.0')
