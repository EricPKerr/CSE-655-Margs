class ASTNode(object):
    # support subscription
    def __getitem__(self, i):
        # each instance of the concrete subclasses of ASTNode must provide a
        # children property to indicate its child nodes in the AST
        # by this way we can mimic the list representation of the parse tree,
        # which is the "format" used by the prettyPrintTree function
        return self.children[i]

    # support iteration
    def __iter__(self):
        return self.children

    def __init__(self):
        raise Exception('Can\'t initialize an abstract class.')

    def __str__(self):
        return self.__class__.__name__

    __repr__ = __str__

class Program(ASTNode):
    block = None
    def __init__(self, blk):
        self.block = blk
        self.children = [ self.__class__.__name__, blk ]

class Block(ASTNode):
    const_names, const_values = [], []
    var_names = []
    procs = []
    stmt = None
    def __init__(self, cnames, cvalues, vnames, ps, s):
        self.const_names, self.const_values = cnames, cvalues
        self.var_names = vnames
        self.procs = ps
        self.stmt = s
        self.children = [ self.__class__.__name__, cnames, cvalues, vnames ]
        # add procedures to the children list individually, not as a list
        self.children.extend(ps)
        self.children.append(s)

# this is the only ASTNode that doesn't correrspond to one of the
# non-terminals (or a subclass of a non-terminals) of the grammer.
class Procedure(ASTNode):
    name, block = None, None
    def __init__(self, n, blk):
        self.name, self.block = n, blk
        self.children = [ self.__class__.__name__, n, blk ]

class Statement(ASTNode):
    def __init__(self):
        raise Exception('Can\'t initialize an abstract class.')

class AssignStatement(Statement):
    name, expr = None, None
    def __init__(self, n, e):
        self.name, self.expr = n, e
        self.children = [ self.__class__.__name__, n, e ]

class CallStatement(Statement):
    proc_name = None
    def __init__(self, p):
        self.proc_name = p
        self.children = [ self.__class__.__name__, p ]

class SeqStatement(Statement):
    stmts = []
    def __init__(self, sts):
        self.stmts = sts
        self.children = [ self.__class__.__name__ ]
        # add statements to the children list individually, not as a list
        self.children.extend(sts)

class IfStatement(Statement):
    cond, stmt = None, None
    def __init__(self, c, st):
        self.cond, self.stmt = c, st
        self.children = [ self.__class__.__name__, c, st ]

class WhileStatement(Statement):
    cond, stmt = None, None
    def __init__(self, c, st):
        self.cond, self.stmt = c, st
        self.children = [ self.__class__.__name__, c, st ]

class PrintStatement(Statement):
    expr = None
    def __init__(self, e):
        self.expr = e
        self.children = [ self.__class__.__name__, e ]

class InputStatement(Statement):
    variable = None
    def __init__(self, e):
        self.variable = e.terms[0].children[2].name.text
        self.children = [ self.__class__.__name__, e ]

class Condition(ASTNode):
    def __init__(self):
        raise Exception('Can\'t initialize an abstract class.')

class OddCondition(Condition):
    expr = None
    def __init__(self, e):
        self.expr = e
        self.children = [ self.__class__.__name__, e ]

class BinaryCondition(Condition):
    lhs_expr, rhs_expr = None, None
    cmp = None
    def __init__(self, lhs, rhs, c):
        self.lhs_expr, self.rhs_expr = lhs, rhs
        self.cmp = c
        self.children = [ self.__class__.__name__, lhs, rhs, c ]

class Expression(ASTNode):
    # len(signs) == len(terms) or
    # len(signs) == len(terms) - 1 must be satisfied
    signs, terms = [], []
    def __init__(self, s, t):
        self.signs, self.terms = s, t
        self.children = [ self.__class__.__name__, s ]
        # add terms to the children list individually, not as a list
        self.children.extend(t)

class Term(ASTNode):
    # len(signs) == len(terms) - 1 must be satisfied
    signs, factors = [], []
    def __init__(self, s, f):
        self.signs, self.factors = s, f
        self.children = [ self.__class__.__name__, s ]
        # add factors to the children list individually, not as a list
        self.children.extend(f)

class Factor(ASTNode):
    def __init__(self):
        raise Exception('Can\'t initialize an abstract class.')

class IdFactor(Factor):
    name = None
    def __init__(self, n):
        self.name = n
        self.children = [ self.__class__.__name__, n ]

class NumFactor(Factor):
    number = None
    def __init__(self, n):
        self.number = n
        self.children = [ self.__class__.__name__, n ]

class ExprFactor(Factor):
    expr = None
    def __init__(self, e):
        self.expr = e
        self.children = [ self.__class__.__name__, e ]

