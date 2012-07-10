import sys
import os

#update the system path so we can run both simulator and translator at once
sys.path.append(sys.path[0] + os.sep + 'simulator')
sys.path.append(sys.path[0] + os.sep + 'translator')

MARGS_EXT = '.margs'

def tokenize(infile, outfile = None):
  """
  Tokenizes a given input file and writes the tokens to the given outfile or screen
  infile (text): input file to tokenize
  outfile (text, optional): output file to write to
  """
  
  from translator import parser
  p = parser.Parser(infile).loadFile().parse()
  if outfile != None:
    f = open(outfile, 'w')
    f.write(str(p))
    f.close()
  else:
    print str(p)
  
def translate(infile, outfile = None):
  """
  Translates a given input file and writes the output to the given outfile or screen
  infile (text): input file to translate
  outfile (text, optional): output file to write to
  """
  
  from translator import parser
  from translator import compiler
  
  p = parser.Parser(infile).loadFile().parse()
  if len(p.errors) > 0:
    quit('ERRORS:\n' + '\n'.join(p.errors))
  c = compiler.Compiler(p.tokens)
  c.run()
  if outfile != None:
    f = open(outfile, 'w')
    f.write(str(c))
    f.close()
  else:
    print str(c)

def simulate(infile, outfile = None):
  """
  Simulates a given PL/0. Makes use of external pypl0 library.
  infile (text): input file to translate
  outfile (text, optional): file to write results to
  """
  
  from simulator import interp
  from simulator import main
  
  if outfile != None: #overwrite stdout
    sys.stdout = open(outfile,'w')
  interp.interpret(main._genAstFromFile(infile))
  if outfile != None: #restore stdout
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def both(infile, outfile = None):
  from translator import parser
  from translator import compiler
  """
  Translates and Simulates a given input Margs file.
  infile (text): input file to simulate
  outfile (text, optional): file to write results to
  """
  p = parser.Parser(infile).loadFile().parse()
  if len(p.errors) > 0:
    quit('ERRORS:\n' + '\n'.join(p.errors))
  c = compiler.Compiler(p.tokens)
  c.run()
  out = open('TEMP_FILE', 'w') #temporary output file (to send to simulator)
  out.write(''.join([str(i) for i in c.compiled])) #the compiled code
  out.close()
  simulate('TEMP_FILE', outfile)
  os.remove('TEMP_FILE') #clean up the temp file

def tests():
  from datetime import datetime
  
  print 'Beginning Testing'
  
  old, errors, success, removes = sys.stdout, 0, 0, list()
  
  begin = datetime.now()
  
  for fn in os.listdir('tests'):
    if fn.endswith(MARGS_EXT):
      fpath = 'tests' + os.sep + fn
      
      efn = fn.split(MARGS_EXT)[0] + '.expected' #expected filename
      epath = 'tests' + os.sep + efn
      ofn = fn.split(MARGS_EXT)[0] + '.observed' #observed filename
      opath = 'tests' + os.sep + ofn
      if not os.path.exists(epath):
        print '*** FATAL: Expected test file does not exist (' + efn + ')'
      else:
        both(fpath, opath)
        observed = open(opath, 'r').readlines()[0].strip() #firest line of observed test
        expected = open(epath, 'r').readlines()[0].strip() #first line of expected test
        if observed != expected:
          errors += 1
          print '*** FAILED: ' + fn
          print '         OBSERVED: ' + observed 
          print '         EXPECTED: ' + expected
        else:
          print '    SUCCESS: ' + fn
          success += 1
        removes.append(opath)
  
  end = datetime.now()
  
  for f in removes: os.remove(f) #clean up temporary observed file
  
  print 'End Testing.' + (' ' * 10) + 'Success: ' + str(success) + (' ' * 10) + 'Errors: ' + str(errors) + (' ' * 10) + 'Time: ' + str(end - begin)


if __name__ == '__main__':
  #map action strings to corresponding function
  actions = {
    'tokenize' : tokenize,
    'translate' : translate,
    'simulate' : simulate,
    'both' : both,
    'tests' : tests
  }

  from optparse import OptionParser
  parser = OptionParser(
      usage="""
python %prog action [-o outputfile] infile
Action is one of
tokenize   -  Tokenize a program from Margs
translate  -  Translate a program from Margs to PL/0 (Recommended)
simulate   -  Simulate a program written in PL/0 assembly language
both       -  Translate and simulate a program written in Margs
tests      -  Run all test files through compiler and simulator for expected output""")

  parser.add_option('-o', '--outputfile', action='store', dest='outputfile', help='Output file.')
  (options, args) = parser.parse_args()
  
  if len(args) == 1 and args[0] == 'tests':
    tests()
  else:
    if len(args) != 2:
      parser.error('Wrong number of arguments.')
    
    action = args[0]
    infile = args[1]
    if action in actions.keys() and len(args) == 2:
      if hasattr(options, 'outputfile') and options.outputfile:
        actions[action](infile, options.outputfile)
      else:
        actions[action](infile)
    else:
      parser.error('Invalid action.')
