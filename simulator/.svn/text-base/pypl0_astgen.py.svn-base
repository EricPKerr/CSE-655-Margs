def traverse(node):
    """Traverses the (concrete) parse tree and
        generates the abstract syntax tree.
       Param node is a (partial) parse tree like
        ['<PROGRAM>',
         ['<BLOCK>' ... ],
         DOT("."),
         EOF("")]
    """
    if hasattr(node, '__iter__'):
        # non-terminal nodes
        tag = node[0]
        if tag == '<PROGRAM>' and node[1][0] == '<BLOCK>':
            return Program(traverse(node[1]))

        elif tag == '<BLOCK>':
            const_names, const_values = [], []
            var_names = []
            procs = []
            stmt = None
            # skip the '<BLOCK>' tag
            lst = node[1:]

            # CONST
            if lst and hasattr(lst[0], 'tokentype') and \
               lst[0].tokentype == Token.CONST:
                # skip the CONST token
                lst = lst[1:]
                for i, token in enumerate(lst):
                    if token.tokentype == Token.SEMI:
                        lst = lst[i+1:]
                        break
                    elif token.tokentype == Token.ID:
                        const_names.append(token)
                    elif token.tokentype == Token.NUM:
                        const_values.append(token)

            # VAR
            if lst and hasattr(lst[0], 'tokentype') and \
               lst[0].tokentype == Token.VAR:
                # skip the VAR token
                lst = lst[1:]
                for i, token in enumerate(lst):
                    if token.tokentype == Token.SEMI:
                        lst = lst[i+1:]
                        break
                    elif token.tokentype == Token.ID:
                        var_names.append(token)

            # PROCEDURE
            while lst and hasattr(lst[0], 'tokentype') and \
                  lst[0].tokentype == Token.PROCEDURE:
                procs.append(Procedure(lst[1], traverse(lst[3])))
                lst = lst[5:]

            # STATEMENT
            if lst and hasattr(lst[0], '__iter__') and \
               lst[0][0] == '<STATEMENT>' and lst[0][1:]:
                # the last condition is to test if STATEMENT is empty
                stmt = traverse(lst[0])

            return Block(const_names, const_values, var_names, procs, stmt)
        elif tag == '<STATEMENT>':
            # skip the '<STATEMENT>' tag
            lst = node[1:]

            # ASSIGN
            if lst and hasattr(lst[0], 'tokentype') and \
               lst[0].tokentype == Token.ID:
                return AssignStatement(lst[0], traverse(lst[2]))

            # CALL
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.CALL:
                return CallStatement(lst[1])

            # BEGIN - END
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.BEGIN:
                stmts = []
                # skip the BEGIN token
                for e in lst[1:]:
                    if hasattr(e, 'tokentype') and e.tokentype == Token.END:
                        break
                    elif hasattr(e, '__iter__') and e[0] == '<STATEMENT>' \
                                                and e[1:]:
                        # the last condition is to test if STATEMENT is empty
                        stmts.append(traverse(e))
                return SeqStatement(stmts)

            # IF
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.IF:
                return IfStatement(traverse(lst[1]), traverse(lst[3]))

            # WHILE
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.WHILE:
                return WhileStatement(traverse(lst[1]), traverse(lst[3]))

            # !
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.EXCLAIM:
                return PrintStatement(traverse(lst[1]))

        elif tag == '<CONDITION>':
            # skip the '<CONDITION>' tag
            lst = node[1:]

            # ODD
            if lst and hasattr(lst[0], 'tokentype') and \
               lst[0].tokentype == Token.ODD:
                return OddCondition(traverse(lst[1]))

            # BINARY
            elif lst and hasattr(lst[0], '__iter__') and \
               lst[0][0] == '<EXPRESSION>':
                return BinaryCondition(traverse(lst[0]),
                                       traverse(lst[2]),
                                       lst[1])

        elif tag == '<EXPRESSION>':
            signs, terms = [], []
            # skip the '<EXPRESSION>' tag
            lst = node[1:]

            for e in lst:
                if hasattr(e, 'tokentype') and \
                   (e.tokentype == Token.PLUS or
                    e.tokentype == Token.MINUS):
                    signs.append(e)
                elif hasattr(e, '__iter__') and e[0] == '<TERM>':
                    terms.append(traverse(e))
            return Expression(signs, terms)

        elif tag == '<TERM>':
            signs, factors = [], []
            # skip the '<TERM>' tag
            lst = node[1:]

            for e in lst:
                if hasattr(e, 'tokentype') and \
                   (e.tokentype == Token.MUL or
                    e.tokentype == Token.DIV):
                    signs.append(e)
                elif hasattr(e, '__iter__') and e[0] == '<FACTOR>':
                    factors.append(traverse(e))
            return Term(signs, factors)

        elif tag == '<FACTOR>':
            # skip the '<FACTOR>' tag
            lst = node[1:]

            if lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.ID:
                return IdFactor(lst[0])
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.NUM:
                return NumFactor(lst[0])
            elif lst and hasattr(lst[0], 'tokentype') and \
                 lst[0].tokentype == Token.LPAREN:
                return ExprFactor(traverse(lst[1]))

    else:
        # terminal nodes - tokens are good representation of them
        # they should never be passed to this function
        raise Exception('Please do not pass in anything except a parse tree \
                internal node. Recieved: %s' % (str(node), ))

# import the Token definition from the scanner
from pypl0_scanner import Token

# import the AST node definitions from pypl0_astnodes
import pypl0_astnodes
d = {}
for name in dir(pypl0_astnodes):
    n = getattr(pypl0_astnodes, name)
    # if it's a class and it's a subclass of pypl0_astnodes.ASTNode
    if isinstance(n, type) and issubclass(n, pypl0_astnodes.ASTNode):
        d[name] = n
globals().update(d)

del(pypl0_astnodes)
del(d)
del(name)
del(n)

