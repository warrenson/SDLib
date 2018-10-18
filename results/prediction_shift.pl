#!/usr/bin/env perl
#
use strict;

open(my $ratings_file, $ARGV[0]) || die;

# Store original ratings, per user id, and sum them per item
my %ratings;
while (<$ratings_file>) {
    my ($user, $item, $rating) = split();
    $ratings{"$item"}{'users'}{"$user"} = $rating; 
}
close($ratings_file);

# Sum ratings per item 
foreach my $item ( sort keys %ratings ) {
    $ratings{"$item"}{'pre'} = 0;
    foreach my $user ( sort keys %{$ratings{"$item"}{'users'} } ) {
        #print "Adding $item, $user, $val\n";
        $ratings{"$item"}{'pre'} += $ratings{"$item"}{'users'}{"$user"};
    }
    #print "$item ", $ratings{"$item"}{'pre'}, "\n";
}

# zero the rating for users which are predicted to be shillers
my $removed = 0;
open(my $predictions_file, $ARGV[1]) || die;
while (<$predictions_file>) {
    my ($user, $real, $prediction) = split(',');
    if ($prediction == 1) {
        $removed++;
        foreach my $item ( sort keys %ratings ) {
            if (exists($ratings{"$item"}{'users'}{"$user"})) {
                #print "Removing $old, from $item, for user:$user\n";
                $ratings{"$item"}{'users'}{"$user"} = 0;
            }
        }
    }
}
close($predictions_file);
#print "Removed $removed shillers\n";

# Sum ratings per item, post shiller removal
foreach my $item ( sort keys %ratings ) {
    $ratings{"$item"}{'post'} = 0;
    foreach my $user ( sort keys %{$ratings{"$item"}{'users'} } ) {
        $ratings{"$item"}{'post'} += $ratings{"$item"}{'users'}{"$user"};
    }
}

# Compare before and after metrics
my $diff_sum = 0;
my $pre_sum = 0;
my $post_sum = 0;

foreach my $item ( sort keys %ratings ) {
    my $pre  = $ratings{"$item"}{'pre'};
    my $post = $ratings{"$item"}{'post'};
    die "$pre, $post" if ($pre < $post); # makes no sense
    my $diff =  abs($pre - $post);

    $diff_sum += $diff;
    $pre_sum  += $pre;
    $post_sum += $post
}

#   print "Removed: $removed shillers\n";
#   print "Pre Item Ratings Sum: $pre_sum\n";
#   print "Post Item Ratings Sum: $post_sum\n";
#   print "Differnce: $diff_sum\n";
#printf "%0.2f,%0.2f,%0.2f,%0.4f\n", $pre_sum, $post_sum, $diff_sum, $post_sum / $pre_sum;
printf "%0.4f\n", $post_sum / $pre_sum;

exit 0;

