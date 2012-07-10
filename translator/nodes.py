from parser import Token
from copy import copy

class Node():
  """
  Abstract base class for all nodes within the language Grammar.
  """
  
  def __init__(self, compiler = None):
    """
    Initializer for the Node.
    """
    self.compiler = compiler
  
  def build(self):
    """
    Use and consume the tokens to build an abstract syntax tree.
    """
    pass
  
  def clean(self):
    """
    Prepare the node to be translated to PL/0.
    """
    pass
  
  def compile(self, indent = 0):
    """
    Generate the compiled PL/0 code for the given node.
    indent (int, optional): The level of indentation for the given node in the compiled program.
    """
    pass

def _indent(num = 0):
  """
  Helper function to indent a given number of blocks
  num (int, optional): The amount to indent
  """
  return str('  ' * num)


class Comparison(Node):
  """
  Comparison node from the Grammar.
  """
  
  #translations for straight conversion (true => true)
  normal = {
    '<=' : '<=',
    '>=' : '>=',
    '<'  : '<',
    '>'  : '>',
    '==' : '=',
    '!=' : '#'
  }
  
  #translations for inverted conversion (true => false)
  inverted = {
    '<=' : '>=',
    '>=' : '<=',
    '<'  : '>',
    '>'  : '<',
    '==' : '#',
    '!=' : '='
  }
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error('must contain at least 1 token for valid syntax')
    if self.compiler.next() not in self.compiler.valid_comparison_tokens: self.compiler.error('COMPARISON token expected. Found ' + self.compiler.next())
    self.comparison = self.compiler.tokens[0].text
    self.compiler.skip(1) # <comparison>
    return self
  
  def compile(self, indent = 0, inverse = False):
    self.compiler.compiled.append(self.normal[self.comparison] if not inverse else self.inverted[self.comparison])

class Condition(Node):
  """
  Condition node from the Grammar.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.left = None # (Expression) the left portion of the condition
    self.right = None # (Expression) the right portion of the condition
    self.comparison = None # (Comparison) the comparison made between the two Expressions
    self.boolean = None # The boolean operation (if no comparison is made)
  
  def build(self):
    if len(self.compiler.tokens) < 3: self.compiler.error("must contain at least 3 tokens for valid syntax")
    if self.compiler.next() in (Token.TRUE, Token.FALSE):
      self.boolean = self.compiler.tokens[0].type
      self.compiler.skip(1)
    else:
      self.left = Expression(self.compiler).build()
      self.comparison = Comparison(self.compiler).build()
      self.right = Expression(self.compiler).build()
    return self
  
  def compile(self, indent = 0, inverse = False):
    if self.boolean != None: #it's a boolean and not a comparison (true or false)
      if self.boolean == Token.TRUE:
        self.compiler.compiled.append('1=1' if not inverse else '1#1')
      elif self.boolean == Token.FALSE:
        self.compiler.compiled.append('1#1' if not inverse else '1=1')
    else:
      self.left.compile()
      self.comparison.compile(inverse = inverse)
      self.right.compile()

class Declaration(Node):
  """
  Declaration node from the Grammar. Can either be an assignment (<identifier> = <expression>) or just an <identifier>.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.identifier = None
    self.value = None
    self.assignment = ' = ' #determined/changed by Statement_Vars type
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("must contain at least 1 token for valid syntax")
    if self.compiler.next() != Token.IDENTIFIER: self.compiler.error("IDENTIFIER token expected. Found " + self.compiler.next())
    
    self.identifier = self.compiler.tokens[0] #identifier token
    self.compiler.skip() # <identifier>
    
    if self.compiler.next() == Token.EQUALS:
      self.compiler.skip(1) # =
      self.value = Expression(self.compiler).build() # (Expression) the value corresponding to the declaration
    return self
  
  def compile(self, indent = 0):
    self.compiler.compiled.append(_indent(indent) + self.identifier.text)
    if self.value != None: #append the <expression> portion if the value is defined
      self.compiler.compiled.append(self.assignment) #type of assignment (either = or :=)
      self.value.compile(indent)

