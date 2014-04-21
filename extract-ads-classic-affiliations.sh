#!/bin/bash -xe

export PERL5LIB=/proj/ads/soft/adsperl/lib64/perl5:/proj/ads/soft/adsperl/lib/perl5:/proj/ads/soft/abs/absload/lib

AFFILIATION_HOME=`pwd`

cd $AFFILIATION_HOME/extracted_affiliations/input

perl /proj/ads/soft/bin/extract_affils.pl --quiet AST
