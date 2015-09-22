use warnings;
use strict;
use Data::Dumper;
use Bio::SeqIO;
use Statistics::Basic qw(:all);

# Input processing

my $fasta = $ARGV[0];
my $feature = $ARGV[1];

my %protein;
&parseFASTA(\%protein,$fasta);
my $id = (keys %protein)[0];
my $seq = $protein{$id};

$feature = "Alpha-helix, Deleage-Roux, Protein Engineering 1987, 1:289-294" if $feature eq "alphahelix";
$feature = "Normalized frequency of beta-sheet, Chou-Fasman, Adv. Enzymol. 1978, 47:45-148" if $feature eq "betasheet";
$feature = "DisProt, Dunker AK, Protein Pept Lett. 2008; 15(9): 956–963" if $feature eq "disorder";
$feature = "Hydrophobicity, Eisenberg et al, J. Mol. Biol. 1984, 179:125-142" if $feature eq "hydrophobicity";

# Database parsing

my $database = 'database/scales.txt';

local $/ = "";
my @arr;
open FILE, $database or die $!;
while ( <FILE> ) {
    chomp;
    $_=~ s/\n/"\t"/g;
    push @arr,$_;
}
close FILE;
my %HoA;
for my $str(@arr){
    my($a,$b)=split/"\t"/,$str;
    $HoA{$a} = $b;
}
my @k = keys %HoA;

my $alpha = "ARNDCQEGHILKMFPSTWYVX";
my @a = split//,$alpha;

my %profile;
my $n = scalar keys %HoA;
for my $scale (0..$n-1){
    my $sum = 0;
    for my $i (split//,$seq){
        my( $index )= grep { $a[$_] eq $i } 0..$#a;
        my @b = split/ /,$HoA{$k[$scale]};
        push @{$profile{$k[$scale]}}, $b[$index];
    }
}

# Output printing

open PROFILE, '>', 'outputs/profile.txt' or die $!;
open TABLE, '>', 'outputs/table.txt' or die $!;
for my $k(keys %profile){
    next if $feature ne $k;
    print PROFILE join("\t",$id,"@{$profile{$k}}"),"\n";
    print TABLE join("\t",$id,median(@{$profile{$k}}),mean(@{$profile{$k}}),variance(@{$profile{$k}}),stddev(@{$profile{$k}})),"\n";
}
close PROFILE;
close TABLE;

# Subrutines

sub parseFASTA {
    my $hash  = $_[0];
    my $reader=new Bio::SeqIO(-format=>'fasta',-file=>$_[1]);
    while (my $seqRec=$reader->next_seq)
    {
        $hash->{$seqRec->id} = $seqRec->seq;
        
    }
}