class Declaration_List(Node):
  """
  Declaration_List node from the grammar.  Holds a list of Declarations.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.declarations = list()
    self.which = None #type of token the Statement_Var is.
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("must contain at least 1 token for valid syntax")
    if self.compiler.next() != Token.IDENTIFIER: self.compiler.error("IDENTIFIER token expected. Found " + self.compiler.next())
    
    while self.compiler.next() == Token.IDENTIFIER: #iterate through until we don't have any more declarations
      self.declarations.append(Declaration(self.compiler).build())
      if self.compiler.next() != Token.COMMA: #we're at the end because a comma doesn't separate two more values
        break
      elif self.compiler.next(1) == Token.IDENTIFIER: #it's a comma and the following token is an identifier
        self.compiler.skip(1) # ,
    return self
  
  def compile(self, indent = 0):
    if len(self.declarations) > 0:
      if self.which == None:
        for declaration in self.declarations[:-1]:
          declaration.assignment = ' := '
          declaration.compile(indent)
          self.compiler.compiled.append(';\n')
        self.declarations[-1].assignment = ' := '
        self.declarations[-1].compile(indent)
      else:
        for declaration in self.declarations[:-1]:
          declaration.assignment = ' = '
          declaration.compile(0)
          self.compiler.compiled.append(', ')
        self.declarations[-1].assignment = ' = '
        self.declarations[-1].compile(0)

class Expression(Node):
  """
  Expression node from the Grammar.  Can hold any expression or a single identifier.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.expression = list() #the Tokens corresponding to the expression
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("must contain at least 1 token for valid syntax")
    if self.compiler.next() not in self.compiler.valid_expression_tokens: self.compiler.error("EXPRESSION token expected. Found " + self.compiler.next())
    
    lparen, rparen = 0, 0
    while self.compiler.next() in self.compiler.valid_expression_tokens:
      self.expression.append(self.compiler.tokens[0])
      if self.compiler.next() == Token.LPAREN: lparen += 1
      if self.compiler.next() == Token.RPAREN: rparen += 1
      self.compiler.skip(1)
    
    if rparen == lparen + 1 and self.expression[-1].type == Token.RPAREN: # we accidentally took too many parenthesis off (probably from the end of the condition).
      self.compiler.tokens = [self.expression[-1]] + self.compiler.tokens
      self.expression = self.expression[:-1]
    
    if len(self.expression) > 0 and self.expression[0].text == '-': #if there is a leading negative we need to trick PL/0 into thinking it's 0 - <exression>
      t = Token('0', Token.NUMBER, True)
      self.expression = [t] + self.expression
    
    return self
    
  def compile(self, indent = 0):
    self.compiler.compiled += [i.text for i in self.expression]

