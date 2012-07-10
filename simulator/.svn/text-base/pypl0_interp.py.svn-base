## the symbol table
# string : number
const_dict = {}
# string : number
var_dict = {}
# string : Block(ASTNode)
proc_dict = {}

def interpret(node):
    map(dict.clear, (const_dict, var_dict, proc_dict))
    interpretProgram(node)

def interpretProgram(node):
    interpretBlock(node.block)

def interpretBlock(node):
    for k, v in zip(node.const_names, node.const_values):
        if const_dict.has_key(k.text):
            raise Exception('Const %s cannot be redefined at line %d.'
                    % (k.text, k.linenum))
        else:
            const_dict[k.text] = int(v.text)
    for k in node.var_names:
        if var_dict.has_key(k.text):
            raise Exception('Variable %s cannot be redeclared at line %d.'
                    % (k.text, k.linenum))
        else:
            var_dict[k.text] = None
    map(interpretProcedure, node.procs)
    if node.stmt:
        interpretAbstractType(node.stmt)

def interpretProcedure(node):
    if proc_dict.has_key(node.name.text):
        raise Exception('Procedure %s cannot be redeclared at line %d.'
                % (node.name.text, node.name.linenum))
    else:
        proc_dict[node.name.text] = node.block

def interpretAssignStatement(node):
    if not var_dict.has_key(node.name.text):
        raise Exception('Variable %s assigned before declaration at line %d.'
                % (node.name.text, node.name.linenum))
    else:
        var_dict[node.name.text] = interpretExpression(node.expr)

def interpretCallStatement(node):
    if not proc_dict.has_key(node.proc_name.text):
        raise Exception('Procedure %s undefined at line %d.'
                % (node.proc_name.text, node.proc_name.linenum))
    else:
        interpretBlock(proc_dict[node.proc_name.text])

def interpretSeqStatement(node):
    map(interpretAbstractType, node.stmts)

def interpretIfStatement(node):
    if interpretAbstractType(node.cond):
        interpretAbstractType(node.stmt)

def interpretWhileStatement(node):
    while interpretAbstractType(node.cond):
        interpretAbstractType(node.stmt)

def interpretPrintStatement(node):
    import sys
    sys.stdout.write(str(interpretExpression(node.expr)))

def interpretOddCondition(node):
    return interpretExpression(node.expr)

def interpretBinaryCondition(node):
    l = interpretExpression(node.lhs_expr)
    r = interpretExpression(node.rhs_expr)
    cmp = node.cmp.text
    return {'<=': l <= r,
            '>=': l >= r,
            '<': l < r,
            '>': l > r,
            '=': l == r,
            '#': not l == r }[cmp]

def interpretExpression(node):
    signs, terms = node.signs, node.terms
    if len(signs) == len(terms) - 1:
        firstsign = 1
    elif len(signs) == len(terms):
        firstsign = -1 if signs[0] == '-' else 1
        signs = signs[1:]
    accum = firstsign * interpretTerm(terms[0])
    terms = terms[1:]
    for s, t in zip(signs, terms):
        if s.text == '+':
            accum += interpretTerm(t)
        elif s.text == '-':
            accum -= interpretTerm(t)
    return accum

def interpretTerm(node):
    signs, factors = node.signs, node.factors
    accum = interpretAbstractType(factors[0])
    factors = factors[1:]
    for s, f in zip(signs, factors):
        if s.text == '*':
            accum *= interpretAbstractType(f)
        elif s.text == '/':
            accum /= interpretAbstractType(f)
    return accum

def interpretIdFactor(node):
    n = node.name.text
    if const_dict.has_key(n):
        return const_dict[n]
    if var_dict.has_key(n):
        # have to compare with None here since it can be 0
        # if we provide a null value in PL/0 we need to distinguish
        # "uninitialized" and "null" from implementation perspective
        if var_dict[n] == None:
            raise Exception('Variable %s used before initialized at line %d.'
                    % (node.name.text, node.name.linenum))
        else:
            return var_dict[n]
    raise Exception('Identifier %s not found at line %d.'
            % (node.name.text, node.name.linenum))

def interpretNumFactor(node):
    return int(node.number.text)

def interpretExprFactor(node):
    return interpretExpression(node.expr)

def interpretAbstractType(node):
    return apply(eval('interpret' + node.__class__.__name__), (node, ))

