## SCANNER
class Token(object):
    """Tokentype is one of (ID, NUM, DOT, CONST, EQUAL,
    COMMA, SEMI, VAR, PROCEDURE, ASSIGN, CALL, BEGIN, END,
    IF, THEN, WHILE, DO, ODD, HASH, LT, LTEQ, GT, GTEQ,
    PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EXCLAIM, EOF, ILLEGAL).
    Please DO NOT touch this doc string.
    """
    def __init__(self, txt, tktp, linenum):
        self.text = txt
        self.tokentype = tktp
        self.linenum = linenum
    def __str__(self):
        return '%s("%s")' % (self.tokentype, self.text)

    __repr__ = __str__

# evil magic
(lambda doc:
        map(lambda t: setattr(Token, t, t),
            [ t.rstrip(',') for t in doc[doc.find('(')+1 : doc.find(')')].split() ]
        )
)(Token.__doc__)

# all token types that can be reconized literally, that is, except ID, NUM, EOF and ILLEGAL
literal_words = {
    ':=' : 'ASSIGN',
    '<=' : 'LTEQ',
    '>=' : 'GTEQ',
    '<' : 'LT',
    '>' : 'GT',
    '#' : 'HASH',
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'MUL',
    '/' : 'DIV',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '!' : 'EXCLAIM',
    '.' : 'DOT',
    '=' : 'EQUAL',
    ',' : 'COMMA',
    ';' : 'SEMI',
    'VAR' : 'VAR',
    'CONST' : 'CONST',
    'PROCEDURE' : 'PROCEDURE',
    'CALL' : 'CALL',
    'BEGIN' : 'BEGIN',
    'END' : 'END',
    'IF' : 'IF',
    'THEN' : 'THEN',
    'WHILE' : 'WHILE',
    'DO' : 'DO',
    'ODD' : 'ODD',
}

def lookahead(n=1):
    # make sure buffer has at least n tokens
    _replenishbuf(n)
    return _buf[:n]

def nexttoken():
    # make sure buffer has at least 1 token
    _replenishbuf(1)
    return _buf.pop(0)


def _replenishbuf(target_size=1):
    """Makes sure the buffer has at least target_size number of tokens by
       repeatedly reading in lines and tokenizing them.
       At the end of the file stream this means multiple <EOF> tokens, however
       our parse stops at the first one.
       """
    global _linenum
    while len(_buf) < target_size:
        line = _srcfile.readline()
        # may reach EOF
        if not line:
            _buf.append(Token('', Token.EOF, _linenum))
            continue
        # nay, not EOF - let's deal with this line
        _linenum += 1
        _tokenizeline(line)

def _tokenizeline(line):
    """Tokenizes a line of PL/0 source code and updates the buffer."""
    # a simple but working tokenizing algorithm!
    line = line.rstrip()
    while line:
        line = line.lstrip()
        if line[:2] in (':=', '<=', '>='):
            # double-char symbols
            _buf.append(Token(line[:2],
                                getattr(Token, literal_words[line[:2]]),
                                _linenum))
            line = line[2:]
            continue
        elif line[0] in ('<', '>', '#', '+', '-', '*', '/',
                            '(', ')', '!', '.', '=', ',', ';'):
            # single-char symbols
            _buf.append(Token(line[0],
                                getattr(Token, literal_words[line[0]]),
                                _linenum))
            line = line[1:]
            continue
        else:
            # keywords, ids, numbers or illegal
            import re
            m = re.match('[a-zA-Z]\w*', line)
            if m:
                # keywords or ids - they're reconized by the same re
                # but we need to construct different types of token
                text = m.group()
                if literal_words.has_key(text):
                    # keywords
                    t = Token(text, getattr(Token, literal_words[text]), _linenum)
                else:
                    # ids
                    t = Token(text, Token.ID, _linenum)
                _buf.append(t)
                line = line[len(text):]
                continue
            m = re.match('\d+', line)
            if m:
                # numbers
                text = m.group()
                _buf.append(Token(text, Token.NUM, _linenum))
                line = line[len(text):]
                continue
            # illegal if it's not one of the first three
            # consider the first part of the line until a whitespace an illegal token
            print line
            m = re.match('(\S)\s', line)
            text = m.group(1)
            _buf.append(Token(text, Token.ILLEGAL, _linenum))
            line = line[len(text):]

## AUXILIARIES
def init(f):
    """Call this when before a new parsing occurs.
       Usually this is done by the parser."""
    global _srcfile, _buf, _linenum
    # the file is opened and closed outside this module
    _srcfile = f
    _buf = []
    _linenum = 0