class Function(Node):
  """
  Function node from the Grammar.  Holds all information corresponding to a given function in the Program.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.name = None #function name
    self.parameters = None #incoming parameters associated with this function
    self.body = list() #statements which comprise the body of the function
    
    self.localvars = Statement_Var(compiler) #holds local definitions as well as variables in parameters
    self.localvars.declarations = Declaration_List(compiler)
    self.localvars.which = Token.VAR
  
  def build(self):
    if len(self.compiler.tokens) <= 7: self.compiler.error('length must be greater than 7 for valid syntax')
    if self.compiler.next() != Token.FUNCTION: self.compiler.error("FUNCTION token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.IDENTIFIER: self.compiler.error("IDENTIFIER token expected. Found " + self.compiler.next())
    if self.compiler.next(2) != Token.LPAREN: self.compiler.error("LPAREN token expected. Found " + self.compiler.next())
    
    self.name = self.compiler.tokens[1].text
    self.compiler.skip(3) # function <IDENTIFIER> (
    self.parameters = Parameters(self.compiler).build()
    
    if self.compiler.next() != Token.RPAREN: self.compiler.error("RPAREN token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.LBLOCK: self.compiler.error("LBLOCK token expected. Found " + self.compiler.next())
    
    self.compiler.skip(2) # ) {
    self.body = Statement_List(self.compiler).build().statements
    
    if self.compiler.next() != Token.RBLOCK: self.compiler.error("RBLOCK token expected. Found " + self.compiler.next())
    self.compiler.skip(1) # }
    return self
    
  def clean(self):
    statements = list()
    for statement in self.body:
      if statement.__class__.__name__ == 'Statement_Var' and statement.which != None: #there is a "var = a,b,c" in the Function body, we need to move it before the BEGIN.
        if statement.declarations != None and statement.declarations.declarations != None:
          for declaration in statement.declarations.declarations:
            self.localvars.declarations.declarations.append(declaration)
      else:
        statements.append(statement)
    self.body = statements
    
    param_num = -1 #the parameter number (used to build global variables)
    assign_statements = list()
    
    for parameter in self.parameters.parameters:
      param_num += 1
      global_name = self.name.upper() + str(param_num) #variable which will be added to the global_vars list for the function's parameters
      
      #global variable declaration
      global_dec = Declaration(self.compiler)
      global_dec.identifier = Token(global_name, Token.IDENTIFIER, -1)
      self.compiler.program.global_var.append(global_dec)
      
      #local declaration before the BEGIN on the PROCEDURE
      local_dec = Declaration(self.compiler)
      localvar_statement = Statement_Var(self.compiler)
      local_dec.identifier = Token(parameter.text, Token.IDENTIFIER, -1)
      self.localvars.declarations.declarations.append(local_dec)
      
      #correlate the global UPPER(<IDENTIFER>)<param_num> with the incoming parameter
      assign_dec = Declaration(self.compiler)
      assign_decs = Declaration_List(self.compiler)
      assign_exp = Expression(self.compiler)
      assign_statement = Statement_Var(self.compiler)
      assign_dec.identifier = Token(parameter.text, Token.IDENTIFIER, -1)
      assign_exp.expression = [Token(global_name, Token.IDENTIFIER, -1)]
      assign_dec.value = assign_exp
      assign_decs.declarations.append(assign_dec)
      assign_statement.declarations = assign_decs
      assign_statements.append(assign_statement)
    
    self.body = assign_statements + self.body
  
  def compile(self, indent = 0):
    self.compiler.compiled.append(_indent(indent) + 'PROCEDURE ' + self.name + ';\n')
    self.localvars.compile(indent) #call the Statement_Vars which doesn't do anything if empty
    self.compiler.compiled.append(_indent(indent) + 'BEGIN\n')
    for statement in self.body:
      statement.compile(indent + 1)
    self.compiler.compiled.append(_indent(indent) + 'END;\n')

class Parameters(Node):
  """
  Paramters node type from the Grammar. Used for <CALL> and <FUNCTION>.
  TODO: Doesn't support expressions in call, only <IDENTIFIER> and <NUMBER>
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.parameters = list() #list of tokens corresponding to the parameters
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("length must be greater than 0")
    
    while self.compiler.next() in (Token.IDENTIFIER, Token.NUMBER):
      self.parameters.append(self.compiler.tokens[0])
      self.compiler.skip(1) # <IDENTIFIER>
      
      if self.compiler.next() != Token.COMMA:
        break
      elif self.compiler.next(1) in (Token.IDENTIFIER, Token.NUMBER): #it's a comma and the following token is an identifier
        self.compiler.skip(1) # ,
    return self
  
  def compile(self, indent = 0):
    pass

