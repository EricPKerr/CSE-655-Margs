import os, re, string

#valid literal keywords (non identifiers) used in the tokenizing process
literal_words = {
  '<=' : 'LTEQ',
  '>=' : 'GTEQ',
  '<' : 'LT',
  '>' : 'GT',
  '+' : 'PLUS',
  '-' : 'MINUS',
  '*' : 'MUL',
  '/' : 'DIV',
  '(' : 'LPAREN',
  ')' : 'RPAREN',
  '{' : 'LBLOCK',
  '}' : 'RBLOCK',
  '.' : 'DOT',
  '=' : 'EQUALS',
  '==' : 'EQUAL',
  '!=' : 'NOTEQUAL',
  ',' : 'COMMA',
  ';' : 'SEMI',
  'true' : 'TRUE',
  'false' : 'FALSE',
  'var' : 'VAR',
  'const' : 'CONST',
  'function' : 'FUNCTION',
  'INPUT' : 'INPUT',
  'OUTPUT' : 'OUTPUT',
  'if' : 'IF',
  'else' : 'ELSE',
  'while' : 'WHILE'
}

class Parser():
  def __init__(self, filename):
    """
    The Parser initializer
    filename (string): The file to open and tokenize.
    """
    self.filename = filename
    self.errors = list() #list of errors during tokenizing.
    self.tokens = list() #list of tokens produced during tokenizing.
    self.lines = list() #lines of code to parse (usually from input file but can be overridden).
    self.legal = True #whether all of the tokens were legal or not.
  
  def loadFile(self):
    if not os.path.exists(self.filename):
      self.errors.append('Input program ' + self.filename + ' does not exist.')
    else:
      self.lines = file(self.filename, 'r').readlines()
    return self
  
  def parse(self):
    line_num = 0
    for line in self.lines:
      line_num += 1
      line = line.strip()
      if len(line) == 0: continue
      self.tokenize(line, line_num)
    return self
  
  def tokenize(self, line, line_num):
    while line:
      line = line.lstrip() #remove all leading whitespace
      if not line: continue #skip if it's an empty line
      if line[:2] in ('<=', '>=', '!=', '=='):
        self.tokens.append(Token(line[:2], literal_words[line[:2]], line=line_num))
        line = line[2:]
      elif line[0] in ('<', '>', '+', '-', '*', '/', '(', ')', '{', '}', '=', ',', ';'):
        self.tokens.append(Token(line[0], literal_words[line[0]], line=line_num))
        line = line[1:]
      else:
        m = re.match('[a-zA-Z]\w*', line)
        if m:
          text = m.group()
          if literal_words.has_key(text):
            t = Token(text, literal_words[text], line=line_num) #keyword
          elif set(text).issubset(set(string.lowercase)):
            t = Token(text, Token.IDENTIFIER, line=line_num) #identifier
          else:
            t = Token(text, Token.ILLEGAL, False, line=line_num) #is all alphanumeric but contains uppercase and isnt a keyword
          self.tokens.append(t)
          line = line[len(text):]
        else:
          m = re.match('[\.\d]+', line) #numeric regex (not perfect, fails for 1.2.3.4)
          if m: #numbers
            text = m.group()
            self.tokens.append(Token(text, Token.NUMBER, line=line_num))
            line = line[len(text):]
          else: #illegal token
            self.legal = False;
            m = re.match('(\S)\s', line) #illegal, so we'll get everything before the next space
            text = m.group(1)
            self.tokens.append(Token(text, Token.ILLEGAL, False, line=line_num))
            line = line[len(text):]
  
  def __str__(self):
    """
    String representation of the Parser.
    """
    return '\n'.join([str(token) for token in self.tokens])

class Token():
  IDENTIFIER = 'IDENTIFIER'
  NUMBER = 'NUMBER'
  ILLEGAL = 'ILLEGAL'

  def __init__(self, text, _type, legal = True, line = 0):
    """
    Token initiazer
    text (string): Raw text in the token (found within the file)
    _type (string): Type of token (found in literal_words.values())
    legal (bool): Whether the token is valid or not
    line (int): Line number the token was found on
    """
    self.text = text
    self.type = _type
    self.legal = legal
    self.line = line
    self.value = None

  def __str__(self):
    """
    String representation of the Token.
    """
    return self.text + ' >> Line ' + str(self.line) + ' >> ' + self.type

#map all of the literal_words values and give Token the corresponding attribute. Nice hack.
map(lambda t: setattr(Token, t, t), literal_words.values())
