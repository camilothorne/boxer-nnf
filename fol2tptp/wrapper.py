'''********************

Created on Mar 29, 2012

@author: Camilo Thorne

(Boxer2TPTP wrapper/driver)

*******************'''

import re
import ply.lex as lex
import ply.yacc as yacc


"""-------------------------------------------------------------
 1. Tokenizer
------------------------------------------------------------"""

# reserved words

reserved = {
            
    'not' : 'NEG',
    'all' : 'ALL',
    'some': 'SOME',
    'or'  : 'OR',
    'and' : 'AND',
    'imp' : 'IMP',
    'eq'  : 'EQ',
    'card': 'CARD',
    'fol' : 'TYP'
    
}

# list of token names   

tokens = ['VAR', 'PRED', 'DIG', 'LP', 'COMMA', 'RP'] + list(reserved.values())

"""-------------------------------------------------------------"""

# token definitions

def t_VAR(t):
    r'(_G[0-9]+ | [A-Z])'
    # check for reserved words
    t.type = reserved.get(t.value,'VAR')
    #print t.value
    return t

def t_PRED(t):
    #r'([a-z]+ | [A-Za-z0-9_]+_[0-9A-Za-z\-]+ | [a-z]{1,1}[0-9]+[a-z]+)'
    r'([a-z]+([0-9]+[a-z]+)* | [A-Za-z0-9_]+_[0-9A-Za-z\-]+ | [a-z]{1,1}[0-9]+[a-z]+)'
    # check for reserved words
    t.type = reserved.get(t.value,'PRED')
    #print t.value
    return t

def t_LP(t):
    r'\('
    #print t.value
    return t
 
def t_RP(t):
    r'\)'
    #print t.value
    return t
 
def t_COMMA(t):
    r','
    #print t.value
    return t

def t_DIG(t):
    r'\d'
    t.type = reserved.get(t.value,'DIG')
    return t

"""-------------------------------------------------------------"""

# error handling rule

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# skipping ignored characters (spaces, tabs, etc.)

t_ignore  = ' \t'
t_ignore  = ' [.]'

"""----------------------------------------------------------"""

# building the lexer

lexerFO = lex.lex(optimize=1,reflags=re.UNICODE)


"""------------------------------------------------------------
 2. Parser
------------------------------------------------------------"""


# infixing operator

def infix(operator,opb,form1,com,form2,cb):
    return opb + form1 + operator + form2 + cb

# rewriting of quantifiers

def quant(oper,var,form):
    return oper + " [" + var[0:] + "]: " + form 

"""-----------------------------------------------------------"""

# a. rules for complex formulas
    
def p_forAt(p):
    'for : atom'
    # nothing to do
    p[0] = p[1]
    print "parsed formula: ", p[0]
        
def p_forNEG(p):
    'for : NEG LP for RP'
    # we change only the negation symbol
    p[0] = "~" + p[2] + p[3] + p[4]
    #print "parsed formula: ", p[0]
    
def p_forAND(p):
    'for : AND LP for COMMA for RP'
    # infixing
    p[0] = infix(" & ",p[2],p[3],p[4],p[5],p[6]) 
    #print "parsed formula: ", p[0]
    
def p_forSOME(p):
    'for : SOME LP VAR COMMA for RP'
    # rewriting
    p[0] = quant("(?",p[3],p[5]+")")
    #print "parsed formula: ", p[0]
    
def p_forOR(p):
    'for : OR LP for COMMA for RP'
    # infixng
    p[0] = infix(" | ",p[2],p[3],p[4],p[5],p[6]) 
    #print "parsed formula: ", p[0]

def p_forIMP(p):
    'for : IMP LP for COMMA for RP'
    # infixing
    p[0] = infix(" => ",p[2],p[3],p[4],p[5],p[6])  
    #print "parsed formula: ", p[0]

def p_forALL(p):
    'for : ALL LP VAR COMMA for RP'
    # rewriting
    p[0] = quant("(!",p[3],p[5]+")")
    #print "parsed formula: ", p[0]

def p_forTYP(p):
    'for : TYP LP DIG COMMA for RP'
    #projection
    p[0] = p[5]
    #print "parsed formula: ", p[0]    

"""-----------------------------------------------------------"""

# b. rules for atomic formulas

def p_atom1(p):
    'atom : PRED LP VAR RP'
    p[0] = p[1] + p[2] + p[3] + p[4]
    #print "atom: ", p[0]
    
def p_atom2(p):
    'atom : PRED LP VAR COMMA VAR RP' 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
    #print "atom: ", p[0]
        
def p_atom3(p):
    'atom : EQ LP VAR COMMA VAR RP' 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
    #print "equality: ", p[0]
    
def p_atom4(p):
    'atom : CARD LP VAR COMMA VAR RP' 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
    #print "equality: ", p[0]

"""------------------------------------------------------------"""

# c. errors
        
def p_error(t):
    print("Syntax error at '%s'" %t.value)

"""------------------------------------------------------------"""

# d. building the parser

parserFO = yacc.yacc(optimize=1)


"""-------------------------------------------------------------
 3. Build wrapper
-------------------------------------------------------------"""


def makeWrapper(formula,typ):
    if None != parserFO.parse(formula,lexer=lexerFO):
        if typ == "axiom":
            return "fof(comsem,axiom, " + parserFO.parse(formula,lexer=lexerFO) + " )."
        if typ == "conjecture":
            return "fof(comsem,conjecture, " + parserFO.parse(formula,lexer=lexerFO) + " )."
        if typ == "plain":
            return parserFO.parse(formula,lexer=lexerFO)
    else:
        return ""