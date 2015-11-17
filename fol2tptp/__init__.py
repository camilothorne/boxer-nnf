from wrapper import * 

for1 = "not(all(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(v1love(C),and(r1agent(C,A),r1patient(C,B))))))))))))"
for2 = "fol(1,not(all(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(v1love(C),and(r1agent(C,A),r1patient(C,B)))))))))))))"
for3 = "some(A,and(pernammia(A),some(B,and(r1agent(B,A),v1walk(B)))))"

# we print the (test) results

print parserFO.parse("man(A,B)",lexerFO)                + "\n"
print parserFO.parse("pernammia(A)",lexerFO)            + "\n"
print parserFO.parse("n1man(A)",lexerFO)                + "\n"
print parserFO.parse("not(man(A))",lexerFO)             + "\n"
print parserFO.parse("and(n1man(A),man(A))",lexerFO)    + "\n"
print parserFO.parse(for1,lexer=lexerFO)                + "\n"
print parserFO.parse(for2,lexer=lexerFO)                + "\n"
print parserFO.parse(for3,lexer=lexerFO)                + "\n"
