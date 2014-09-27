from flask import Flask, request, g, abort, json


# create our little application :)
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/', methods=['GET'])
def default_route():
    temp = json.jsonify({ "hola": "chau"})
    return temp, 200, { 'Content-Type': 'application/json' }


# Route to perform a calculation
# Returns 200 and the result if success, a 400 otherwise
@app.route('/calculate', methods=['GET'])
def calculate():
    expression = request.args.get('expression', '')
    temp = json.jsonify({ "hola": "chau"})
    return temp, 200, { 'Content-Type': 'application/json' }


if __name__ == '__main__':
    app.run()
