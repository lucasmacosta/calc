calc
====

Experimenting with Python :)

## Install

In order to avoid issues with multiple versions of python is recommended to use [virtualenv](http://virtualenv.readthedocs.org/en/latest/)

After **virtualenv** is installed, you can issue this command from the console to create a new env:
```
$ virtualenv venv
```

And then activate it with:
```
$ source venv/bin/activate
```

Then install the required dependencies:
```
$ pip install flask
$ pip install pyparsing
$ pip install sqlalchemy
$ pip install requests
```

## Running the server

Run the REST server with:
```
$ python calcServer.py
```

## Runnnig the client

Fire another console, run the CLI script and follow the onscreen instructions:
```
$ python calc.py
```
