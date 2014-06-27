from wrapper import *
#
#
#"""-------------------------------------------------------------
# Sample output
#-------------------------------------------------------------"""
#
#
## semantics of "The winner of Marengo hates loosing very much"
#
#form = "some(_G2870,and(n_winner_1(_G2870),some( _G2927,and(l_marengo_1(_G2927),and(r_of_1( _G2870,_G2927),some(_G3009,and(v_loose_1(_G3009),and(a_much_1(_G3009),and(a_very_1(_G3009),and(n_event_1(_G3009),r_agent_1(_G3009,_G2870)))))))))))"
#fnnf = "not(some(A,and(n1man(A),not(not(not(some(B,some(C,and(n1man(B),and(v1love(C),and(r1agent(C,A),r1patient(C,B))))))))))))"

uni = "some(_G46653,and(o_nccn_clinical_practice_guidelines_1(_G46653),some(_G46710,some(_G46731,and(and(n_www_1(_G46731),and(r_nn_1(_G46710,_G46731),o_oncology™_breast_cancer_v22007_continue_1(_G46710))),and(r_in_1(_G46653,_G46731),a_topic_1(_G46653)))))))"
uni2 = "o_nccn_clinical_practice_guidelines_1(_G46653)"
uni3 = "some(_G47944,some(_G47965,some(_G47986,some(_G48007,and(a_html_1(_G47965),and(n_category_1(_G47965),and(n_consensus_1(_G47986),and(n_proposition_1(_G48007),and(a_topic_1(_G47965),and(r_nn_1(_G47944,_G47965),and(r_colon_1(_G47986,_G48007),and(r_of_1(_G47965,_G47986),and(o_nccn_1(_G47944),all(_G48277,imp(n_recommendation_1(_G48277),some(_G48334,and(p_category_2a_1(_G48334),some(_G48384,some(_G48405,some(_G48426,and(v_specify_1(_G48426),and(a_otherwise_1(_G48426),and(n_event_1(_G48384),and(r_patient_1(_G48426,_G48405),and(r_unless_1(_G48384,_G48426),eq(_G48277,_G48334))))))))))))))))))))))))))"
uni4 ="some(_G64474,and(some(_G64577,and(card(_G64474,_G64577),and(c_245_num(_G64577),n_numeral_1(_G64577)))),and(a_topic_1(_G64474),n_thing_12(_G64474))))"

#
#
## we print the (test) results

##print "fof(1,axiom,( " + parserFO.parse(form,lexer=lexerFO) + " ))\n"
##print "fof(1,conjecture,( " + parserFO.parse(form,lexer=lexerFO) + " ))\n"
##print "fof(1,axiom,( " + parserFO.parse(fnnf,lexer=lexerFO) + " ))\n"
##print "fof(1,conjecture,( " + parserFO.parse(fnnf,lexer=lexerFO) + " ))\n"


#print parserFO.parse(uni2,lexer=lexerFO)
print "fof(1,conjecture," + parserFO.parse(uni3,lexer=lexerFO) + ")\n"