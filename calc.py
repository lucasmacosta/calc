import requests
from requests.exceptions import ConnectionError
import sys, getopt
import re

server = 'http://127.0.0.1:5000'


# Generic handler of http requests
def request_handler(type, endpoint, params = {}):
	try:
		if (type == 'post'):
			r = requests.post(endpoint, data=params)
		elif (type == 'get'):
			r = requests.get(endpoint, params=params)
	except ConnectionError, err:
		return False, "Connection error, make sure that calcServer.py is up and running"

	response = r.json()
	if r.status_code != requests.codes.ok:
		return False, response['error']

	return True, response


# Use server to calculate expressions
def calculate_expression(expression):
	global server
	endpoint = server + '/calculate'

	status, response = request_handler('get', endpoint, { 'expression': expression })

	if (status == False):
		print 'Error on calculation: ', response
	else:
		print response['result']

	return status


# Handle persistence of sessions
def session_persistence(operation, session_id, session):
	global server
	endpoint = '{0}/session/{1}'.format(server, session_id)

	if operation == 'save':
		status, response = request_handler('post', endpoint, { 'expression': '|'.join(session) })

		if (status == False):
			print 'Error while saving: ', response
			return False

		print 'Session {0} saved'.format(session_id)

		# Session is now empty
		return []

	elif operation == 'retrieve':
		status, response = request_handler('get', endpoint)

		if (status == False):
			print 'Error while retrieving: ', response
			return False

		print 'Session {0} retrieved'.format(session_id)

		new_session = []
		for expr in response['expressions']:
			print '\t{0} = {1}'.format(expr['expr'], expr['result'])
			new_session.append(expr)

		# Session now has the retrieved expressions
		return new_session



# Main program
def main(argv):
	global server
	session_expressions = []
	try:
		opts, args = getopt.getopt(argv,"hs:",["server="])
	except getopt.GetoptError:
		print 'calc.py -s <server>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'calc.py -s <server>'
			sys.exit()
		elif opt in ("-s", "--server"):
			server = arg
	print 'Using server at ', server
	print 'Simple calculator'
	print 'Enter "exit" to finish'
	print 'Enter "save <id>" to save a session'
	print 'Enter "retrieve <id>" to retrieve a session'
	print 'Enter a math expression to perform calculation'
	while (True):
		command = raw_input("$: ")
		search = re.match(r'(save|retrieve) (\d+)', command)
		if search:
			# Perform operation
			op_result = session_persistence(search.group(1), search.group(2), session_expressions)
			if op_result != False:
				# Update the session with the session result
				session_expressions = op_result
		else:
			# Calculate expression
			if calculate_expression(command):
				# Only valid expressions are added to session
				session_expressions.append(command)



if __name__ == "__main__":
   main(sys.argv[1:])
