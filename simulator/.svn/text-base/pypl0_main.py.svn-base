##
## These functions define convenient entry points for the system.
## All parameters to these functions are strings of filenames.
## Also serves as a utility script.
## Run "python pypl0_main.py -h" for help.
##

def _parseFile(infile):
    import pypl0_parser as parser
    f = open(infile)
    parsetree = parser.parse(f)
    f.close()
    return parsetree

def printParseTreeFromFile(infile):
    import pypl0_utils as utils
    utils.prettyPrintTree(_parseFile(infile))

def _genAstFromFile(infile):
    import pypl0_astgen as astgen
    ast = astgen.traverse(_parseFile(infile))
    return ast

def printAstFromFile(infile):
    import pypl0_utils as utils
    utils.prettyPrintTree(_genAstFromFile(infile))

def interpretFile(infile):
    import pypl0_interp as interp
    interp.interpret(_genAstFromFile(infile))

def genX86AssemblyFromFile(infile, outfile):
    import pypl0_x86codegen as codegen
    f = open(outfile, 'w')
    codegen.gen(_genAstFromFile(infile), f)
    f.close()

def genCMinusFromFile(infile, outfile):
    pass

if __name__ == '__main__':
    actions = {
            'parseprint' : printParseTreeFromFile,
            'astprint'   : printAstFromFile,
            'interp'     : interpretFile,
            'x86asm'     : genX86AssemblyFromFile,
            'c--'        : genCMinusFromFile }

    from optparse import OptionParser
    parser = OptionParser(
            usage="""
python %prog action [-o outputfile] pl0sourcefile
Action is one of
    parseprint      - parse and print the parse tree,
    astprint        - parse, generate the AST then print the AST,
    interp          - parse, generate the AST then interpret the AST,
    x86asm          - parse, generate the AST and x86 assembly
                      (use the Makefile if you want to get the binary executable),
    c--             - parse, generate the AST the C-- code (not supported yet).
Outputfile is ignored unless the action is x86asm or c--.""")
    parser.add_option('-o', '--outputfile',
                      action='store',
                      dest='outputfile',
                      help='Output file.')
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error('wrong number of arguments.')

    action = args[0]
    infile = args[1]
    if action in ('parseprint', 'astprint', 'interp',
                  'x86asm', 'c--') and len(args) == 2:
        if action == 'x86asm' or action == 'c--':
            # check -o option
            if hasattr(options, 'outputfile') and options.outputfile:
                actions[action](infile, options.outputfile)
            else:
                parser.error('Missing -o option.')
        else:
            actions[action](infile)
    else:
        parser.error('Invalid action.')

