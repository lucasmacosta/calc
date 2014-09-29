from flask import Flask, request, g, abort, json
from parser import Parser
from database import db_session, init_db
from models import Session, Expression
from sqlalchemy.orm.exc import NoResultFound

# Init flask app
app = Flask(__name__)
# Get config
app.config.from_pyfile('config.py')


# Init db, it creates tables if not already on the database
init_db()


# Callback to close db session on exit
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Simple math expressions parser
parser = Parser()


# Utility to send json-encoded responses
def jsonResponse( payload, statusCode ):
    encodedStr = json.jsonify( payload )
    return encodedStr, statusCode


# Root
@app.route('/')
def default_route():
    return jsonResponse( { "error": "Invalid endpoint!" }, 400 )


# Route to perform a calculation
# Returns 200 and the result if success, a 400 otherwise
@app.route('/calculate', methods=['GET'])
def calculate():
    expression = request.args.get('expression', '')
    global parser
    try:
        results = parser.parse( expression )
    except Exception, err:
        return jsonResponse({ "error": str(err) }, 400)

    return jsonResponse( { "result": results['evaluation'] }, 200 )


# Wrapper object for an expression and its result
def expression_obj(expression):
    expr_obj = { 'expr': expression.expr_str }
    try:
        results = parser.parse( expression.expr_str )
        expr_obj['result'] = results['evaluation']
    except Exception, err:
        expr_obj['result'] = 'error'
    return expr_obj

# Convert session to an object to return it in the REST interface
def session_to_object(session_model):
    session = {
        'id': session_model.id,
        'number': session_model.number,
        'expressions': map( expression_obj, session_model.expressions )
    }
    return session

# REST interface to store and retrieve calculation sessions

@app.route('/session/<int:session_id>', methods=['POST'])
def store_session(session_id):
    # Get form data
    expression = request.form.get('expression', '')

    # Check if a new session is needed
    try:
        session = db_session.query(Session).filter(Session.number == session_id).one()
    except NoResultFound, err:
        session = Session(session_id)
        db_session.add(session)

    # Cleanup the associated expressions
    session.expressions = []

    # Add related expressions
    for expr in expression.split('|'):
        session.expressions.append(Expression(expr))

    # Save and return
    try:
        db_session.commit()
    except Exception, err:
        return jsonResponse({ "error": str(err) }, 500)

    # Success!
    return jsonResponse(session_to_object( session ), 200)


@app.route('/session/<int:session_id>', methods=['GET'])
def get_session(session_id):
    try:
        session = db_session.query(Session).filter(Session.number == session_id).one()
    except Exception, err:
        return jsonResponse({ "error": str(err) }, 404)

    # Success!
    return jsonResponse(session_to_object( session ), 200)


if __name__ == '__main__':
    app.run()
 