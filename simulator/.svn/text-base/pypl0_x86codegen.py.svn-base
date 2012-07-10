## the symbol table - well, the symbol lists actually since we don't need more
## information than names for such simple semantic checking as we only check for
## duplicate declarations. We don't do type checking since there's only one type
## - integer
# string
const_names = []
# string : number
var_names = []
# string : Block(ASTNode)
proc_names = []

## generated code for .data and .bss segments, and for constants
data = []
bss = []
const = []

## The x86 assembly code generator. Also does minimal semantic checking.
def gen(node, ofile):
    del(const_names[:])
    del(var_names[:])
    del(proc_names[:])
    del(const[:])
    del(data[:])
    del(bss[:])
    _getUniqueLabel.count = -1
    textSeg = genProgram(node)
    ofile.write(tpls['main']
        % ('\n'.join(data), '\n'.join(const), '\n'.join(bss), textSeg))

def genProgram(node):
    return genBlock(node.block)

def genBlock(node):
    for k, v in zip(node.const_names, node.const_values):
        if k.text in const_names:
            raise Exception('Const %s cannot be redefined at line %d.'
                    % (k.text, k.linenum))
        else:
            const_names.append(k.text)
            const.append(tpls['const'] % (k.text, v.text))
    for k in node.var_names:
        if k.text in var_names:
            raise Exception('Variable %s cannot be redeclared at line %d.'
                    % (k.text, k.linenum))
        else:
            var_names.append(k.text)
            # using double words (32 bits) to store integers
            bss.append(tpls['var'] % (k.text, ))
    result = map(genProcedure, node.procs)
    if node.stmt:
        result.append(genAbstractType(node.stmt))
    return '\n'.join(result)

def genProcedure(node):
    if node.name.text in proc_names:
        raise Exception('Procedure %s cannot be redeclared at line %d.'
                % (node.name.text, node.name.linenum))
    else:
        proc_names.append(node.name.text)
        return tpls['proc'] % ('end' + node.name.text,
                               node.name.text,
                               genBlock(node.block),
                               'end' + node.name.text)

def genAssignStatement(node):
    n = node.name.text
    if not n in var_names:
        raise Exception('Variable %s assigned before declaration at line %d.'
                % (n, node.name.linenum))
    else:
        return tpls['assign'] % (genExpression(node.expr), n)

def genCallStatement(node):
    if not node.proc_name.text in proc_names:
        raise Exception('Procedure %s undefined at line %d.'
                % (node.proc_name.text, node.proc_name.linenum))
    else:
        return tpls['call'] % (node.proc_name.text, )

def genSeqStatement(node):
    return '\n'.join(map(genAbstractType, node.stmts))

def genIfStatement(node):
    label = _getUniqueLabel('endif')
    return tpls['if'] % (genAbstractType(node.cond, label),
                              genAbstractType(node.stmt), label)

def genWhileStatement(node):
    whilelabel = _getUniqueLabel('while')
    endwhilelabel = _getUniqueLabel('endwhile')
    return tpls['while'] % (whilelabel,
                            genAbstractType(node.cond, endwhilelabel),
                            genAbstractType(node.stmt),
                            whilelabel,
                            endwhilelabel)

def genPrintStatement(node):
    return tpls['print'] % (genExpression(node.expr), )

def genOddCondition(node, jmplabel):
    # essentially a comparison with 0
    return tpls['oddcond'] % (genExpression(node.expr), jmplabel)

def genBinaryCondition(node, jmplabel):
    def decideJumpInstruction(cmp):
        # actually jumping means "don't go into the if block"
        # so we use the opposite cmp operator
        return { '<=': 'jg',
                 '>=': 'jl',
                 '<': 'jge',
                 '>': 'jle',
                 '=': 'jne',
                 '#': 'je' }[cmp]
    return tpls['bincond'] % (genExpression(node.lhs_expr),
                              genExpression(node.rhs_expr),
                              decideJumpInstruction(node.cmp.text),
                              jmplabel)

def genExpression(node):
    result = []
    signs, terms = node.signs, node.terms
    # first we generate code for the first term
    if len(signs) == len(terms) - 1:
        firstsign = '+'
    elif len(signs) == len(terms):
        firstsign = signs[0].text
        signs = signs[1:]
    result.append(tpls['exprfirst']
            % (genTerm(terms[0]),
               tpls['negate'] if firstsign == '-' else ''))
    terms = terms[1:]
    # then we generate code for other signs and terms
    for s, t in zip(signs, terms):
        result.append(tpls['expr']
                % (genTerm(t), 'sub' if s.text == '-' else 'add'))
    result.append(tpls['exprend'])
    return '\n'.join(result)

def genTerm(node):
    result = []
    signs, factors = node.signs, node.factors
    result.append(tpls['termfirst'] % (genAbstractType(factors[0])))
    factors = factors[1:]
    for s, f in zip(signs, factors):
        if s.text == '*':
            result.append(tpls['termmul'] % (genAbstractType(f), ))
        elif s.text == '/':
            result.append(tpls['termdiv'] % (genAbstractType(f), ))
    result.append(tpls['termend'])
    return '\n'.join(result)

def genIdFactor(node):
    n = node.name.text
    if n in const_names:
        return tpls['idfacconst'] % (n, )
    if n in var_names:
        return tpls['idfacvar'] % (n, )
    raise Exception('Identifier %s not found at line %d.'
            % (n, node.name.linenum))

def genNumFactor(node):
    return tpls['numfac'] % (node.number.text, )

def genExprFactor(node):
    return genExpression(node.expr)

def genAbstractType(node, extra=None):
    return apply(
            eval('gen' + node.__class__.__name__),
            (node, extra) if extra else (node, ))

## AUXILIARIES
def _getUniqueLabel(prefix):
    _getUniqueLabel.count += 1
    return prefix + str(_getUniqueLabel.count)

import pypl0_x86codegentpl
tpls = pypl0_x86codegentpl.templates
del(pypl0_x86codegentpl)