class Program(Node):
  """
  Program node type from the Grammar.  Parent node type which calls all parent build / clean methods in the recursive descent parser.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.statements = list() #all statements made in the lowest level of the program
    self.functions = list() #functions defined in the program
    self.global_var = list() #variables defined globally
    self.global_const = list() #constants defined globally
  
  def build(self):
    #(FALSE) if len(self.compiler.tokens) == 0: self.compiler.error('length must be greater than 0')
    
    while len(self.compiler.tokens) > 0:
      #it's either a <FUNCTION> or <STATEMENT>
      if self.compiler.next() == Token.FUNCTION:
        self.functions.append(Function(self.compiler).build())
      else:
        self.statements.append(Statement(self.compiler).build())
    return self
  
  def clean(self):
    statements = list()
    for statement in self.statements:
      statement.clean() #clean the statement
      if statement.__class__.__name__ == 'Statement_Var':
        if statement.which == Token.VAR: #pull out global VAR to the top
          if statement.declarations != None:
            for declaration in statement.declarations.declarations:
              if declaration.value == None:
                self.global_var.append(declaration)
              else:
                dec = Declaration(self.compiler) #going to add this to global_vars instead (without self.value)
                dec.identifier = declaration.identifier
                self.global_var.append(dec)
                
                decs = Declaration_List(self.compiler)
                stmt = Statement_Var(self.compiler)
                decs.declarations.append(declaration)
                stmt.declarations = decs
                statements.append(stmt)
        elif statement.which == Token.CONST: #pull out global CONST to the top
          if statement.declarations != None:
            for declaration in statement.declarations.declarations:
              self.global_const.append(declaration)
        else:
          statements.append(statement) #it's just a regular assignment
      else:
        statements.append(statement) #it's not a <STATEMENT_VAR>
    self.statements = statements
    for function in self.functions:
      function.clean() #clean the function
  
  def compile(self, indent = 0):
    #prepend the global constants to the program
    if len(self.global_const) > 0:
      self.compiler.compiled.append('CONST\n' + _indent(indent + 1))
      for declaration in self.global_const[:-1]:
        declaration.compile(0)
        self.compiler.compiled.append(', ')
      self.global_const[-1].compile(0)
      self.compiler.compiled.append(';\n\n')
    
    #prepend the global variables to the program
    if len(self.global_var) > 0:
      self.compiler.compiled.append('VAR\n' + _indent(indent + 1))
      for declaration in self.global_var[:-1]:
        declaration.compile(0)
        self.compiler.compiled.append(', ')
      self.global_var[-1].compile(0)
      self.compiler.compiled.append(';\n\n')
    
    #render the compiled functions to the program
    for function in self.functions:
      function.compile()
      self.compiler.compiled.append('\n')
    
    #render the compiled statements to the program
    if len(self.statements) > 0:
      self.compiler.compiled.append('BEGIN\n')
      for statement in self.statements:
        statement.compile(1)
      self.compiler.compiled.append('END');
    
    #put a random period at the end : )
    self.compiler.compiled.append('.\n')

class Statement(Node):
  """
  Base Statement node type from the Grammar.  Used to dispatch between all other Statement node types
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.statement = None
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("length must be greater than 0")
    next = self.compiler.next()
    if next not in self.compiler.valid_statement_tokens: self.compiler.error("invalid first <STATEMENT> token. Found " + next)
    
    if next == Token.LBLOCK:
      self.compiler.skip(1) # {
      self.statement = Statement_List(self.compiler).build()
      if self.compiler.next() != Token.RBLOCK: self.compiler.error("RBLOCK token expected. Found " + self.compiler.next())
      self.compiler.skip(1) # }
    elif next == Token.VAR or next == Token.CONST or (next == Token.IDENTIFIER and len(self.compiler.tokens) > 1 and self.compiler.next(1) != Token.LPAREN):
      self.statement = Statement_Var(self.compiler).build()
    elif next == Token.IF:
      self.statement = Statement_Conditional(self.compiler).build()
    elif next == Token.INPUT or next == Token.OUTPUT:
      self.statement = Statement_IO(self.compiler).build()
    elif next == Token.WHILE:
      self.statement = Statement_Iteration(self.compiler).build()
    elif next == Token.SEMI:
      self.statement = Statement_Empty(self.compiler).build()
    elif next == Token.IDENTIFIER:
      self.statement = Statement_Function_Call(self.compiler).build()
    return self.statement
  
  def clean(self):
    self.statement.clean()
  
  def compile(self, indent = 0):
    self.statement.compile(indent)

