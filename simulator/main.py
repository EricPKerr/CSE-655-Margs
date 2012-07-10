##
## These functions define convenient entry points for the system.
## All parameters to these functions are strings of filenames.
## Also serves as a utility script.
## Run "python main.py -h" for help.
##

def _parseFile(infile):
    import parser
    f = open(infile)
    parsetree = parser.parse(f)
    f.close()
    return parsetree

def printParseTreeFromFile(infile):
    import utils
    utils.prettyPrintTree(_parseFile(infile))

def _genAstFromFile(infile):
    import astgen
    ast = astgen.traverse(_parseFile(infile))
    return ast

def printAstFromFile(infile):
    import utils
    utils.prettyPrintTree(_genAstFromFile(infile))

def interpretFile(infile):
    import interp
    interp.interpret(_genAstFromFile(infile))

if __name__ == '__main__':
    actions = {
            'parseprint' : printParseTreeFromFile,
            'astprint'   : printAstFromFile,
            'interp'     : interpretFile
            }

    from optparse import OptionParser
    parser = OptionParser(
            usage="""
python %prog action [-o outputfile] pl0sourcefile
Action is one of
    parseprint      - parse and print the parse tree,
    astprint        - parse, generate the AST then print the AST,
    interp          - parse, generate the AST then interpret the AST""")
    parser.add_option('-o', '--outputfile',
                      action='store',
                      dest='outputfile',
                      help='Output file.')
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error('wrong number of arguments.')

    action = args[0]
    infile = args[1]
    if action in ('parseprint', 'astprint', 'interp') and len(args) == 2:
        if action == 'x86asm' or action == 'c--':
            # check -o option
            if hasattr(options, 'outputfile') and options.outputfile:
                actions[action](infile, options.outputfile)
            else:
                parser.error('Missing -o option.')
        else:
            actions[action](infile)
            print '\n'
    else:
        parser.error('Invalid action.')

