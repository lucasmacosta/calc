from pyparsing import Word, ParseException, Literal, Combine, Optional, nums, Forward, ZeroOrMore, StringStart, StringEnd

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

        # Now the actual grammar ;)
        expr = Forward()
        atom = floatNumber.setParseAction( self.pushFirst ) | ( lPar + expr + rPar )
        term = atom + ZeroOrMore( (multOp + atom).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( (addOp + term).setParseAction( self.pushFirst ) )

        self.bnf = expr

        self.ops = {
            "+" : lambda a, b: a + b,
            "-" : lambda a, b: a - b,
            "*" : lambda a, b: a * b,
            "/" : lambda a, b: a / b
        }


    def pushFirst( self, str, loc, toks ):
        self.exprStack.append( toks[0] )


    def evaluate( self ):
        op = self.exprStack.pop()
        if op in "+-*/":
            op2 = self.evaluate( )
            op1 = self.evaluate( )
            return self.ops[op]( op1, op2 )
        else:
            return float( op )


    def parse( self, str ):
        self.exprStack = []
        try:
            result = self.bnf.parseString( str )
        except ParseException,err:
            raise Exception, 'Parse Failure:' + str

        return { "parseResult": result, "stack": self.exprStack, "evaluation": self.evaluate( ) }