class Statement_Conditional(Node):
  """
  Statement_Conditional node type from the Grammar.  Used to build IF and IF / ELSE blocks.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.condition = None
    self.if_statement = None
    self.else_statement = None
  
  def build(self):
    if len(self.compiler.tokens) < 5: self.compiler.error("must contain at least 5 tokens for valid syntax")
    if self.compiler.next() != Token.IF: self.compiler.error("IF token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.LPAREN: self.compiler.error("LPAREN token expected. Found " + self.compiler.next(1))
    
    self.compiler.skip(2) # IF (
    self.condition = Condition(self.compiler).build()
    
    if self.compiler.next() != Token.RPAREN: self.compiler.error("RPAREN token expected. Found " + self.compiler.next())
    
    self.compiler.skip(1) # )
    self.if_statement = Statement(self.compiler).build()
    
    if self.compiler.next() == Token.ELSE:
      self.compiler.skip(1) # ELSE
      self.else_statement = Statement(self.compiler).build()
    return self
  
  def compile(self, indent):
    self.compiler.compiled.append(_indent(indent) + 'IF ')
    self.condition.compile(indent + 1)
    self.compiler.compiled.append(' THEN BEGIN\n')
    self.if_statement.compile(indent + 1)
    self.compiler.compiled.append(_indent(indent) + 'END;\n')
    if self.else_statement != None: #need to use IF and invert conditional
      self.compiler.compiled.append(_indent(indent) + 'IF ')
      self.condition.compile(indent + 1, inverse = True)
      self.compiler.compiled.append(' THEN BEGIN\n')
      self.else_statement.compile(indent + 1)
      self.compiler.compiled.append(_indent(indent) + 'END;\n')

class Statement_Empty(Node):
  """
  Empty Statement node type from the Grammar.  Used for no reason other than support extraneous ';' in the code
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("must contain at least 1 token for valid syntax")
    if self.compiler.next() != Token.SEMI: self.compiler.error("SEMI token expected. Found " + self.compiler.next())
    self.compiler.skip(1) # ;
    return self

class Statement_Function_Call(Node):
  """
  Function Call statements node type from the Grammar.  Used when calling a function and optionally passing parameters.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.name = None
    self.parameters = None
  
  def build(self):
    if len(self.compiler.tokens) < 4: self.compiler.error('must contain at least 4 tokens for valid syntax')
    if self.compiler.next() != Token.IDENTIFIER: self.compiler.error("IDENTIFIER token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.LPAREN: self.compiler.error("LPAREN token expected. Found " + self.compiler.next())
    
    self.name = self.compiler.tokens[0].text
    self.compiler.skip(2)
    
    if self.compiler.next() != Token.RPAREN: #the next token isn't a right parenthesis, so there must be Parameters
      self.parameters = Parameters(self.compiler).build()
    
    if self.compiler.next() != Token.RPAREN: self.compiler.error("RPAREN token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.SEMI: self.compiler.error("SEMI token expected. Found " + self.compiler.next())
    
    self.compiler.skip(2) # ) ;
    return self
  
  def compile(self, indent):
    if self.parameters != None: #if there are parameters in this call, we need to associate them with the global variables from the FUNCTION node.
      fn = None
      for _fn in self.compiler.program.functions: #get the function from the program
        if _fn.name == self.name:
          fn = _fn
      if fn == None:
        self.compiler.error('call to Undefined function (' + self.name + ')')
        return
      param_num = 0
      while param_num < len(self.parameters.parameters):
        global_name = self.name.upper() + str(param_num)
        
        #correlate the parameter with the global variable by generating the correct number of assignment statatements.
        assign_dec = Declaration(self.compiler)
        assign_decs = Declaration_List(self.compiler)
        assign_exp = Expression(self.compiler)
        assign_statement = Statement_Var(self.compiler)
        assign_dec.identifier = Token(global_name, Token.IDENTIFIER, -1)
        assign_exp.expression = [self.parameters.parameters[param_num]]
        assign_dec.value = assign_exp
        assign_decs.declarations.append(assign_dec)
        assign_statement.declarations = assign_decs
        assign_statement.compile(indent)
        
        param_num += 1
    
    self.compiler.compiled.append(_indent(indent) + 'CALL ' + self.name + ';\n')

class Statement_IO(Node):
  """
  The Input/Output Statement node type from the grammar.  Used to input and view data / results.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.which = None
    self.expression = None
    self.identifier = None
  
  def build(self):
    if len(self.compiler.tokens) < 3: self.compiler.error("must contain at least 3 tokens for valid syntax")
    if self.compiler.next() not in (Token.INPUT, Token.OUTPUT): self.compiler.error("INPUT or OUTPUT token expected. Found " + self.compiler.next())
    
    self.which = self.compiler.tokens[0]
    self.compiler.skip(1) # INPUT | OUTPUT
    
    if self.which.type == Token.OUTPUT:
      self.expression = Expression(self.compiler).build() #outputs can be expressions, inputs need to be identifiers
    else: # it is INPUT
      if self.compiler.next() != Token.IDENTIFIER: self.compiler.error("IDENTIFIER token expected. Found " + self.compiler.next())
      self.identifier = self.compiler.tokens[0].text
      self.compiler.skip(1) # <idenfifier>
    
    if self.compiler.next() != Token.SEMI: self.compiler.error("SEMI token expected. Found " + self.compiler.next())
    
    self.compiler.skip(1) # ;
    return self
  
  def compile(self, indent):
    if self.identifier != None:
      self.compiler.compiled.append(_indent(indent) + '@ ' + self.identifier + ';\n')
    else:
      self.compiler.compiled.append(_indent(indent) + '! ')
      self.expression.compile(indent)
      self.compiler.compiled.append(';\n')

