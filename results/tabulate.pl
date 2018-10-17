#!/usr/bin/env perl
#
# 0.2-0.05_kmeans_reverse-bandwagon_p1.res.txt
use strict;

my $file = $ARGV[0];

my $name = `basename $file .res.txt`;
chomp $name;

my ($sizes, $method, $attack, $param) = split('_', $name); 
$param ||= 'NA';
my ($attack_size, $filler_size) = split('-', $sizes);

my $lastline = `tail -n1 $file`;
$lastline =~ s/^\s+|\s+$//g;
my ($label, $pres, $rec, $f1, $sup) = split(/\s+/, $lastline);

# HEADER
# METHOD,PARAMS,ATTACK,ATTACK-SIZE,FILLER-SIZE,PRECISION,RECALL,F1,SUPPORT
print join(',',
    $method,
    $param,
    $attack,
    $attack_size,
    $filler_size,
    $pres,
    $rec,
    $f1,
    $sup
), "\n";
