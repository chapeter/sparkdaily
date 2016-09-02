__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Healthy"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
