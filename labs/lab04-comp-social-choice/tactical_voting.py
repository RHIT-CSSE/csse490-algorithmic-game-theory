"""
Tactical voting analysis framework for ranked voting systems.

This module provides tools for exploring whether voter groups can benefit
by misreporting their preferences (tactical voting) under different voting systems.
"""
from colorama import Fore
from typing import List, Dict, Tuple, Callable
from ballot import Ballot, aggregate_ballot_types
import algorithms


def simulate_election_with_modified_ballots(original_ballots: List[Ballot],
                                           voter_type: Ballot,
                                           new_ranking: List[str],
                                           voting_system: Callable,
                                           candidates: List[str]) -> Tuple[List[str], Dict]:
    """
    Simulate an election where voters of a specific type change their ballots.
    
    Creates a counterfactual scenario: "What if voters with ballot type X
    had instead voted with ranking Y?"
    
    Args:
        original_ballots: The actual ballots cast
        voter_type: The Ballot type that will be modified
        new_ranking: The alternative ranking those voters will report
        voting_system: The voting algorithm function (copeland, borda_count, or schulze)
        candidates: List of candidate names
    
    Returns:
        Tuple of (winner_list, scores_dict) from the modified election
    
    DO NOT MODIFY THIS FUNCTION
    """
    # Count how many voters have this type
    type_counts = aggregate_ballot_types(original_ballots)
    num_of_type = type_counts.get(voter_type, 0)
    
    if num_of_type == 0:
        # This voter type doesn't exist in the election
        return voting_system(original_ballots, candidates)
    
    # Create modified ballot list: replace all ballots of this type
    modified_ballots = []
    new_ballot = Ballot(new_ranking)
    
    for ballot in original_ballots:
        if ballot == voter_type:
            modified_ballots.append(new_ballot)
        else:
            modified_ballots.append(ballot)
    
    # Run election with modified ballots
    return voting_system(modified_ballots, candidates)


def find_tactical_opportunities(voter_type: Ballot,
                                all_ballots: List[Ballot],
                                voting_system: Callable,
                                candidates: List[str]) -> List[Dict]:
    """
    Search for tactical voting opportunities for a specific voter type.
    
    A tactical voting opportunity exists when voters of this type could achieve
    a better outcome by reporting a different preference ranking than their
    true preferences.
    
    Args:
        voter_type: The Ballot type to analyze (represents their TRUE preferences)
        all_ballots: All ballots in the election (including this type)
        voting_system: The voting algorithm function to test
        candidates: List of candidate names
    
    Returns:
        List of dictionaries, each describing a tactical opportunity:
        {
            'original_winners': list of winners with honest voting,
            'alternative_ranking': the misreported ranking,
            'new_winners': list of winners if voter type misreports,
            'benefit': description of why this is beneficial
        }
    
    TODO: Implement this method. 
    Remember, use simple heuristics rather than exhaustive search.
    """
    opportunities = []
    original_winners, _ = voting_system(all_ballots, candidates)
    true_ranking = voter_type.get_ranking()
    
    alternative_rankings = []

    # TODO: Append your alternative rankings to test here. 
    # Then, delete the line below to enable testing your alternatives. 
    raise NotImplementedError("Tactical voting opportunity detection not yet implemented")

    # Test each alternative ranking
    for alt_ranking in alternative_rankings:
        new_winners, _ = simulate_election_with_modified_ballots(
            all_ballots, voter_type, alt_ranking, voting_system, candidates
        )
        
        # Check if outcome improved for this voter type
        # "Improved" means their favorite wins when they didn't before,
        # or a more-preferred candidate wins
        if is_better_outcome(true_ranking, original_winners, new_winners):
            opportunities.append({
                'original_winners': original_winners,
                'alternative_ranking': alt_ranking,
                'new_winners': new_winners,
                'benefit': describe_benefit(true_ranking, original_winners, new_winners)
            })
    
    return opportunities


def is_better_outcome(true_ranking: List[str], 
                     original_winners: List[str], 
                     new_winners: List[str]) -> bool:
    """
    Determine if the new outcome is better for a voter than the original.
    
    Args:
        true_ranking: Voter's true preference ranking
        original_winners: Winners under honest voting
        new_winners: Winners under tactical voting
    
    Returns:
        True if new outcome is strictly better for this voter
    
    DO NOT MODIFY THIS FUNCTION
    """
    # Find highest-ranked candidate in original winners
    original_best_position = min(
        true_ranking.index(w) for w in original_winners if w in true_ranking
    )
    
    # Find highest-ranked candidate in new winners
    new_best_position = min(
        true_ranking.index(w) for w in new_winners if w in true_ranking
    )
    
    # Better if a more-preferred candidate wins (lower position index)
    return new_best_position < original_best_position