class Statement_Iteration(Node):
  """
  The Iteration Statement type.  Used to generate WHILE loops.
  TODO: implement for loops and translate them to a functionally equivalent WHILE loop.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.condition = None #the condition to terminate upon.
    self.body = None #the body to execute of the system.
  
  def build(self):
    if len(self.compiler.tokens) < 5: self.compiler.error("must contain at least 5 tokens for valid syntax")
    if self.compiler.next() != Token.WHILE: self.compiler.error("WHILE token expected. Found " + self.compiler.next())
    if self.compiler.next(1) != Token.LPAREN: self.compiler.error("LPAREN token expected. Found " + self.compiler.next(1))
    
    self.compiler.skip(2) # WHILE (
    self.condition = Condition(self.compiler).build()
    
    if self.compiler.next() != Token.RPAREN: self.compiler.error("RPAREN token expected. Found " + self.compiler.next())
    
    self.compiler.skip(1) # )
    self.body = Statement(self.compiler).build()
    return self
  
  def compile(self, indent):
    self.compiler.compiled.append(_indent(indent) + 'WHILE ')
    self.condition.compile(indent + 1)
    self.compiler.compiled.append(' DO BEGIN\n')
    self.body.compile(indent + 1)
    self.compiler.compiled.append(_indent(indent) + 'END;\n')

class Statement_List(Node):
  """
  List Statement node type from the Grammar.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.statements = list() #statments in the block
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("length must be greater than 0")
    
    while len(self.compiler.tokens) > 0 and self.compiler.next() in self.compiler.valid_statement_tokens:
      self.statements.append(Statement(self.compiler).build())
    return self
  
  def compile(self, indent):
    if len(self.statements) > 0:
      for statement in self.statements:
        statement.compile(indent)

"""class Statement_Return(Node):
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.identifier = None
  
  def build(self):
    if len(self.compiler.tokens) < 2: self.compiler.error("must contain at least 2 tokens for valid syntax")
    if self.compiler.next() != Token.RETURN: self.compiler.error("RETURN token expected. Found " + self.compiler.next())
    
    self.identifier = self.compiler.tokens[1] if self.compiler.next(1) == Token.IDENTIFIER else None
    
    if self.identifier != None:
      self.compiler.skip(1) # <identifier>
    
    if self.compiler.next() != Token.SEMI: self.compiler.error("SEMI token expected. Found " + self.compiler.next())
    return self
  
  def compile(self, indent):
    pass #this is removed
"""

class Statement_Var(Node):
  """
  Var Statement node type from the Grammar.  Used to hold a collection of declarations.
  """
  
  def __init__(self, compiler = None):
    Node.__init__(self, compiler) #call the parent abstract method
    self.which = None
    self.declarations = None
  
  def build(self):
    if len(self.compiler.tokens) == 0: self.compiler.error("length must be greater than 0")
    
    self.which = self.compiler.tokens[0].type if (self.compiler.next() == Token.VAR or self.compiler.next() == Token.CONST) else None
    
    if self.which != None:
      self.compiler.skip(1) # var | const
    
    self.declarations = Declaration_List(self.compiler).build()
    
    if self.compiler.next() != Token.SEMI: self.compiler.error("SEMI token expected. Found " + self.compiler.next())
    
    self.compiler.skip(1) # ;
    return self
  
  def compile(self, indent):
    self.declarations.which = self.which
    if len(self.declarations.declarations) > 0:
      if self.which != None:
        self.compiler.compiled.append(_indent(indent) + ('VAR ' if self.which == Token.VAR else 'CONST '))
      self.declarations.compile(indent)
      self.compiler.compiled.append(';\n')
