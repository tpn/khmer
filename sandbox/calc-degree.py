#! /usr/bin/env python2
#
# This file is part of khmer, http://github.com/ged-lab/khmer/, and is
# Copyright (C) Michigan State University, 2009-2013. It is licensed under
# the three-clause BSD license; see doc/LICENSE.txt.
# Contact: khmer-project@idyll.org
#
import sys
import screed.fasta
import os
import khmer

K = 31                                  # use K-1 for assembly K
HASHTABLE_SIZE = int(1e9)
N_HT = 4

###

infile = sys.argv[1]
outfp = open(os.path.basename(infile) + '.degree', 'w')

print 'making hashtable'
ht = khmer.new_hashbits(K, HASHTABLE_SIZE, N_HT)

print 'eating', infile
ht.consume_fasta(infile)

for n, record in enumerate(screed.fasta.fasta_iter(open(infile),
                                                   parse_description=False)):
    if n % 10000 == 0:
        print '... calc', n
    if n > 1e5:
        break

    name = record['name']
    seq = record['sequence']

    for j in range(len(seq) - K):
        kmer = seq[j:j + K]
        print >>outfp, ht.kmer_degree(kmer)