def describe_benefit(true_ranking: List[str],
                    original_winners: List[str],
                    new_winners: List[str]) -> str:
    """
    Describe why the new outcome is beneficial.
    
    DO NOT MODIFY THIS FUNCTION
    """
    # Find which candidate from new_winners is most preferred
    new_best = min(new_winners, key=lambda c: true_ranking.index(c))
    new_position = true_ranking.index(new_best)
    
    # Find which candidate from original_winners is most preferred
    orig_best = min(original_winners, key=lambda c: true_ranking.index(c))
    orig_position = true_ranking.index(orig_best)
    
    return (f"Voter's {_ordinal(new_position + 1)} choice ({new_best}) wins instead of "
            f"{_ordinal(orig_position + 1)} choice ({orig_best})")


def _ordinal(n: int) -> str:
    """
    Convert number to ordinal string (1st, 2nd, 3rd, etc.).

    DO NOT MODIFY THIS FUNCTION
    """
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


def run_tactical_voting_experiments(ballots: List[Ballot], candidates: List[str]) -> None:
    """
    Run tactical voting analysis across all voting systems and voter types.
    
    For each voting system and each voter type, checks whether that type
    could benefit from misreporting their preferences.
    
    Args:
        ballots: List of Ballot objects representing the election
        candidates: List of candidate names
    
    DO NOT MODIFY THIS FUNCTION
    """
    voting_systems = {
        'Copeland': algorithms.copeland,
        'Borda Count': algorithms.borda_count,
        'Schulze': algorithms.schulze
    }
    
    # Aggregate ballots into types
    voter_types = aggregate_ballot_types(ballots)
    
    print("\n" + "="*70)
    print("TACTICAL VOTING ANALYSIS")
    print("="*70)
    print(f"\nAnalyzing {len(ballots)} ballots with {len(voter_types)} distinct voter types")
    print(f"Candidates: {', '.join(candidates)}")
    
    for system_name, system_func in voting_systems.items():
        print("\n" + "-"*70)
        print(f"Voting System: {system_name}")
        print("-"*70)
        
        # Get honest voting outcome
        try:
            honest_winners, honest_scores = system_func(ballots, candidates)
            print(f"Honest voting winners: {', '.join(honest_winners)}")
            print(f"Honest voting scores: {honest_scores}")
        except NotImplementedError:
            print(f"  {system_name} not yet implemented - skipping tactical voting analysis")
            continue
        
        found_some_opportunity = False

        # Analyze each voter type
        for voter_type, count in voter_types.items():
            voter_type_str = f"\nVoter type ({count} voters): {voter_type}"
            
            try:
                opportunities = find_tactical_opportunities(
                    voter_type, ballots, system_func, candidates
                )

                if opportunities:
                    found_some_opportunity = True
                    print(voter_type_str)
                    opp_string = "opportunity" if len(opportunities) == 1 else "opportunities"
                    print(f"  {Fore.RED}Found {len(opportunities)} tactical voting {opp_string}!{Fore.RESET}")
                    for i, opp in enumerate(opportunities, 1):
                        print(f"\n  Opportunity {i}:")
                        print(f"    If they report: {' > '.join(opp['alternative_ranking'])}")
                        print(f"    New winners: {', '.join(opp['new_winners'])}")
                        print(f"    Benefit: {opp['benefit']}")
                elif len(ballots) <= 10: # Keep output tidy for large elections
                    print(voter_type_str)
                    print(f"  {Fore.GREEN}✓{Fore.RESET} No tactical voting opportunities found.")
                    print(f"    System appears strategy-proof for this type.")

            except NotImplementedError:
                print(f"    Tactical opportunity detection not yet implemented")
                break  # Don't repeat message for every voter type
        
        if not found_some_opportunity:
            print(f"\n{Fore.GREEN}✓ No tactical voting opportunities found for any voter type.{Fore.RESET}")
    
    print("\n" + "="*70)
    print("Analysis complete. See results above.")
    print("="*70)
