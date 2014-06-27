"""-------------------------------------------------------------
Sample output
-------------------------------------------------------------"""

from normalizer import *

# testing the two functions/procedures

print ax1
print nnf_rewriting2(ax1)
print box_printer(ax1)
print box_printer(nnf_rewriting2(ax1))
print tptp_printer(nnf_rewriting2(ax1))

print "\n"

print ax2
print nnf_rewriting2(ax2)
print box_printer(ax2)
print box_printer(nnf_rewriting2(ax2))
print tptp_printer(nnf_rewriting2(ax2))