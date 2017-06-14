#!/usr/bin/python3
# demo code for instant runnoff voting. For question about
# "Australian voting" in interview. Algorithm works by giving
# the winner if there is a majority count, and if not, by assigning
# second-place votes after eliminating lowest vote-getter
import sys

def read_ballots(file_path):
    """
    Reads a csv-style file, pulls each record into its own list, and
    returns the a list of these
    :param file_path: full path to CSV-style file; each line contains
    a ranked ballot
    :returns list of ballots, each ballot is a RANKED list of votes
    """
    pass


def read_candidates(file_path):
    """
    Reads a list of candidates from file. Each line contains the name
    of one candidate, as the the name would be lisited on the ballot
    :param file_path: full path to file; each line is name of one candidate
    :returns list of candidates
    """
    pass


def scrub_invalid_ballots(input_ballots):
    """
    Goes through ballots; it throws out any ballot where the list of
    candidates are not represented on the ballot
    """
    pass


def instant_runoff(scrubbed_ballots, candidate_set):
    """
    Counts first-place votes from all ballots. If a majority winner
    exists, returns the winner. Otherwise, adjusts the ballots to throw
    out the loser and rerun. To prevent a tie resulting in a loop, it will
    pick a random winner in the case of a two-way tie ONLY in the case where
    both have exactly 50% of the vote.
    NOTE THAT BOTH IN-PARAMS WILL BE CHANGED
    :param scrubbed_ballots: list of ballots; each element of list is 
    itself a preference-sorted ballot
    :param candidate_set: the list of candidates
    :returns the candidate that won
    """
    top_picks = [ballot[0] for ballot in scrubbed_ballots]
    ballot_counts = {}
    for candidate in candidate_set:
        ballot_counts[candidate] = top_picks.count(candidate)
        
    num_ballots = len(top_picks)
    for candidate in top_picks:
        if ballot_counts[candidate] > round(num_ballots / 2):
            return candidate     # we have a winner!!
        elif (ballot_counts[candidate] == round(num_ballots / 2) and
              len(candidate_set) == 2):
              return candidate    # tie, just pick one

    # if reached here, we need to toss out the lowest candidate
    loser = min(ballot_counts, key=ballot_counts.get)
    candidate_set.remove(loser)
    for ballot in scrubbed_ballots:
        ballot.remove(loser)
    return instant_runoff(scrubbed_ballots, candidate_set)
    

def irv(ballot_path, candidate_list_path):
    """
    Top-level routine - reads file with ballots, verifies ballots,
    and runs instant-voting procedure
    :param file_path: full path to CSV-style file; each line contains
    a ranked ballot
    :returns winner
    """
    ballot_array = read_ballots(file_path)
    candidate_array = read_candidates(candidate_list_path)
    cleaned_ballots = scrub_invalid_ballots(ballot_array, candidate_array)
    winner = instant_runoff(cleaned_ballots, candidate_array)
    return winner


    
if __name__ == "main":
    if len(sys.argv) != 3:
        print "Unable to run - no argument given!"
    else:
        result = irv(sys.argv[1], sys.argv[2])
        print "The top vote-getter: " + result
