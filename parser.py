from pyparsing import Word, ParseException, Literal, Combine, Optional, nums, Forward, ZeroOrMore, StringStart, StringEnd, Group
from math import log10

class Parser:

    def __init__( self ):

        # define grammar

        # definition of a float number
        point       = Literal('.')
        plusOrMinus = Literal('+') | Literal('-')
        number      = Word(nums)
        integer     = Combine( Optional(plusOrMinus) + number )
        floatNumber = Combine( integer + Optional( point + number ) )

        # operators
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )

        # parentheses are discarded
        lPar  = Literal( "(" ).suppress()
        rPar  = Literal( ")" ).suppress()

        # For precedence handling
        addOp  = plus | minus
        multOp = mult | div
        logOp  = Literal( "log" )

        expr = Forward()
        term = Forward()

        atom = floatNumber | ( lPar + expr + rPar )
        factor = Group(logOp + atom) | atom
        term << ( Group(factor + multOp + term ) | factor )
        expr << ( Group(term + addOp + expr ) | term )

        self.bnf = StringStart() + expr + StringEnd()

        self.ops = {
            "+" : lambda a, b: a + b,
            "-" : lambda a, b: a - b,
            "*" : lambda a, b: a * b,
            "/" : lambda a, b: a / b
        }

        self.funcs = {
            "log" : lambda a: log10(a)
        }


    def evaluate( self, node ):
        if isinstance(node, basestring):
            if node in "+-*/":
                return self.ops[node]
            elif node in ["log"]:
                return self.funcs[node]
            else:
                return float(node)
        else:
            if len(node) == 3:
                operator = self.evaluate(node[1]);
                return operator(self.evaluate(node[0]), self.evaluate(node[2]))
            elif len(node) == 2:
                function = self.evaluate(node[0]);
                return function(self.evaluate(node[1]))
            else:
                return self.evaluate(node[0])


    def parse( self, expr ):
        self.exprStack = []
        try:
            result = self.bnf.parseString( expr )
        except ParseException,err:
            raise Exception, 'Parse Failure: ' + str(err)

        return { "parseResult": result, "evaluation": self.evaluate( result ) }
