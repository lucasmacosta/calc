from pyparsing import Word, alphas, ParseException, Literal, CaselessLiteral \
, Combine, Optional, nums, Or, Forward, ZeroOrMore, StringEnd, alphanums

from parser import Parser


myParser = Parser()

if __name__ == "__main__":

    def test( s ):
        global myParser
        try:
        	results = myParser.parse( s )
        	print s, "=", results['parseResult'], "=>", results['evaluation']
    	except Exception, err:
    		print s, "=> parsing failed!!", err
  
    test( "" )
    test( "9" )
    test( "-9" )
    test( "(3)" )
    test( "9 * -2" )
    test( "9 * -2 + 5" )
    test( "5.5 + 9 * -2" )
    test( "(5 + 9) * -2" )
    test( "5 * 3 * (8 - 23)" )
    test( "(2 + 2) * log 10 / 3" )
    test( "--5" )
    test( "5 / 0" )
