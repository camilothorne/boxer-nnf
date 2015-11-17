from wrapper import * 

for1 = "not(all(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(v1love(C),and(r1agent(C,A),r1patient(C,B))))))))))))"
for2 = "fol(1,not(all(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(v1love(C),and(r1agent(C,A),r1patient(C,B)))))))))))))"
for3 = "some(A,and(pernammia(A),some(B,and(r1agent(B,A),v1walk(B)))))"
for4 = "some(G64474,and(some(A,and(card(G64474,G64577),and(c245num(G64577),nnumeral1(G64577)))),and(atopic1(G64474),nthing12(G64474))))"

# we print the (test) results

print parserFO.parse("all(A)",lexerFO)

#print "fof(1,conjecture," + parserFO.parse(for1,lexer=lexerFO) + ")\n"
#print "fof(1,conjecture," + parserFO.parse(for2,lexer=lexerFO) + ")\n"
#print "fof(1,conjecture," + parserFO.parse(for3,lexer=lexerFO) + ")\n"
#print "fof(1,conjecture," + parserFO.parse(for4,lexer=lexerFO) + ")\n"