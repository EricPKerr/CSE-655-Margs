## PARSER
# A recursive descent parser - almost a direct translation of the grammer.
def parse(f):
    _init(f)
    return program()

def program():
    return '<PROGRAM>', block(), _expect(Token.DOT), _expect(Token.EOF)

def block():
    result = ['<BLOCK>']

    if lk1().tokentype == Token.CONST:
        result.extend(
                map(_expect,
                    (Token.CONST, Token.ID, Token.EQUAL, Token.NUM)))
        while lk1().tokentype == Token.COMMA:
            result.extend(
                    map(_expect,
                        (Token.COMMA, Token.ID, Token.EQUAL, Token.NUM)))
        result.append(_expect(Token.SEMI))

    if lk1().tokentype == Token.VAR:
        result.extend(
                map(_expect,
                    (Token.VAR, Token.ID)))
        while lk1().tokentype == Token.COMMA:
            result.extend(
                    map(_expect,
                        (Token.COMMA, Token.ID)))
        result.append(_expect(Token.SEMI))

    while lk1().tokentype == Token.PROCEDURE:
        result.extend(
                map(_expect,
                    (Token.PROCEDURE, Token.ID, Token.SEMI)))
        result.append(block())
        result.append(_expect(Token.SEMI))

    result.append(statement())

    return result

def statement():
    result = ['<STATEMENT>']

    t = lk1()
    if t.tokentype == Token.ID:
        result.extend(
                map(_expect,
                    (Token.ID, Token.ASSIGN)))
        result.append(expression())
    elif t.tokentype == Token.CALL:
        result.extend(
                map(_expect,
                    (Token.CALL, Token.ID)))
    elif t.tokentype == Token.BEGIN:
        result.append(_expect(Token.BEGIN))
        result.append(statement())
        while lk1().tokentype == Token.SEMI:
            result.append(_expect(Token.SEMI))
            result.append(statement())
        result.append(_expect(Token.END))
    elif t.tokentype == Token.IF:
        result.append(_expect(Token.IF))
        result.append(condition())
        result.append(_expect(Token.THEN))
        result.append(statement())
    elif t.tokentype == Token.WHILE:
        result.append(_expect(Token.WHILE))
        result.append(condition())
        result.append(_expect(Token.DO))
        result.append(statement())
    elif t.tokentype == Token.EXCLAIM:
        result.append(_expect(Token.EXCLAIM))
        result.append(expression())

    return result

def condition():
    result = ['<CONDITION>']

    if lk1().tokentype == Token.ODD:
        result.append(_expect(Token.ODD))
        result.append(expression())
    else:
        result.append(expression())
        t = lk1()
        if t.tokentype == Token.EQUAL:
            result.append(_expect(Token.EQUAL))
        elif t.tokentype == Token.HASH:
            result.append(_expect(Token.HASH))
        elif t.tokentype == Token.LT:
            result.append(_expect(Token.LT))
        elif t.tokentype == Token.LTEQ:
            result.append(_expect(Token.LTEQ))
        elif t.tokentype == Token.GT:
            result.append(_expect(Token.GT))
        elif t.tokentype == Token.GTEQ:
            result.append(_expect(Token.GTEQ))
        else:
            _reporterror((Token.EQUAL,
                          Token.HASH,
                          Token.LT,
                          Token.LTEQ,
                          Token.GT,
                          Token.LTEQ),
                         t)
        result.append(expression())

    return result

def expression():
    result = ['<EXPRESSION>']

    t = lk1()
    if t.tokentype == Token.PLUS:
        result.append(_expect(Token.PLUS))
    elif t.tokentype == Token.MINUS:
        result.append(_expect(Token.MINUS))

    result.append(term())

    t = lk1()
    while t.tokentype == Token.PLUS or t.tokentype == Token.MINUS:
        if t.tokentype == Token.PLUS:
            result.append(_expect(Token.PLUS))
        elif t.tokentype == Token.MINUS:
            result.append(_expect(Token.MINUS))
        else:
            _reporterror((Token.PLUS, Token.MINUS), t)
        result.append(term())
        t = lk1()

    return result

def term():
    result = ['<TERM>']

    result.append(factor())

    t = lk1()
    while t.tokentype == Token.MUL or t.tokentype == Token.DIV:
        if t.tokentype == Token.MUL:
            result.append(_expect(Token.MUL))
        elif t.tokentype == Token.DIV:
            result.append(_expect(Token.DIV))
        else:
            _reporterror((Token.MUL, Token.DIV), t)
        result.append(factor())
        t = lk1()

    return result

def factor():
    result = ['<FACTOR>']

    t = lk1()
    if t.tokentype == Token.ID:
        result.append(_expect(Token.ID))
    elif t.tokentype == Token.NUM:
        result.append(_expect(Token.NUM))
    elif t.tokentype == Token.LPAREN:
        result.append(_expect(Token.LPAREN))
        result.append(expression())
        result.append(_expect(Token.RPAREN))
    else:
        _reporterror((Token.ID, Token.NUM, Token.LPAREN), t)

    return result

## AUXILIARIES
def _expect(tokentype):
    """Matches the next token."""
    ntk = nexttoken()
    if ntk.tokentype == tokentype:
        return ntk
    else:
        _reporterror((tokentype, ), ntk)

def _reporterror(expectedTokenTypes, actualToken):
    raise Exception('Parsing error at line %d: expecting one of (%s); got %s'
                % (actualToken.linenum,
                   ', '.join(expectedTokenTypes),
                   str(actualToken)))

def _init(f):
    global Token, nexttoken, lk1
    # feed the file to the scanner
    import pypl0_scanner
    pypl0_scanner.init(f)
    # these 3 are what we need from our pypl0_scanner
    Token, nexttoken = pypl0_scanner.Token, pypl0_scanner.nexttoken
    # we only need lookahead(1) for PL/0 grammer
    lk1 = lambda : pypl0_scanner.lookahead()[0]

