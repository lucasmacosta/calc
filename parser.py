from pyparsing import Word, ParseException, Literal, Combine, Optional, nums, Forward, ZeroOrMore, StringStart, StringEnd
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

        '''
        expr = Forward()
        atom = floatNumber.setParseAction( self.pushFirst ) | ( lPar + expr + rPar )
        term = atom + ZeroOrMore( (multOp + atom).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( (addOp + term).setParseAction( self.pushFirst ) )

        '''
        # Now the actual grammar ;)
        expr = Forward()
        term = Forward()

        atom = floatNumber.setParseAction( self.pushFirst ) | ( lPar + expr + rPar )
        factor = (logOp + atom).setParseAction( self.pushFirst ) ^ atom
        term << ( factor + ( multOp + term ).setParseAction( self.pushFirst ) ^ factor )
        expr << ( term + ( addOp + expr ).setParseAction( self.pushFirst ) ^ term )

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


    def pushFirst( self, str, loc, toks ):
        self.exprStack.append( toks[0] )


    def evaluate( self ):
        op = self.exprStack.pop()
        if op in "+-*/":
            op2 = self.evaluate( )
            op1 = self.evaluate( )
            return self.ops[op]( op1, op2 )
        elif op == "log":
            op = self.evaluate( )
            return self.funcs['log']( op )
        else:
            return float( op )


    def parse( self, expr ):
        self.exprStack = []
        try:
            result = self.bnf.parseString( expr )
        except ParseException,err:
            raise Exception, 'Parse Failure: ' + str(err)

        return { "parseResult": result, "evaluation": self.evaluate( ) }
