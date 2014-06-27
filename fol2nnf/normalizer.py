'''********************

Created on Mar 29, 2012

@author: Camilo Thorne

(NNF rewriting algorithm)

*******************'''


import ply.lex as lex2
import ply.yacc as yacc2


"""-------------------------------------------------------------
 1. Tokenizer
------------------------------------------------------------"""


# list of token names   

tokens = ('VAR', 'PRED', 'OR', 'IMP', 'LP', 'RP', 'COMMA', 'AND', 'SOME', 'ALL', 'NEG', 'EQ')

# reserved words

reserved = {'nil' : 'NIL'}

"""-------------------------------------------------------------"""

# token definitions

def t_VAR(t):
    r'(_G[0-9]+ | [A-Z])'
    t.type = reserved.get(t.value,'VAR')
    return t

def t_PRED(t):
    r'([a-z]+_[0-9]*[a-z]+_[0-9]+ | [a-z]{1,1}[0-9]+[a-z]+)'
    t.type = reserved.get(t.value,'PRED')
    return t

def t_EQ(t):
    r'eq'
    return t

def t_NEG(t):
    r'not'
    return t

def t_AND(t):
    r'and'
    return t

def t_SOME(t):
    r'some'
    return t

def t_OR(t):
    r'or'
    return t

def t_IMP(t):
    r'imp'
    return t

def t_ALL(t):
    r'all'
    return t

def t_LP(t):
    r'\('
    return t

def t_RP(t):
    r'\)'
    return t

def t_COMMA(t):
    r','
    return t

"""-------------------------------------------------------------"""

# error handling rule

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# skipping ignored characters (spaces and tabs)

t_ignore  = ' \t'

"""----------------------------------------------------------"""

# building the lexer

lexerNFO = lex2.lex(optimize=1)


"""------------------------------------------------------------
 2. Parser
------------------------------------------------------------"""


# actions

# we recursively (on the grammar rules)
# build a list-based representation of the
# FO formula parse tree (a recursive structure!)

def myparse(exp,parser):
    parsetree = parser.parse(exp,lexer=lexerNFO)
    print len(parsetree)
    return parsetree

# the following functions build the
# nodes and arcs

def leaf(atom):
    l = []
    l.append(atom)
    return l

def neg_tree(op,form1):
    l = []
    l.append(op)
    l.append(form1)
    return l

def q_tree(op,var,form1):
    l = []
    l.append(op)
    l.append(var)
    l.append(form1)
    return l

def bin_tree(op,form1,form2):
    l = []
    l.append(op)
    l.append(form1)
    l.append(form2)
    return l
        
"""-----------------------------------------------------------"""

# a. rules for complex formulas

def p_Ter(p):
    'cfor : for'
    p[0] = p[1]
    print "final formula: ", p[0]

def p_forAt(p):
    'for : atom'
    p[0] = p[1]
    print "parsed atom: ", p[0]
            
def p_forNEG2(p):
    'for : NEG LP for RP'
    p[0] = neg_tree(p[1],p[3])
    print "parsed subformula: neg: ", p[0]

def p_forAND2(p):
    'for : AND LP for COMMA for RP'
    p[0] = bin_tree(p[1],p[3],p[5])
    print "parsed subformula: and: ", p[0]
    
def p_forOR2(p):
    'for : OR LP for COMMA for RP'
    p[0] = bin_tree(p[1],p[3],p[5])   
    print "parsed subformula: or: ", p[0]
    
def p_forSOME2(p):
    'for : SOME LP VAR COMMA for RP'
    p[0] = q_tree(p[1],p[3],p[5])
    print "parsed formula: some: ", p[0]
    
def p_forALL2(p):
    'for : ALL LP VAR COMMA for RP'
    p[0] = q_tree(p[1],p[3],p[5])
    print "parsed formula: all: ", p[0]

def p_forIMP2(p):
    'for : IMP LP for COMMA for RP'
    p[0] = bin_tree('or',neg_tree('not', p[3]),p[5])
    print "parsed formula: imp: ", p[0]

"""-----------------------------------------------------------"""

# b. rules for atomic formulas

def p_atom1(p):
    'atom : PRED LP VAR RP'
    p[0] = leaf(p[1] + p[2] + p[3] + p[4])
    
def p_atom2(p):
    'atom : PRED LP VAR COMMA VAR RP' 
    p[0] = leaf(p[1] + p[2] + p[3] + p[4] + p[5] + p[6])
        
def p_atom3(p):
    'atom : EQ LP VAR COMMA VAR RP' 
    p[0] = leaf(p[1] + p[2] + p[3] + p[4] + p[5] + p[6])

"""------------------------------------------------------------"""

# c. errors
        
def p_error(t):
    print("Syntax error at '%s'" %t.value)

"""------------------------------------------------------------"""

# d. building the parser

parserNFO = yacc2.yacc(optimize=1,start='cfor')


"""-------------------------------------------------------------
 4. Parse tree examples
-------------------------------------------------------------"""


# complex examples
fnnf1   = "not(some(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(not(v1love(C)),and(r1agent(C,A),r1patient(C,B))))))))))))"
fnnf2   = "not(some(A,and(not(some(B,not(or(q2q(B),q3q(B))))),n2n(A))))"
fnnf3   = "imp ( or( not( not( p1p(A) ) ), p2p(A) ) , p3p(A) )"
fnnf4   = "or ( not( or( p1p(A) , p2p(A) ) ) , p3p(A) )"

# simple examples
fnnf5   = "or(p1p(A),or(p2p(A),p3p(A)))"
fnnf6   = "not(p1p(A))"

#parses
ax1 = myparse(fnnf1,parserNFO)
ax2 = myparse(fnnf2,parserNFO)
ax3 = myparse(fnnf3,parserNFO)
ax4 = myparse(fnnf4,parserNFO)
ax5 = myparse(fnnf5,parserNFO)
ax6 = myparse(fnnf6,parserNFO)


"""-------------------------------------------------------------
 5. NNF rewriting
 
 nnf(A) = A
 nnf(~A) = ~A
 nnf(~~F) = nnf(F)
 nnf(~(F v F')) = nnf(~F) & nnf(~F')
 nnf(~(F & F')) = nnf(~F) v nnf(~F')
 nnf(~/\x.F) = \/x.nnf(~F)
 nnf(~\/x.F) = /\x.nnf(~F)
 nnf(F o F') = nnf(F) o nnf(F'), o = &, v
 nnf(Qx.F) = Qx.nnf(F), Q = /\, \/
-------------------------------------------------------------"""

# we push negations down to the atoms

# (this new version works!)

def nnf_rewriting2(myform):
    if (len(myform) == 1):
        return myform
    else:
        if myform[0] == 'not':
            if len(myform[1]) == 1:
                return myform
            if myform[1][0] == 'and':
                return ['or',nnf_rewriting2(['not',myform[1][1]]),
                              nnf_rewriting2(['not',myform[1][2]])]
            if myform[1][0] == 'or':
                return ['and',nnf_rewriting2(['not',myform[1][1]]),
                              nnf_rewriting2(['not',myform[1][2]])]
            if myform[1][0] == 'not':
                return nnf_rewriting2(myform[1][1])
            if myform[1][0] == 'some':
                return ['all', myform[1][1],nnf_rewriting2(['not',myform[1][2]])]
            if myform[1][0] == 'all':
                return ['all', myform[1][1],nnf_rewriting2(['not',myform[1][2]])]
        if (myform[0] == 'and') | (myform[0] == 'or'):
            return [myform[0],nnf_rewriting2(myform[1]),nnf_rewriting2(myform[2])]
        if (myform[0] == 'some') | (myform[0] == 'all'):
            return [myform[0],nnf_rewriting2(myform[1]),nnf_rewriting2(myform[2])]


"""-------------------------------------------------------------
 6. Printing the parse tree as a FO formula
-------------------------------------------------------------"""


# infix syntax
def form_printer(myform):
    # basis (atoms)
    if len(myform) == 1:
        return myform[0]
    else:
        # case for bin operators
        if (myform[0] == 'or') | (myform[0] == 'and'):
            return '(' + form_printer(myform[1]) + ' ' + myform[0] + ' ' + form_printer(myform[2]) + ')'
        # case for negations
        if (myform[0] == 'not'):
            return myform[0] + '(' + form_printer(myform[1]) + ')'
        # case for quantifiers
        if (myform[0] == 'some') | (myform[0] == 'all'):
            return myform[0] + '[' + myform[1] + ']' + '(' + form_printer(myform[2]) + ')'

# infix tptp syntax
def tptp_printer(myform):
    # basis (atoms)
    if len(myform) == 1:
        return myform[0]
    else:
        # case for bin operators
        if (myform[0] == 'or'):
            return '(' + tptp_printer(myform[1]) + ' v ' + tptp_printer(myform[2]) + ')'
        if (myform[0] == 'and'):
            return '(' + tptp_printer(myform[1]) + ' & ' + tptp_printer(myform[2]) + ')'
        # case for negations
        if (myform[0] == 'not'):
            return '~' + tptp_printer(myform[1])
        # case for quantifiers
        if (myform[0] == 'some') | (myform[0] == 'all'):
            return '?' + ' [' + myform[1] + ']' + ' : ' + tptp_printer(myform[2])
        if (myform[0] == 'all') | (myform[0] == 'all'):
            return '!' + ' [' + myform[1] + ']' + ' : ' + tptp_printer(myform[2])

# boxer prefix syntax       
def box_printer(myform):
    # basis (atoms)
    if len(myform) == 1:
        return myform[0]
    else:
        # case for bin operators
        if (myform[0] == 'and'):
            return myform[0] + '(' + box_printer(myform[1]) + ',' + box_printer(myform[2]) + ')'
        if (myform[0] == 'or'):
            return myform[0] + '(' + box_printer(myform[1]) + ',' + box_printer(myform[2]) + ')'
        # case for negations
        if (myform[0] == 'not'):
            return myform[0] + '(' + box_printer(myform[1]) + ')'
        # case for quantifiers
        if (myform[0] == 'some'):
            return myform[0] + '(' + myform[1] + ',' + box_printer(myform[2]) + ')'
        if (myform[0] == 'all'):
            return myform[0] + '(' + myform[1] + ',' + box_printer(myform[2]) + ')'


#"""-------------------------------------------------------------
# 5. Sample output
#-------------------------------------------------------------"""
#
## testing the two functions/procedures
#
#print ax1
#print nnf_rewriting2(ax1)
#print box_printer(ax1)
#print box_printer(nnf_rewriting2(ax1))
#print tptp_printer(nnf_rewriting2(ax1))
#
#print "\n"
#
#print ax2
#print nnf_rewriting2(ax2)
#print box_printer(ax2)
#print box_printer(nnf_rewriting2(ax2))
#print tptp_printer(nnf_rewriting2(ax2))